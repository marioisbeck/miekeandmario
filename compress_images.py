import os
import re
import argparse
from PIL import Image


def get_image_files(directory):
    # Get all image files in the directory and subdirectories
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if re.match(r".*\.(jpg|jpeg|png|gif|bmp|tiff)$", file, re.IGNORECASE):
                image_files.append(os.path.join(root, file))
    return sorted(
        image_files, key=lambda x: (tuple(map(int, re.findall(r"\d+", x))), x)
    )


def convert_to_jpg(file_path):
    img = Image.open(file_path)
    rgb_img = img.convert("RGB")
    new_file_path = os.path.splitext(file_path)[0] + ".jpg"
    rgb_img.save(
        new_file_path, "JPEG", quality=20, optimize=True
    )  # Adjusted quality for more compression
    os.remove(file_path)
    return new_file_path


def compress_image(image_path):
    img = Image.open(image_path)
    img.save(
        image_path, "JPEG", quality=20, optimize=True
    )  # Adjusted quality for more compression


def process_images(directory):
    files = get_image_files(directory)
    for file_path in files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext != ".jpg":
            file_path = convert_to_jpg(file_path)
        compress_image(file_path)
        print(f"Processed {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress and convert images to JPG.")
    parser.add_argument(
        "directory", type=str, help="Path to the directory containing images."
    )
    args = parser.parse_args()

    process_images(args.directory)
