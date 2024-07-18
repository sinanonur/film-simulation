import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import colour
import json
import os
import psutil
from scipy.interpolate import interp1d
import piexif
import argparse
import multiprocessing
from functools import partial

class FilmProfile:
    def __init__(self, name, color_curves, contrast, saturation, chromatic_aberration, blur, base_color, grain_amount, grain_size):
        self.name = name
        self.color_curves = color_curves
        self.contrast = contrast
        self.saturation = saturation
        self.chromatic_aberration = chromatic_aberration
        self.blur = blur
        self.base_color = base_color
        self.grain_amount = grain_amount
        self.grain_size = grain_size

def create_curve(curve_data):
    x = np.array(curve_data['x'])
    y = np.array(curve_data['y'])
    return interp1d(x, y, kind='cubic', bounds_error=False, fill_value=(y[0], y[-1]))

def load_film_profiles_from_json(json_path):
    with open(json_path, 'r') as f:
        profiles_data = json.load(f)
    
    profiles = {}
    for name, data in profiles_data.items():
        color_curves = {
            channel: create_curve(curve_data)
            for channel, curve_data in data['color_curves'].items()
        }
        profiles[name] = FilmProfile(
            name,
            color_curves=color_curves,
            contrast=data['contrast'],
            saturation=data['saturation'],
            chromatic_aberration=data.get('chromatic_aberration', 0),
            blur=data.get('blur', 0),
            base_color=tuple(data.get('base_color', (255, 255, 255))),
            grain_amount=data.get('grain_amount', 0),
            grain_size=data.get('grain_size', 1)
        )
    return profiles

def apply_color_curves(image, curves):
    result = np.zeros_like(image)
    for i, channel in enumerate(['R', 'G', 'B']):
        result[:,:,i] = curves[channel](image[:,:,i])
    return result

def apply_chromatic_aberration_pil(img, strength):
    width, height = img.size
    center_x, center_y = width // 2, height // 2
    
    r, g, b = img.split()
    
    def create_displacement(x, y):
        return int(strength * ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5 / (width + height))
    
    r = r.transform(img.size, Image.AFFINE, (1, 0, create_displacement(0, 0), 0, 1, 0))
    b = b.transform(img.size, Image.AFFINE, (1, 0, -create_displacement(0, 0), 0, 1, 0))
    
    return Image.merge("RGB", (r, g, b))

