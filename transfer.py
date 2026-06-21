import os
import sys
from PIL import Image

# =============================
# SETTINGS
# =============================

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(SCRIPT_DIR, "polytoria")

# Change to Image.NEAREST for pixel-art skins
RESAMPLE_MODE = Image.BICUBIC

SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

ROBLOX_BASE_WIDTH = 585
ROBLOX_BASE_HEIGHT = 559

POLY_BASE_WIDTH = 1024
POLY_BASE_HEIGHT = 1024

# =============================
# ROBLOX REGION DEFINITIONS
# Source template: 585x559
# =============================

ROBLOX_TORSO = {
    "front":  (231,  74, 358, 201),
    "bottom": (231, 204, 358, 267),
    "top":    (231,   8, 358,  71),
    "right":  (165,  74, 228, 201),
    "left":   (361,  74, 424, 201),
    "back":   (427,  74, 554, 201),
}

ROBLOX_RIGHT_ARM = {
    "left":  ( 19, 355,  82, 482),
    "back":  ( 85, 355, 148, 482),
    "right": (151, 355, 214, 482),
    "front": (217, 355, 280, 482),
    "up":    (217, 289, 280, 352),
    "down":  (217, 485, 280, 548),
}

ROBLOX_LEFT_ARM = {
    "left":  (374, 355, 437, 482),
    "back":  (440, 355, 503, 482),
    "right": (506, 355, 569, 482),
    "front": (308, 355, 371, 482),
    "up":    (308, 289, 371, 352),
    "down":  (308, 485, 371, 548),
}

ROBLOX_RIGHT_LEG = {
    "left":  ( 19, 355,  82, 482),
    "back":  ( 85, 355, 148, 482),
    "right": (151, 355, 214, 482),
    "front": (217, 355, 280, 482),
    "up":    (217, 289, 280, 352),
    "down":  (217, 485, 280, 548),
}

ROBLOX_LEFT_LEG = {
    "left":  (374, 355, 437, 482),
    "back":  (440, 355, 503, 482),
    "right": (506, 355, 569, 482),
    "front": (308, 355, 371, 482),
    "up":    (308, 289, 371, 352),
    "down":  (308, 485, 371, 548),
}

# =============================
# POLYTORIA REGION DEFINITIONS
# Base layout: 1024x1024
# =============================

POLY_TORSO = {
    "front":  (439, 103, 584, 392),
    "bottom": (439, 393, 584, 488),
    "top":    (439,   7, 584, 102),
    "right":  (351, 103, 438, 392),
    "left":   (585, 103, 672, 392),
    "back":   (439, 519, 584, 808),
}

POLY_RIGHT_ARM = {
    "left":  (  6,  71,  71, 360),
    "back":  ( 72,  71, 137, 360),
    "right": (138,  71, 203, 360),
    "front": (204,  71, 269, 360),
    "up":    (204,   7, 269,  70),
    "down":  (204, 361, 269, 424),
}

POLY_LEFT_ARM = {
    "front": (754,  71, 819, 360),
    "left":  (820,  71, 885, 360),
    "back":  (886,  71, 951, 360),
    "right": (952,  71, 1017, 360),
    "up":    (754,   7, 819,  70),
    "down":  (754, 361, 819, 424),
}

POLY_RIGHT_LEG = {
    "left":  ( 14, 661,  77, 952),
    "back":  ( 78, 661, 141, 952),
    "right": (142, 661, 205, 952),
    "front": (206, 661, 269, 952),
    "up":    (206, 597, 269, 660),
    "down":  (206, 953, 269, 1016),
}

POLY_LEFT_LEG = {
    "front": (754, 661, 817, 952),
    "left":  (818, 661, 881, 952),
    "back":  (882, 661, 945, 952),
    "right": (946, 661, 1009, 952),
    "up":    (754, 597, 817, 660),
    "down":  (754, 953, 817, 1016),
}

# =============================
# HELP TEXT
# =============================

