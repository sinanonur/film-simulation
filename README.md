# Film Simulation Script

This Python script applies various film simulation profiles to digital images, allowing you to emulate the look of popular film stocks. It supports both sequential and parallel processing, and allows for custom film profiles through JSON configuration.

## Features

- Apply multiple film profiles to a single image
- Adjustable color curves, contrast, saturation, chromatic aberration, and blur
- Film grain simulation
- Color temperature adjustment
- Cross-processing effect
- Optional parallel processing for improved performance
- Custom film profiles via JSON configuration

## Examples

| Original Image                      | Kodak Portra 400                  | Fuji Superia 400                    |
|-------------------------------------|-----------------------------------|-------------------------------------|
| ![Original](examples/picture.jpg)   | ![Kodak Portra 400](examples/picture_Kodak_Portra_400.jpg) | ![Fuji Superia 400](examples/picture_Fuji_Superia_400.jpg) |

| Ilford HP5 Plus 400                 | Kodak Ektar 100                   | Kodachrome 64                       |
|-------------------------------------|-----------------------------------|-------------------------------------|
| ![Ilford HP5 Plus 400](examples/picture_Ilford_HP5_Plus_400.jpg) | ![Kodak Ektar 100](examples/picture_Kodak_Ektar_100.jpg) | ![Kodachrome 64](examples/picture_Kodachrome_64.jpg) |

| Fujifilm Velvia 50                  |                                   |                                     |
|-------------------------------------|-----------------------------------|-------------------------------------|
| ![Fujifilm Velvia 50](examples/picture_Fujifilm_Velvia_50.jpg)    |                                   |                                     |


## Requirements

- Python 3.6+
- Required Python packages:
  - numpy
  - Pillow
  - colour-science
  - psutil
  - scipy
  - piexif

You can install the required packages using pip:

```
pip install numpy Pillow colour-science psutil scipy piexif
```

## Usage

Basic usage:

```
python film_simulation.py input_image.jpg --profiles film_profiles.json
```

With parallel processing:

```
python film_simulation.py input_image.jpg --profiles film_profiles.json --parallel
```

### Command-line Arguments

- `input_image`: Path to the input image (required)
- `--profiles`: Path to JSON file containing film profiles (required)
- `--chroma`: Override chromatic aberration strength
- `--blur`: Override blur amount
- `--color_temp`: Color temperature (default: 6500K)
- `--cross_process`: Apply cross-processing effect
- `--parallel`: Enable parallel processing

### Examples

1. Process an image with default settings:
   ```
   python film_simulation.py my_photo.jpg --profiles default_profiles.json
   ```

2. Process an image with parallel processing and custom color temperature:
   ```
   python film_simulation.py my_photo.jpg --profiles custom_profiles.json --parallel --color_temp 5500
   ```

3. Apply cross-processing effect:
   ```
   python film_simulation.py my_photo.jpg --profiles film_profiles.json --cross_process
   ```

## Custom Film Profiles

You can create custom film profiles by modifying the JSON file. Here's an example structure:

```json
{
  "My Custom Film": {
    "color_curves": {
      "R": {"x": [0, 0.25, 0.5, 0.75, 1], "y": [0, 0.27, 0.53, 0.77, 1]},
      "G": {"x": [0, 0.25, 0.5, 0.75, 1], "y": [0, 0.25, 0.5, 0.75, 1]},
      "B": {"x": [0, 0.25, 0.5, 0.75, 1], "y": [0, 0.23, 0.47, 0.73, 1]}
    },
    "contrast": 1.1,
    "saturation": 0.9,
    "chromatic_aberration": 0.2,
    "blur": 0.1,
    "base_color": [255, 250, 245],
    "grain_amount": 0.03,
    "grain_size": 1
  }
}
```

You can include multiple film profiles in a single JSON file.

## Output

The script will generate one output image for each film profile in the JSON file. Output images will be saved in the same directory as the input image, with the film profile name appended to the original filename.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/film-simulation/issues) if you want to contribute.

## Author

[Sinan Onur Altınuç]

