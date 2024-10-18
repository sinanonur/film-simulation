import json
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFilter, ImageChops

import random

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def apply_tone_curve(image, curve_points):
    # Create a lookup table for the curve
    lut = np.interp(np.linspace(0, 255, 256), [p[0] for p in curve_points], [p[1] for p in curve_points]).astype(np.uint8)
    # Apply the lookup table to the image
    return image.point(lut)

def apply_tone_curve_per_channel(image, tone_curve_params):
    # Split the channels
    r, g, b = image.split()

    # Apply the tone curve to each channel
    r = apply_tone_curve(r, tone_curve_params['red'])
    g = apply_tone_curve(g, tone_curve_params['green'])
    b = apply_tone_curve(b, tone_curve_params['blue'])

    # Merge channels back together
    return Image.merge('RGB', (r, g, b))

def apply_exposure_adjustment(image, exposure):
    if exposure != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(exposure)
    return image

def apply_color_adjustments(image, color_params):
    saturation = color_params.get('saturation', 1.0)
    contrast = color_params.get('contrast', 1.0)

    # Apply saturation adjustment
    if saturation != 1.0:
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(saturation)

    # Apply contrast adjustment
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)

    return image

def apply_base_color(image, base_color, blend_weight=0.05):
    if base_color:
        # Convert image to a NumPy array
        img_array = np.array(image).astype(np.float32) / 255.0
        # Apply base color shift with a blending weight
        base_color_array = np.array(base_color).astype(np.float32) / 255.0
        img_array = img_array * (1 - blend_weight) + base_color_array * blend_weight
        # Clip values to ensure valid range
        img_array = np.clip(img_array, 0, 1)
        # Convert back to uint8
        img_array = (img_array * 255).astype(np.uint8)
        image = Image.fromarray(img_array)
    return image

def add_grain(image, grain_intensity):
    if grain_intensity == 0.0:
        return image

    # Generate grain
    width, height = image.size
    grain = np.random.normal(loc=128, scale=128 * grain_intensity, size=(height, width)).astype(np.uint8)

    # Convert grain to an image and resize to match the original image size
    grain_image = Image.fromarray(grain).resize(image.size, resample=Image.BILINEAR)

    # Convert image and grain to arrays
    img_array = np.array(image).astype(np.float32)
    grain_array = np.array(grain_image).astype(np.float32)

    # Expand dimensions of grain_array to match img_array (RGB channels)
    grain_array = np.repeat(grain_array[:, :, np.newaxis], 3, axis=2)

    # Blend grain with image and clip values to be within valid range
    img_array = img_array + (grain_array - 128)
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)

    return Image.fromarray(img_array)

def apply_chromatic_aberration(image, shift_amount=2):
    # Split the channels
    r, g, b = image.split()
    width, height = image.size

    # Convert to NumPy arrays for more flexible operations
    r_array = np.array(r)
    g_array = np.array(g)
    b_array = np.array(b)

    # Create shifted versions of the channels
    shifted_r = np.roll(r_array, shift_amount, axis=1)  # Shift right
    shifted_g = np.roll(g_array, -shift_amount, axis=1)  # Shift left
    shifted_b = np.roll(b_array, shift_amount, axis=0)  # Shift down

    # Convert back to images
    r = Image.fromarray(shifted_r)
    g = Image.fromarray(shifted_g)
    b = Image.fromarray(shifted_b)

    # Merge channels back together
    return Image.merge('RGB', (r, g, b))