USAGE = """\
Roblox → Polytoria Clothing Converter

Ways to use:

1. Drag a folder named "shirts" onto this program
   - Every supported image inside is converted as a shirt.
   - Output goes to:
     polytoria/shirts/

2. Drag a folder named "pants" onto this program
   - Every supported image inside is converted as pants.
   - Output goes to:
     polytoria/pants/

3. Command-line/manual mode:
   python convert.py shirt file1.png file2.png
   python convert.py pants file1.png file2.png

4. Mixed drag-and-drop batch:
   You can drag both "shirts" and "pants" folders at once.

Supported input formats:
  .png, .jpg, .jpeg, .webp

HD Roblox templates are supported:
  585x559       -> 1024x1024 output
  1170x1118     -> 2048x2048 output
  2340x2236     -> 4096x4096 output
  4680x4472     -> 8192x8192 output

Output is saved next to this program in:
  polytoria/shirts/
  polytoria/pants/
"""

# =============================
# UTIL
# =============================

def pause_if_double_clicked():
    """
    Keeps the console window open when double-clicked on Windows.
    """
    if os.name == "nt":
        input("\nPress Enter to close...")


def normalize_clothing_type(name):
    name = name.lower().strip()

    if name in ("shirt", "shirts"):
        return "shirt"

    if name in ("pants", "pant"):
        return "pants"

    return None


def output_subfolder_name(clothing_type):
    if clothing_type == "shirt":
        return "shirts"

    if clothing_type == "pants":
        return "pants"

    return clothing_type


def is_supported_image(path):
    ext = os.path.splitext(path)[1].lower()
    return ext in SUPPORTED_EXTS


def scale_box(box, scale_x, scale_y):
    x1, y1, x2, y2 = box

    return (
        round(x1 * scale_x),
        round(y1 * scale_y),
        round(x2 * scale_x),
        round(y2 * scale_y),
    )


def clamp_box(box, width, height):
    x1, y1, x2, y2 = box

    return (
        max(0, min(width, x1)),
        max(0, min(height, y1)),
        max(0, min(width, x2)),
        max(0, min(height, y2)),
    )


def detect_scale(src_width, src_height):
    src_scale_x = src_width / ROBLOX_BASE_WIDTH
    src_scale_y = src_height / ROBLOX_BASE_HEIGHT

    output_scale = (src_scale_x + src_scale_y) / 2

    return src_scale_x, src_scale_y, output_scale


def transfer_regions(
    src_img,
    dst_img,
    src_map,
    dst_map,
    src_scale_x,
    src_scale_y,
    dst_scale,
    pad=1
):
    for key in src_map:
        if key not in dst_map:
            continue

        src_box = scale_box(src_map[key], src_scale_x, src_scale_y)
        src_box = clamp_box(src_box, src_img.width, src_img.height)

        dst_box = scale_box(dst_map[key], dst_scale, dst_scale)
        x1, y1, x2, y2 = dst_box

        scaled_pad = max(1, round(pad * dst_scale))

        dx1 = max(0, x1 - scaled_pad)
        dy1 = max(0, y1 - scaled_pad)
        dx2 = min(dst_img.width,  x2 + scaled_pad)
        dy2 = min(dst_img.height, y2 + scaled_pad)

        cropped = src_img.crop(src_box)
        resized = cropped.resize((dx2 - dx1, dy2 - dy1), RESAMPLE_MODE)

        dst_img.paste(resized, (dx1, dy1), resized)


def collect_jobs_from_folder(folder_path):
    """
    If a dragged folder is named shirts or pants, convert every supported image
    inside it as that clothing type.

    This scans recursively, so nested folders work too.
    """
    folder_name = os.path.basename(os.path.normpath(folder_path))
    clothing_type = normalize_clothing_type(folder_name)

    if clothing_type is None:
        print(f"Skipping folder with unknown type: {folder_path}")
        print("Folder must be named 'shirts' or 'pants'.")
        return []

    jobs = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            full_path = os.path.join(root, filename)

            if is_supported_image(full_path):
                jobs.append((clothing_type, full_path))

    return jobs


