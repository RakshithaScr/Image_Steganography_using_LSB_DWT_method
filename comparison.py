import os
import matplotlib.pyplot as plt
from PIL import Image

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


def main():
    cover_file, stego_file = find_files()

    cover_img = Image.open(cover_file).convert("RGB")
    stego_img = Image.open(stego_file).convert("RGB")

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(cover_img)
    plt.title("Cover Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(stego_img)
    plt.title("Stego Image")
    plt.axis("off")

    plt.suptitle("Cover Image vs Stego Image")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
