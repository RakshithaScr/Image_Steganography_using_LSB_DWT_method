import numpy as np
from PIL import Image
import pywt
import os

SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")


def find_cover_file():
    for ext in SUPPORTED_FORMATS:
        file = f"cvimage11{ext}"
        if os.path.exists(file):
            return file
    raise FileNotFoundError("Cover image cvimage11 not found.")


def message_to_bits(message):
    bits = []
    for char in message.encode("utf-8"):
        for i in range(8):
            bits.append((char >> (7 - i)) & 1)
    return bits


def embed_lsb_channel(channel, message_bits):
    flat = channel.flatten()
    if len(message_bits) > len(flat):
        raise ValueError("Message too large for this image.")
    for i, bit in enumerate(message_bits):
        flat[i] = (flat[i] & 0xFE) | bit
    return flat.reshape(channel.shape)


def embed_message_in_image(img_array, full_message_bits):
    r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]

    # Embed message in Red channel using LSB
    r_embedded = embed_lsb_channel(r, full_message_bits)

    # Apply DWT and IDWT
    r_coeffs = pywt.dwt2(r_embedded, "haar")
    g_coeffs = pywt.dwt2(g, "haar")
    b_coeffs = pywt.dwt2(b, "haar")

    r_rec = pywt.idwt2(r_coeffs, "haar")
    g_rec = pywt.idwt2(g_coeffs, "haar")
    b_rec = pywt.idwt2(b_coeffs, "haar")

    r_rec = np.uint8(np.clip(np.round(r_rec), 0, 255))
    g_rec = np.uint8(np.clip(np.round(g_rec), 0, 255))
    b_rec = np.uint8(np.clip(np.round(b_rec), 0, 255))

    return np.stack((r_rec, g_rec, b_rec), axis=2)


def main():
    cover_file = find_cover_file()
    img = Image.open(cover_file).convert("RGB")
    img_array = np.array(img)

    with open("smmessage.txt", "r", encoding="utf-8") as f:
        secret_message = f.read().strip()

    message_length = len(secret_message)
    length_bits = [(message_length >> (31 - i)) & 1 for i in range(32)]
    message_bits = message_to_bits(secret_message)

    full_message_bits = length_bits + message_bits

    stego_array = embed_message_in_image(img_array, full_message_bits)
    stego_img = Image.fromarray(stego_array)

    name, ext = os.path.splitext(cover_file)
    stego_img.save(f"stego_cvimage11{ext}")

    print("Embedding complete. Stego image created successfully.")


if __name__ == "__main__":
    main()