def add_light_leak(image):
    """
    Apply a light leak effect to a PIL Image.
    
    Parameters:
    image (PIL.Image.Image): The input image.
    
    Returns:
    PIL.Image.Image: The image with a light leak effect applied.
    """
    # Ensure the image is in RGB mode
    image = image.convert('RGB')
    
    # Convert image to numpy array
    img_array = np.array(image).astype('float')
    h, w, _ = img_array.shape
    
    # Create a light leak overlay
    leak = np.zeros((h, w, 3), dtype='float')
    
    # Randomly decide the number of leaks
    num_leaks = random.randint(1, 3)
    
    for _ in range(num_leaks):
        # Random position
        x0 = random.randint(-w//2, w)
        y0 = random.randint(-h//2, h)
        
        # Random size
        radius = random.randint(w//4, int(1.5 * w))
        
        # Random color (reddish/orange hues)
        color = np.array([
            random.randint(200, 255),   # Red channel
            random.randint(50, 200),    # Green channel
            random.randint(0, 100)      # Blue channel
        ], dtype='float')
        
        # Create gradient
        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - x0)**2 + (Y - y0)**2)
        mask = (dist_from_center <= radius)
        gradient = (1 - dist_from_center / radius) * mask
        
        # Add the gradient to the leak overlay
        for i in range(3):  # For each color channel
            leak[..., i] += gradient * color[i]
    
    # Normalize leak values
    leak = np.clip(leak, 0, 255)
    
    # Blend the leak with the original image
    blended = img_array + leak * random.uniform(0.3, 0.7)
    blended = np.clip(blended, 0, 255).astype('uint8')
    
    # Convert back to PIL Image
    result_image = Image.fromarray(blended)
    
    # Optional: Adjust color balance to imitate film
    enhancer = ImageEnhance.Color(result_image)
    result_image = enhancer.enhance(1.2)
    
    # Optional: Add slight vignette effect
    vignette = Image.new('L', (w, h), 0)
    overlay = ImageDraw.Draw(vignette)
    max_dim = max(w, h)
    overlay.ellipse([(-max_dim//2, -max_dim//2), (w + max_dim//2, h + max_dim//2)], fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=max_dim//2))
    vignette_mask = ImageOps.invert(vignette).convert('L')
    result_image.putalpha(vignette_mask)
    result_image = result_image.convert('RGB')
    
    return result_image

def apply_dynamic_range_compression(image, compression_factor=0.5):
    """
    Apply dynamic range compression to simulate the limited dynamic range of film.
    
    Parameters:
    image (PIL.Image.Image): The input image.
    compression_factor (float): The factor by which to compress the dynamic range. Values between 0 and 1.
    
    Returns:
    PIL.Image.Image: The image with dynamic range compression applied.
    """
    # Convert image to NumPy array
    img_array = np.array(image).astype(np.float32) / 255.0
    
    # Apply a less aggressive dynamic range compression
    img_array = np.power(img_array, 1 - compression_factor)
    img_array = np.clip(img_array, 0, 1)
    
    # Convert back to uint8
    img_array = (img_array * 255).astype(np.uint8)
    return Image.fromarray(img_array)

import numpy as np
from PIL import Image, ImageDraw

def apply_vignette(image, radius=1.5, strength=0.8, falloff=2.0):
  """
  Apply a vignette effect to the image with adjustable falloff.
  
  Parameters:
  image (PIL.Image.Image): The input image.
  radius (float): Controls the size of the vignette effect. Lower values create a larger vignette.
  strength (float): The intensity of the vignette effect, from 0 to 1. Higher values create a stronger effect.
  falloff (float): Controls how quickly the vignette transitions from center to edge. 
                   Lower values create a steeper transition, higher values a more gradual one.
  
  Returns:
  PIL.Image.Image: The image with vignette effect applied.
  """
  x, y = np.ogrid[:image.height, :image.width]
  center = (image.height / 2, image.width / 2)
  distance_to_center = np.sqrt((x - center[0])**2 + (y - center[1])**2)
  
  # Normalize the distance
  max_distance = np.sqrt(center[0]**2 + center[1]**2)
  normalized_distance = distance_to_center / max_distance
  
  # Apply falloff
  mask = (1 - normalized_distance * radius)**falloff
  
  # Clip the mask and apply strength
  mask = np.clip(mask, 0, 1)
  mask = 1 - strength * (1 - mask)
  
  vignette = Image.fromarray(np.uint8(mask * 255), 'L')
  return ImageChops.multiply(image, Image.merge('RGB', (vignette, vignette, vignette)))

def emulate_film(image_path, config_path, output_dir, chromatic_aberration=False, shift_amount=2, light_leak=False, vignette_strength=0.3):
    # Load image and film profiles from config file
    image = Image.open(image_path).convert('RGB')
    film_profiles = load_config(config_path)

    # Apply each film profile
    for film_profile_name, film_profile in film_profiles.items():
        # Make a copy of the original image for each profile
        output_image = image.copy()

        # Apply chromatic aberration if specified
        if chromatic_aberration:
            print("Applying chromatic aberration")
            output_image = apply_chromatic_aberration(output_image, shift_amount)
        
        if light_leak:
            print("Applying light leak")
            output_image = add_light_leak(output_image)

        # Apply dynamic range compression if specified in the film profile
        compression_factor = film_profile.get('dynamic_range_compression', None)
        if compression_factor is not None:
            print(f"Applying dynamic range compression for {film_profile_name}")
            output_image = apply_dynamic_range_compression(output_image, compression_factor)

        # Apply tone curve per channel
        tone_curve_params = film_profile['curves']
        print(f"Applying tone curve for {film_profile_name}")
        output_image = apply_tone_curve_per_channel(output_image, tone_curve_params)

        # Apply base color shift
        base_color = film_profile.get('base_color', None)
        if base_color:
            print(f"Applying base color for {film_profile_name}")
            output_image = apply_base_color(output_image, base_color)

        # Apply exposure adjustment
        exposure = film_profile.get('exposure', 1.0)
        print("Applying exposure adjustment")
        output_image = apply_exposure_adjustment(output_image, exposure)

        # Apply color adjustments (contrast and saturation)
        color_params = {
            'contrast': film_profile['contrast'],
            'saturation': film_profile['saturation']
        }
        print("Applying color adjustments")
        output_image = apply_color_adjustments(output_image, color_params)

        # Add grain
        grain_intensity = film_profile['grain']
        print("Adding grain")
        output_image = add_grain(output_image, grain_intensity)

        # Apply vignette effect if specified
        if vignette_strength > 0:
            print("Applying vignette effect")
            output_image = apply_vignette(output_image, radius=1, strength=vignette_strength, falloff=1)

        # Save the final output image for each profile
        output_path = f"{output_dir}/{film_profile_name.replace(' ', '_').lower()}.jpg"
        output_image.save(output_path)
        print(f"Saved emulated film image for {film_profile_name} to {output_path}")