def collect_jobs(args):
    """
    Supports:
      convert.py shirt file1 file2
      convert.py pants file1 file2
      convert.py shirts_folder pants_folder
      convert.py shirt file1 pants file2
    """
    jobs = []
    current_type = None

    for arg in args:
        possible_type = normalize_clothing_type(arg)

        if possible_type is not None:
            current_type = possible_type
            continue

        if os.path.isdir(arg):
            folder_jobs = collect_jobs_from_folder(arg)
            jobs.extend(folder_jobs)
            continue

        if os.path.isfile(arg):
            if not is_supported_image(arg):
                print(f"Skipping unsupported file: {arg}")
                continue

            if current_type is None:
                print(f"Skipping file without clothing type: {arg}")
                print("Put files inside a folder named 'shirts' or 'pants', or use:")
                print("  python convert.py shirt file.png")
                print("  python convert.py pants file.png")
                continue

            jobs.append((current_type, arg))
            continue

        print(f"Skipping unknown path/argument: {arg}")

    return jobs


def convert_one(clothing_type, in_path, first_in_batch=False):
    filename = os.path.basename(in_path)
    base_name, _ = os.path.splitext(filename)

    out_folder = os.path.join(OUTPUT_DIR, output_subfolder_name(clothing_type))
    os.makedirs(out_folder, exist_ok=True)

    out_filename = base_name + ".png"
    out_path = os.path.join(out_folder, out_filename)

    try:
        roblox_img = Image.open(in_path).convert("RGBA")
    except Exception as e:
        print(f"Failed to open {filename}: {e}")
        return False

    src_scale_x, src_scale_y, output_scale = detect_scale(
        roblox_img.width,
        roblox_img.height
    )

    poly_width = round(POLY_BASE_WIDTH * output_scale)
    poly_height = round(POLY_BASE_HEIGHT * output_scale)

    if first_in_batch:
        print(USAGE)
        print("Starting batch conversion...\n")

    print(
        f"Converting {filename} as {clothing_type}: "
        f"Roblox {roblox_img.width}x{roblox_img.height} "
        f"→ Polytoria {poly_width}x{poly_height} "
        f"scale={output_scale:.2f}x"
    )

    polytoria_img = Image.new(
        "RGBA",
        (poly_width, poly_height),
        (0, 0, 0, 0)
    )

    if clothing_type == "shirt":
        transfer_regions(
            roblox_img,
            polytoria_img,
            ROBLOX_TORSO,
            POLY_TORSO,
            src_scale_x,
            src_scale_y,
            output_scale
        )

        transfer_regions(
            roblox_img,
            polytoria_img,
            ROBLOX_RIGHT_ARM,
            POLY_RIGHT_ARM,
            src_scale_x,
            src_scale_y,
            output_scale
        )

        transfer_regions(
            roblox_img,
            polytoria_img,
            ROBLOX_LEFT_ARM,
            POLY_LEFT_ARM,
            src_scale_x,
            src_scale_y,
            output_scale
        )

    elif clothing_type == "pants":
        transfer_regions(
            roblox_img,
            polytoria_img,
            ROBLOX_TORSO,
            POLY_TORSO,
            src_scale_x,
            src_scale_y,
            output_scale
        )

        transfer_regions(
            roblox_img,
            polytoria_img,
            ROBLOX_RIGHT_LEG,
            POLY_RIGHT_LEG,
            src_scale_x,
            src_scale_y,
            output_scale
        )

        transfer_regions(
            roblox_img,
            polytoria_img,
            ROBLOX_LEFT_LEG,
            POLY_LEFT_LEG,
            src_scale_x,
            src_scale_y,
            output_scale
        )

    else:
        print(f"Unknown clothing type: {clothing_type}")
        return False

    polytoria_img.save(out_path)
    print(f"Converted → {os.path.relpath(out_path, SCRIPT_DIR)}")

    return True


# =============================
# MAIN
# =============================

def main():
    if len(sys.argv) < 2:
        print(USAGE)
        pause_if_double_clicked()
        return

    jobs = collect_jobs(sys.argv[1:])

    if not jobs:
        print(USAGE)
        print("\nNo valid clothing files found.")
        pause_if_double_clicked()
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(jobs)
    converted = 0

    for index, (clothing_type, in_path) in enumerate(jobs):
        first_in_batch = index == 0

        if convert_one(clothing_type, in_path, first_in_batch=first_in_batch):
            converted += 1

    print(f"\nDone. Converted {converted}/{total} file(s).")

    # This only really matters when launched by drag/drop or double-click on Windows.
    pause_if_double_clicked()


if __name__ == "__main__":
    main()