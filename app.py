import gradio as gr
from PIL import Image
from film_simulation import process_images

def gradio_interface(image, profiles_json, chroma_override, blur_override, color_temp, cross_process_flag, curve_type):
    image = Image.open(image)
    profiles_json_path = profiles_json.name
    processed_images = process_images(image, profiles_json_path, chroma_override, blur_override, color_temp, cross_process_flag, curve_type)
    return processed_images

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.inputs.Image(type="file", label="Input Image"),
        gr.inputs.File(label="Profiles JSON"),
        gr.inputs.Slider(0, 10, step=0.1, default=None, label="Chromatic Aberration Override"),
        gr.inputs.Slider(0, 10, step=0.1, default=None, label="Blur Override"),
        gr.inputs.Slider(1000, 10000, step=100, default=6500, label="Color Temperature (K)"),
        gr.inputs.Checkbox(label="Cross Process"),
        gr.inputs.Dropdown(choices=["color", "advanced", "both", "auto"], default="auto", label="Curve Type"),
    ],
    outputs=[
        gr.outputs.Image(type="pil", label="Processed Image 1"),
        gr.outputs.Image(type="pil", label="Processed Image 2"),
        gr.outputs.Image(type="pil", label="Processed Image 3"),
        gr.outputs.Image(type="pil", label="Processed Image 4"),
        gr.outputs.Image(type="pil", label="Processed Image 5"),
        gr.outputs.Image(type="pil", label="Processed Image 6"),
        gr.outputs.Image(type="pil", label="Processed Image 7"),
        gr.outputs.Image(type="pil", label="Processed Image 8"),
        gr.outputs.Image(type="pil", label="Processed Image 9"),
        gr.outputs.Image(type="pil", label="Processed Image 10"),
        gr.outputs.Image(type="pil", label="Processed Image 11"),
        gr.outputs.Image(type="pil", label="Processed Image 12"),
    ],
    title="Film Simulation",
    description="Upload an image and a JSON file with film profiles to apply different film simulations."
)

iface.launch()
