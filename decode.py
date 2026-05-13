import numpy as np
from PIL import Image
import pywt
import os

SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")


def find_stego_file():
    """Find the stego image in the folder."""
    for ext in SUPPORTED_FORMATS:
        file = f"stego_cvimage11{ext}"
        if os.path.exists(file):
            return file
    raise FileNotFoundError("Stego image not found.")


def bits_to_bytes(bits):
    """Convert list of bits to bytes."""
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
            else:
                byte <<= 1
        data.append(byte)
    return bytes(data)


def extract_lsb_channel(channel):
    """Extract secret message bits from red channel LSB."""
    flat = channel.flatten()

    # Read first 32 bits to get message length
    length_bits = [int(flat[i] & 1) for i in range(32)]
    length = 0
    for bit in length_bits:
        length = (length << 1) | bit

    # Convert to Python int explicitly (prevents overflow)
    length = int(length)

    # Sanity check
    if length <= 0 or length > 1000000:  # max 1 million chars
        raise ValueError("Invalid message length detected. Check embedding or cover image.")

    total_bits = length * 8
    message_bits = [int(flat[i] & 1) for i in range(32, 32 + total_bits)]
    return message_bits


def main():
    stego_file = find_stego_file()
    stego_img = Image.open(stego_file).convert("RGB")
    stego_array = np.array(stego_img)

    r = stego_array[:, :, 0]

    # Apply DWT + IDWT
    coeffs = pywt.dwt2(r, "haar")
    r_rec = pywt.idwt2(coeffs, "haar")
    r_rec = np.uint8(np.clip(np.round(r_rec), 0, 255))

    try:
        message_bits = extract_lsb_channel(r_rec)
        message_bytes = bits_to_bytes(message_bits)
        secret_message = message_bytes.decode("utf-8")
    except Exception as e:
        print("Error extracting message:", e)
        return

    password = input("Enter password to reveal secret message: ")
    if password == "1234":
        print("\nSecret Message:")
        print(secret_message)
    else:
        print("Incorrect password. Access denied.")


if __name__ == "__main__":
    main()
