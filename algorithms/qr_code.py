import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image
import io, base64

def generate_qr(
    data: str,
    version: int = None,
    error_correction: str = "M",
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
    logo_path: str = None,
    logo_size: int = 100,
    file_format: str = "png",
    output_path: str = "qr_code.png",
    return_image: bool = False,
    return_base64: bool = False
):
    # Map error correction
    ec_levels = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q, "H": ERROR_CORRECT_H}
    
    qr = qrcode.QRCode(
        version=version,
        error_correction=ec_levels.get(error_correction.upper(), ERROR_CORRECT_M),
        box_size=box_size,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")
    
    # Add logo if provided
    if logo_path:
        logo = Image.open(logo_path)
        logo = logo.resize((logo_size, logo_size))
        pos = ((img.size[0] - logo.size[0]) // 2,
               (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)
    
    # Save file
    img.save(output_path, format=file_format.upper())
    
    results = {"file_path": output_path}
    
    if return_image:
        results["image_obj"] = img
    
    if return_base64:
        buffer = io.BytesIO()
        img.save(buffer, format=file_format.upper())
        base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        results["base64"] = base64_str
    
    return results

# Main Execution
if __name__ == "__main__":
    qr_data = "Hello World from QR Code Generator!"
    qr_code = generate_qr(
        data=qr_data,
        version=1,
        error_correction="H",
        box_size=10,
        border=4,
        fill_color="black",
        back_color="white",
        logo_path=None,  # Provide path to logo if needed
        logo_size=100,
        file_format="png",
        output_path="example_qr.png",
        return_image=True,
        return_base64=True
    )
    print("QR Code generated and saved to:", qr_code["file_path"])
    if "base64" in qr_code:
        print("Base64 Representation:", qr_code["base64"][:50] + "...")  # 