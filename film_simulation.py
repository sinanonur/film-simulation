import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import colour
import json
import os
import psutil
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter
import piexif
import argparse
import multiprocessing
from functools import partial

class FilmProfile:
    def __init__(self, name, color_curves, contrast, saturation, chromatic_aberration, blur, base_color, grain_amount, grain_size,
                 halation_strength=0.0, halation_threshold=0.7, vignette_strength=0.0,
                 shadow_tint=None, highlight_rolloff=0.0, color_bleed=0.0):
        self.name = name
        self.color_curves = color_curves
        self.contrast = contrast
        self.saturation = saturation
        self.chromatic_aberration = chromatic_aberration
        self.blur = blur
        self.base_color = base_color
        self.grain_amount = grain_amount
        self.grain_size = grain_size
        self.halation_strength = halation_strength
        self.halation_threshold = halation_threshold
        self.vignette_strength = vignette_strength
        self.shadow_tint = shadow_tint if shadow_tint else [0, 0, 0]
        self.highlight_rolloff = highlight_rolloff
        self.color_bleed = color_bleed

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
            grain_size=data.get('grain_size', 1),
            halation_strength=data.get('halation_strength', 0.0),
            halation_threshold=data.get('halation_threshold', 0.7),
            vignette_strength=data.get('vignette_strength', 0.0),
            shadow_tint=data.get('shadow_tint', [0, 0, 0]),
            highlight_rolloff=data.get('highlight_rolloff', 0.0),
            color_bleed=data.get('color_bleed', 0.0)
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

def generate_perlin_noise_2d(shape, res):
    """Generate 2D Perlin noise for more realistic grain texture"""
    def interpolant(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]].transpose(1, 2, 0) % 1

    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))

    gradients = np.repeat(np.repeat(gradients, d[0], axis=0), d[1], axis=1)
    gradients = gradients[:shape[0], :shape[1]]

    g00 = gradients[:-1, :-1]
    g10 = gradients[1:, :-1]
    g01 = gradients[:-1, 1:]
    g11 = gradients[1:, 1:]

    # Ensure proper dimensions for grid
    grid = grid[:shape[0]-1, :shape[1]-1]

    # Ramps
    n00 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1])) * g00, axis=2)
    n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, axis=2)
    n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, axis=2)
    n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, axis=2)

    # Interpolation
    t = interpolant(grid)
    n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
    n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11

    noise = np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)

    # Pad the last row and column
    noise = np.pad(noise, ((0, 1), (0, 1)), mode='edge')

    return noise

