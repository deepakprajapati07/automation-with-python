import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io, base64

def generate_barcode(
    data: str,
    barcode_type: str = "code128",
    output_path: str = "barcode.png",
    file_format: str = "png",
    module_width: float = 0.25,
    module_height: float = 10.0,
    font_size: int = 10,
    text_distance: float = 4.0,
    background: str = "white",
    foreground: str = "black",
    write_text: bool = True,
    return_image: bool = False,
    return_base64: bool = False
):
    writer = ImageWriter()
    options = {
        "module_width": module_width,
        "module_height": module_height,
        "font_size": font_size,
        "text_distance": text_distance,
        "background": background,
        "foreground": foreground,
        "write_text": write_text,
    }
    
    # Generate barcode
    bc = barcode.get(barcode_type, data, writer=writer)
    filename = bc.save(output_path.replace("." + file_format, ""), options)
    
    results = {"file_path": filename}
    
    # Return PIL image
    if return_image or return_base64:
        img = Image.open(filename)
        if return_image:
            results["image_obj"] = img
        if return_base64:
            buffer = io.BytesIO()
            img.save(buffer, format=file_format.upper())
            results["base64"] = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return results

# Main Execution
if __name__ == "__main__":
    result = generate_barcode(
        data="123456789012",
        barcode_type="code128",
        output_path="barcode.png",
        file_format="png",
        return_image=True,
        return_base64=True
    )
    print("Barcode saved to:", result["file_path"])
    if "image_obj" in result:
        result["image_obj"].show()
    if "base64" in result:
        print("Base64 String:", result["base64"][:50] + "...")  # Print first 50 chars of base64 string

"""
    Summary:
    This script generates a barcode from the given data and saves it as an image file.
    It supports various barcode types and customization options for appearance.
    Additionally, it can return the barcode as a PIL image object or a base64-encoded string.
    Key features:
    - Supports multiple barcode formats (e.g., Code128, EAN, etc.)
    - Customizable appearance (size, colors, text)
    - Option to return image as PIL object or base64 string for further use in applications.
    Core flow:
        Input data & options → generate barcode → save image → optionally return image/base64.
    Dependencies:
    - python-barcode
    - Pillow
    - io, base64
"""