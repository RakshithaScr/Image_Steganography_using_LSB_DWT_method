import numpy as np
from PIL import Image
import os

SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")


def find_files():
    """Find cover and stego images."""
    cover_file = stego_file = None
    for ext in SUPPORTED_FORMATS:
        if os.path.exists(f"cvimage11{ext}"):
            cover_file = f"cvimage11{ext}"
        if os.path.exists(f"stego_cvimage11{ext}"):
            stego_file = f"stego_cvimage11{ext}"
    if not cover_file:
        raise FileNotFoundError("Cover image not found (cvimage11).")
    if not stego_file:
        raise FileNotFoundError("Stego image not found (stego_cvimage11).")
    return cover_file, stego_file


def calculate_mse(original, stego):
    """Calculate Mean Squared Error between two images."""
    original = original.astype(np.float64)
    stego = stego.astype(np.float64)
    diff = original - stego
    mse = np.mean(diff ** 2)
    return mse


def calculate_psnr(mse, max_pixel=255.0):
    """Calculate PSNR from MSE."""
    if mse == 0:
        return float("inf")
    return 20 * np.log10(max_pixel / np.sqrt(mse))


def main():
    cover_file, stego_file = find_files()

    cover_img = np.array(Image.open(cover_file).convert("RGB"))
    stego_img = np.array(Image.open(stego_file).convert("RGB"))

    # Resize stego if dimensions mismatch
    if cover_img.shape != stego_img.shape:
        stego_img = np.array(Image.fromarray(stego_img).resize(
            (cover_img.shape[1], cover_img.shape[0])
        ))

    mse = calculate_mse(cover_img, stego_img)
    psnr = calculate_psnr(mse)

    # Save results in a text file
    with open("calculation.txt", "w") as f:
        f.write("----- MSE & PSNR Calculation -----\n")
        f.write(f"Image Dimensions: {cover_img.shape}\n")
        f.write(f"MSE  = {mse:.6f}\n")
        f.write(f"PSNR = {psnr:.2f} dB\n")
        f.write("--------------------------------\n")

    print(f"MSE  : {mse:.6f}")
    print(f"PSNR : {psnr:.2f} dB")


if __name__ == "__main__":
    main()