def add_film_grain(image, amount=0.1, size=1):
    width, height = image.size
    grain = np.random.normal(0, amount, (height//size, width//size, 3))
    grain = np.repeat(np.repeat(grain, size, axis=0), size, axis=1)
    grain = grain[:height, :width, :]
    
    img_array = np.array(image).astype(np.float32) / 255.0
    grainy_image = np.clip(img_array + grain, 0, 1) * 255
    return Image.fromarray(grainy_image.astype(np.uint8))

def adjust_color_temperature(image, temperature):
    r_multiplier = 1 + (temperature - 6500) / 100 * 0.01
    b_multiplier = 1 - (temperature - 6500) / 100 * 0.01
    g_multiplier = 1
    
    r, g, b = image.split()
    
    r = r.point(lambda i: min(255, int(i * r_multiplier)))
    g = g.point(lambda i: min(255, int(i * g_multiplier)))
    b = b.point(lambda i: min(255, int(i * b_multiplier)))
    
    return Image.merge('RGB', (r, g, b))

def apply_base_color(image, base_color):
    base = Image.new('RGB', image.size, base_color)
    return Image.blend(image, base, 0.1)  # Adjust blend factor as needed

def cross_process(image):
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(1.5)
    
    r, g, b = image.split()
    r = r.point(lambda i: min(255, int(i * 1.2)))
    g = g.point(lambda i: int(i * 0.9))
    b = b.point(lambda i: min(255, int(i * 1.1)))
    
    image = Image.merge('RGB', (r, g, b))
    
    saturation_enhancer = ImageEnhance.Color(image)
    image = saturation_enhancer.enhance(1.3)
    
    return image

def apply_film_profile(img, profile, chroma_override=None, blur_override=None, color_temp=6500, cross_process_flag=False):
    img_array = np.array(img).astype(np.float32) / 255.0
    
    img_linear = colour.models.eotf_sRGB(img_array)
    
    img_color_adjusted = apply_color_curves(img_linear, profile.color_curves)
    
    img_srgb = colour.models.eotf_inverse_sRGB(img_color_adjusted)
    
    img_pil = Image.fromarray((img_srgb * 255).astype(np.uint8))
    
    enhancer = ImageEnhance.Contrast(img_pil)
    img_contrast = enhancer.enhance(profile.contrast)
    
    enhancer = ImageEnhance.Color(img_contrast)
    img_saturated = enhancer.enhance(profile.saturation)
    
    chroma_strength = chroma_override if chroma_override is not None else profile.chromatic_aberration
    if chroma_strength > 0:
        img_saturated = apply_chromatic_aberration_pil(img_saturated, chroma_strength)
    
    blur_amount = blur_override if blur_override is not None else profile.blur
    if blur_amount > 0:
        img_saturated = img_saturated.filter(ImageFilter.GaussianBlur(radius=blur_amount))
    
    img_saturated = apply_base_color(img_saturated, profile.base_color)
    
    img_saturated = add_film_grain(img_saturated, amount=profile.grain_amount, size=profile.grain_size)
    
    img_saturated = adjust_color_temperature(img_saturated, color_temp)
    
    if cross_process_flag:
        img_saturated = cross_process(img_saturated)
    
    return img_saturated

def process_image(args):
    image_path, profile, chroma_override, blur_override, color_temp, cross_process_flag, output_filename = args
    with Image.open(image_path) as img:
        exif_data = img.getexif()
        
        orientation = exif_data.get(274, 1)
        if orientation in [3, 6, 8]:
            img = img.rotate({3: 180, 6: 270, 8: 90}[orientation], expand=True)
        
        processed_image = apply_film_profile(img, profile, chroma_override, blur_override, color_temp, cross_process_flag)

        if exif_data:
            exif_data[274] = 1
            exif_bytes = piexif.dump(exif_data)
            processed_image.info['exif'] = exif_bytes

        processed_image.save(output_filename, 'JPEG', quality=95)
        print(f"Processed image saved as {output_filename}")

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_optimal_pool_size(target_memory_usage=75):
    available_memory = 100 - get_memory_usage()
    cpu_count = multiprocessing.cpu_count()
    
    # Start with all CPUs and reduce until we're under the target memory usage
    for i in range(cpu_count, 0, -1):
        estimated_memory_usage = get_memory_usage() + (available_memory / cpu_count) * i
        if estimated_memory_usage <= target_memory_usage:
            return i
    
    return 1  # Fallback to single process if we can't meet the memory target

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply film profiles to an image.")
    parser.add_argument("input_image", help="Path to the input image")
    parser.add_argument("--profiles", help="Path to JSON file containing film profiles")
    parser.add_argument("--chroma", type=float, help="Override chromatic aberration strength")
    parser.add_argument("--blur", type=float, help="Override blur amount")
    parser.add_argument("--color_temp", type=int, default=6500, help="Color temperature (default: 6500K)")
    parser.add_argument("--cross_process", action="store_true", help="Apply cross-processing effect")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel processing")
    args = parser.parse_args()

    if args.profiles:
        film_profiles = load_film_profiles_from_json(args.profiles)
    else:
        print("No profile JSON provided. Please provide a JSON file with film profiles.")
        exit(1)

    input_path_base = os.path.splitext(args.input_image)[0]

    process_args = []
    for profile_name, profile in film_profiles.items():
        output_filename = f"{input_path_base}_{profile_name.replace(' ', '_')}.jpg"
        process_args.append((args.input_image, profile, args.chroma, args.blur, args.color_temp, args.cross_process, output_filename))

    if args.parallel:
        pool_size = get_optimal_pool_size()
        print(f"Using parallel processing with pool size: {pool_size}")
        with multiprocessing.Pool(pool_size) as pool:
            pool.map(process_image, process_args)
    else:
        print("Using sequential processing")
        for arg in process_args:
            process_image(arg)

    print("All images processed.")