def add_film_grain(image, amount=0.1, size=1):
    """Enhanced film grain with Perlin noise for realistic texture and exposure-dependent visibility"""
    width, height = image.size
    img_array = np.array(image).astype(np.float32) / 255.0

    # Calculate luminance for exposure-dependent grain
    luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]

    # Grain is most visible in midtones, less in deep shadows and highlights
    grain_mask = 1.0 - np.abs(luminance - 0.5) * 2  # Peak at 0.5, fade to 0 at extremes
    grain_mask = np.clip(grain_mask * 1.5, 0.3, 1.0)  # Clamp to ensure some grain everywhere

    # Generate Perlin noise for base grain texture
    res = (max(4, height // (size * 50)), max(4, width // (size * 50)))
    perlin_base = generate_perlin_noise_2d((height, width), res)

    # Add finer detail with higher frequency Perlin noise
    res_detail = (max(8, height // (size * 20)), max(8, width // (size * 20)))
    perlin_detail = generate_perlin_noise_2d((height, width), res_detail) * 0.5

    # Combine base and detail
    grain_texture = perlin_base + perlin_detail

    # Normalize to appropriate range
    grain_texture = (grain_texture - grain_texture.min()) / (grain_texture.max() - grain_texture.min())
    grain_texture = (grain_texture - 0.5) * amount

    # Apply grain with exposure-dependent mask to each channel with slight variation
    grainy_image = np.zeros_like(img_array)
    for i in range(3):
        # Each color channel has slightly different grain pattern
        channel_variation = np.random.normal(0, amount * 0.3, (height, width))
        channel_grain = grain_texture + channel_variation
        grainy_image[:, :, i] = img_array[:, :, i] + (channel_grain * grain_mask)

    grainy_image = np.clip(grainy_image, 0, 1) * 255
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

def apply_halation(img_array, strength=0.3, threshold=0.7):
    """
    Simulate film halation - the red/orange glow around bright highlights
    caused by light scattering through the film base
    """
    if strength <= 0:
        return img_array

    # Calculate luminance
    luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]

    # Create highlight mask (only affects bright areas)
    highlight_mask = np.clip((luminance - threshold) / (1.0 - threshold), 0, 1)
    highlight_mask = np.power(highlight_mask, 2)  # Non-linear response

    # Create halation bloom with Gaussian blur
    bloom = gaussian_filter(highlight_mask, sigma=20.0 * strength)

    # Halation is typically reddish/orange
    halation_color = np.array([1.0, 0.6, 0.3])  # Red-orange tint

    # Apply halation to each channel
    result = img_array.copy()
    for i in range(3):
        halation_layer = bloom * strength * halation_color[i]
        result[:, :, i] = np.clip(result[:, :, i] + halation_layer, 0, 1)

    return result

def apply_vignette(img_array, strength=0.3):
    """
    Apply natural lens vignetting with cosine fourth law falloff
    """
    if strength <= 0:
        return img_array

    height, width = img_array.shape[:2]

    # Create coordinate grid centered at image center
    y, x = np.ogrid[:height, :width]
    center_y, center_x = height / 2, width / 2

    # Normalize coordinates to [-1, 1]
    y_norm = (y - center_y) / (height / 2)
    x_norm = (x - center_x) / (width / 2)

    # Calculate distance from center
    radius = np.sqrt(x_norm**2 + y_norm**2)

    # Cosine fourth law falloff (more natural than simple radial)
    # Add slight elliptical shape (typical of real lenses)
    aspect_ratio = width / height
    if aspect_ratio > 1:
        x_norm = x_norm * aspect_ratio
    else:
        y_norm = y_norm / aspect_ratio

    radius = np.sqrt(x_norm**2 + y_norm**2)

    # Smooth falloff with adjustable strength
    vignette_mask = 1.0 - (radius**2 * strength * 0.7)
    vignette_mask = np.clip(vignette_mask, 0.3, 1.0)  # Prevent complete black corners

    # Apply vignette
    result = img_array * vignette_mask[:, :, np.newaxis]

    return result

def apply_shadow_tint(img_array, tint_color, strength=0.3):
    """
    Apply color tinting in shadow areas (simulates film base fog and dye interactions)
    """
    if strength <= 0:
        return img_array

    # Calculate luminance
    luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]

    # Shadow mask (affects darker areas more)
    shadow_mask = np.clip(1.0 - luminance * 2, 0, 1)  # Fade out above 0.5 luminance
    shadow_mask = np.power(shadow_mask, 1.5)  # Non-linear response

    # Convert tint color to normalized array
    tint = np.array(tint_color) / 255.0

    # Apply tint in shadows
    result = img_array.copy()
    for i in range(3):
        tint_layer = shadow_mask * strength * tint[i]
        result[:, :, i] = np.clip(result[:, :, i] + tint_layer, 0, 1)

    return result

def apply_color_bleed(img_array, strength=0.3):
    """
    Simulate color bleed/crosstalk between dye layers in color negative film
    """
    if strength <= 0:
        return img_array

    result = img_array.copy()

    # Cyan bleed from blue channel into red
    result[:, :, 0] += img_array[:, :, 2] * strength * 0.15

    # Magenta shift: red bleeds into blue
    result[:, :, 2] += img_array[:, :, 0] * strength * 0.1

    # Green channel interactions (subtle)
    result[:, :, 1] += (img_array[:, :, 0] + img_array[:, :, 2]) * strength * 0.05

    return np.clip(result, 0, 1)

def apply_highlight_rolloff(img_array, strength=0.3):
    """
    Simulate film's natural compression of highlights (shoulder of the characteristic curve)
    """
    if strength <= 0:
        return img_array

    # Calculate per-channel luminance to preserve color
    result = img_array.copy()

    for i in range(3):
        channel = img_array[:, :, i]

        # Find highlight areas (above 0.6)
        highlight_mask = np.clip((channel - 0.6) / 0.4, 0, 1)

        # Apply soft compression to highlights
        compressed = 0.6 + (1.0 - 0.6) * (1.0 - np.exp(-5 * (channel - 0.6) * (1.0 - strength)))

        # Blend original and compressed based on highlight mask
        result[:, :, i] = channel * (1 - highlight_mask) + compressed * highlight_mask

    return np.clip(result, 0, 1)

def apply_film_profile(img, profile, chroma_override=None, blur_override=None, color_temp=6500, cross_process_flag=False):
    """
    Apply film profile with improved processing order matching physical film process:
    1. Linear color space conversion
    2. Halation (film base light scatter)
    3. Highlight roll-off (film latitude)
    4. Color curves (dye response)
    5. Shadow tinting (base fog)
    6. Color bleed (dye interactions)
    7. Back to sRGB for further processing
    8. Contrast & saturation adjustments
    9. Film grain
    10. Vignetting (lens characteristic)
    11. Chromatic aberration & blur (lens effects)
    12. Base color & temperature adjustments
    """
    # Step 1: Convert to linear color space
    img_array = np.array(img).astype(np.float32) / 255.0
    img_linear = colour.models.eotf_sRGB(img_array)

    # Step 2: Apply halation (occurs in film base before dye layers)
    if profile.halation_strength > 0:
        img_linear = apply_halation(img_linear, profile.halation_strength, profile.halation_threshold)

    # Step 3: Apply highlight roll-off (film's natural highlight compression)
    if profile.highlight_rolloff > 0:
        img_linear = apply_highlight_rolloff(img_linear, profile.highlight_rolloff)

    # Step 4: Apply color curves (film dye response)
    img_color_adjusted = apply_color_curves(img_linear, profile.color_curves)

    # Step 5: Apply shadow tinting (film base fog)
    if any(t != 0 for t in profile.shadow_tint):
        img_color_adjusted = apply_shadow_tint(img_color_adjusted, profile.shadow_tint, strength=0.2)

    # Step 6: Apply color bleed (dye layer interactions)
    if profile.color_bleed > 0:
        img_color_adjusted = apply_color_bleed(img_color_adjusted, profile.color_bleed)

    # Step 7: Convert back to sRGB for PIL operations
    img_srgb = colour.models.eotf_inverse_sRGB(np.clip(img_color_adjusted, 0, 1))
    img_pil = Image.fromarray((img_srgb * 255).astype(np.uint8))

    # Step 8: Apply contrast adjustment
    enhancer = ImageEnhance.Contrast(img_pil)
    img_contrast = enhancer.enhance(profile.contrast)

    # Step 9: Apply saturation adjustment
    enhancer = ImageEnhance.Color(img_contrast)
    img_saturated = enhancer.enhance(profile.saturation)

    # Step 10: Apply film grain (happens in emulsion layer)
    if profile.grain_amount > 0:
        img_saturated = add_film_grain(img_saturated, amount=profile.grain_amount, size=profile.grain_size)

    # Step 11: Apply vignetting (lens characteristic)
    if profile.vignette_strength > 0:
        img_array_vignette = np.array(img_saturated).astype(np.float32) / 255.0
        img_array_vignette = apply_vignette(img_array_vignette, profile.vignette_strength)
        img_saturated = Image.fromarray((img_array_vignette * 255).astype(np.uint8))

    # Step 12: Apply chromatic aberration (lens aberration)
    chroma_strength = chroma_override if chroma_override is not None else profile.chromatic_aberration
    if chroma_strength > 0:
        img_saturated = apply_chromatic_aberration_pil(img_saturated, chroma_strength)

    # Step 13: Apply slight blur (emulsion diffusion)
    blur_amount = blur_override if blur_override is not None else profile.blur
    if blur_amount > 0:
        img_saturated = img_saturated.filter(ImageFilter.GaussianBlur(radius=blur_amount))

    # Step 14: Apply base color tint
    img_saturated = apply_base_color(img_saturated, profile.base_color)

    # Step 15: Apply color temperature (scanning/printing characteristics)
    img_saturated = adjust_color_temperature(img_saturated, color_temp)

    # Step 16: Optional cross-processing effect
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