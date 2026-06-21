import os
import sys
from PIL import Image

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(BASE_DIR, "polytoria")


# Change to Image.NEAREST for pixel-art skins
RESAMPLE_MODE = Image.BICUBIC

SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

# =============================
# REGION DEFINITIONS
# =============================

ROBLOX_TORSO = {
    "front":  (231, 74, 358, 201),
    "bottom": (231, 204, 358, 267),
    "top":    (231, 8, 358, 71),
    "right":  (165, 74, 228, 201),
    "left":   (361, 74, 424, 201),
    "back":   (427, 74, 554, 201),
}

POLY_TORSO = {
    "front":  (199, 184, 398, 383),
    "bottom": (199, 394, 398, 493),
    "top":    (199, 74, 398, 173),
    "right":  (89, 184, 188, 383),
    "left":   (409, 184, 508, 383),
    "back":   (519, 184, 718, 383),
}

ROBLOX_RIGHT_ARM = {
    "left":  (19, 355, 82, 482),
    "back":  (85, 355, 148, 482),
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

POLY_LEFT_ARM = {
    "left":  (52, 667, 151, 866),
    "back":  (162, 667, 261, 866),
    "right": (272, 667, 371, 866),
    "front": (382, 667, 481, 866),
    "up":    (382, 557, 481, 656),
    "down":  (382, 887, 481, 976),
}

POLY_RIGHT_ARM = {
    "left":  (649, 667, 748, 866),
    "back":  (759, 667, 858, 866),
    "right": (870, 667, 969, 866),
    "front": (538, 667, 637, 866),
    "up":    (538, 557, 637, 656),
    "down":  (538, 877, 637, 976),
}

# =============================
# UTIL
# =============================

def transfer_regions(src_img, dst_img, src_map, dst_map, pad=1):
    for key in src_map:
        src_box = src_map[key]
        x1, y1, x2, y2 = dst_map[key]

        dx1 = max(0, x1 - pad)
        dy1 = max(0, y1 - pad)
        dx2 = min(dst_img.width,  x2 + pad)
        dy2 = min(dst_img.height, y2 + pad)

        cropped = src_img.crop(src_box)
        resized = cropped.resize((dx2 - dx1, dy2 - dy1), RESAMPLE_MODE)
        dst_img.paste(resized, (dx1, dy1), resized)

# =============================
# MAIN
# =============================

def main():
    if len(sys.argv) < 2:
        print("Drag and drop the textures for conversion!")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for in_path in sys.argv[1:]:
        ext = os.path.splitext(in_path)[1].lower()
        if ext not in SUPPORTED_EXTS:
            print(f"Skipping unsupported file: {in_path}")
            continue

        filename = os.path.basename(in_path)
        out_path = os.path.join(OUTPUT_DIR, filename)

        try:
            roblox_img = Image.open(in_path).convert("RGBA")
        except Exception as e:
            print(f"Failed to open {filename}: {e}")
            continue

        polytoria_img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))

        transfer_regions(roblox_img, polytoria_img, ROBLOX_TORSO, POLY_TORSO)
        transfer_regions(roblox_img, polytoria_img, ROBLOX_RIGHT_ARM, POLY_RIGHT_ARM)
        transfer_regions(roblox_img, polytoria_img, ROBLOX_LEFT_ARM, POLY_LEFT_ARM)

        polytoria_img.save(out_path)
        print(f"Converted → polytoria/{filename}")

    print("Done.")

if __name__ == "__main__":
    main()
