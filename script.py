import os
from PIL import Image

# --- Config ---
INPUT_FOLDER = "input-images"
OUTPUT_FOLDER = "output"
TARGET_SIZE = 1600                # Resize target: width or height
FIXED_QUALITY = 70                # JPEG output quality
BOTTOM_OFFSET = 105               # Watermark distance from bottom

# --- Load watermark images (with transparency preserved) ---
wm_landscape = Image.open("landscape-watermark.png").convert("RGBA")
wm_portrait = Image.open("portrait-watermark.png").convert("RGBA")

# --- Prepare output folder ---
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# --- Check for valid images in input folder ---
valid_extensions = (".jpg", ".jpeg", ".png")
input_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(valid_extensions)]

if not input_files:
    print(f"⚠️  No images found in '{INPUT_FOLDER}' folder. Please add some .jpg/.png images.")
    exit()

# --- Process each image ---
for filename in input_files:
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(
        OUTPUT_FOLDER, os.path.splitext(filename)[0] + ".jpg"
    )

    # Load input image
    img = Image.open(input_path)
    orig_w, orig_h = img.size

    # Detect orientation and select watermark
    if orig_h > orig_w:
        orientation = "portrait"
        new_h = TARGET_SIZE
        new_w = int((TARGET_SIZE / orig_h) * orig_w)
        watermark = wm_portrait
    else:
        orientation = "landscape"
        new_w = TARGET_SIZE
        new_h = int((TARGET_SIZE / orig_w) * orig_h)
        watermark = wm_landscape

    # Resize input image
    img = img.resize((new_w, new_h), Image.LANCZOS)
    img_w, img_h = img.size
    print(f"🔧 Resized {filename} to {img_w}x{img_h} ({orientation})")

    # Position watermark: centered horizontally, 105px from bottom
    wm_w, wm_h = watermark.size
    x = (img_w - wm_w) // 2
    y = img_h - wm_h - BOTTOM_OFFSET

    # Prepare image with watermark
    img_rgba = img.convert("RGBA")
    img_with_wm = img_rgba.copy()

    # Paste watermark using its alpha channel
    img_with_wm.paste(watermark, (x, y), watermark)

    # Convert back to RGB and save as JPG
    final_img = img_with_wm.convert("RGB")
    final_img.save(output_path, format="JPEG", quality=FIXED_QUALITY)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ Saved: {output_path} (quality={FIXED_QUALITY}, size={size_kb:.1f}KB)")
