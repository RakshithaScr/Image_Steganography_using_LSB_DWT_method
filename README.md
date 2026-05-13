# Image Steganography using LSB + DWT 

This project is about hiding a secret message inside an image using steganography techniques. It uses LSB (Least Significant Bit) and DWT (Discrete Wavelet Transform) for better security and image quality, and calculates the MSE and PSNR metrics.

---

## Files in this project

```bash
encode.py                 - Used to hide secret message inside the image
decode.py                 - Used to extract the hidden message from stego image
comparison.py            - Shows original image and stego image side by side
calculate_mme_psnr.py    - Calculates image quality using MSE and PSNR
smmessage.txt            - File where secret message is written
cvimage.png              - Original input image
cvimage11.bmp            - Cover image used for embedding
stego_cvimage11.bmp      - Output image after hiding message
calculation.txt          - Stores MSE and PSNR results
```

---

## Requirements

Install required libraries:

```bash
pip install numpy pillow pywavelets matplotlib
```

## Important (Before Running)

Make sure these two files are present in the same folder before running the program:

- `smmessage.txt` → contains the secret message
- `cvimage11.bmp` → cover image used for hiding the message
---

## How to run

### 1. Write message
Put your secret message in:
```
smmessage.txt
```


### 2. Encode (hide message)

```bash
python encode.py
```

Output:
- stego_cvimage11.bmp (image with hidden message)

---

### 3. Decode (get message back)

```bash
python decode.py
```

Output:
- Displays the hidden message in terminal

---

### 4. Compare images

```bash
python comparison.py
```

Output:
- Shows original image and stego image side by side

---

### 5. Check image quality

```bash
python calculate_mme_psnr.py
```

Output:
- MSE and PSNR values
- saved in calculation.txt

---

## Output files generated

- stego_cvimage11.bmp → final stego image
- calculation.txt → quality results

---

## About the project

This project hides data inside images in a way that is not visible to the human eye. It is useful for secure communication and basic data hiding techniques.

---

## Author

Your Name
