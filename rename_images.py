import os
import re
from PIL import Image
from moviepy.editor import ImageSequenceClip, AudioFileClip


def get_image_files(directory):
    # Get all jpg and png files in the directory
    files = [
        f
        for f in os.listdir(directory)
        if re.match(r".*\.(jpg|png)$", f, re.IGNORECASE)
    ]
    return sorted(
        files,
        key=lambda x: (
            tuple(map(int, re.findall(r"\d+", x))),
            x,
        ),
    )


def convert_png_to_jpg(file_path):
    img = Image.open(file_path)
    rgb_img = img.convert("RGB")
    new_file_path = os.path.splitext(file_path)[0] + ".jpg"
    rgb_img.save(new_file_path, "JPEG", quality=85, optimize=True)
    os.remove(file_path)
    return new_file_path


def crop_image(image_path, size):
    img = Image.open(image_path)
    img_ratio = img.width / img.height
    target_ratio = size[0] / size[1]

    if img_ratio > target_ratio:
        # Image is wider than target aspect ratio
        new_width = int(target_ratio * img.height)
        offset = (img.width - new_width) // 2
        crop_box = (offset, 0, offset + new_width, img.height)
    else:
        # Image is taller than target aspect ratio
        new_height = int(img.width / target_ratio)
        offset = (img.height - new_height) // 2
        crop_box = (0, offset, img.width, offset + new_height)

    img = img.crop(crop_box).resize(size, Image.LANCZOS)
    img.save(image_path, "JPEG", quality=85, optimize=True)


def convert_all_pngs(directory):
    files = get_image_files(directory)
    for filename in files:
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".png":
            old_path = os.path.join(directory, filename)
            convert_png_to_jpg(old_path)


def rename_images(directory):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    # Convert all PNG files to JPG first
    convert_all_pngs(directory)

    files = get_image_files(directory)

    # First pass: Rename to new__<image-number>.ext
    for index, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[1].lower()
        new_name = f"new__{index}.jpg"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)

        print(f"Renamed {old_path} to {new_path}")

    # Second pass: Rename to <image-number>.ext
    new_files = get_image_files(directory)
    for filename in new_files:
        if filename.startswith("new__"):
            new_name = filename.replace("new__", "")
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed {old_path} to {new_path}")

    # Create a slideshow video
    create_slideshow(directory)


def create_slideshow(directory):
    image_files = get_image_files(directory)
    image_paths = [os.path.join(directory, f) for f in image_files]

    # Crop images to the same size
    common_size = (800, 600)  # You can change this to your desired size
    for image_path in image_paths:
        crop_image(image_path, common_size)

    # Calculate duration per image
    total_duration = 234  # 3 minutes and 54 seconds
    num_images = len(image_paths)
    duration_per_image = total_duration / num_images

    # Create a video clip from the images
    clip = ImageSequenceClip(image_paths, durations=[duration_per_image] * num_images)
    clip.fps = 1 / duration_per_image  # Set the fps attribute

    # Add background music
    audio_path = "/Users/mario/programming/wedding/miekemario/Last_Love.mp3"
    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio)

    # Save the video clip with a compatible audio codec
    video_path = os.path.join(directory, "slideshow.mp4")
    clip.write_videofile(video_path, codec="libx264", audio_codec="aac")
    print(f"Slideshow video saved to {video_path}")


if __name__ == "__main__":
    directory = "./0d0b4267be8885ac8aae5358dab94d6da880d184/images/wedding_pics"  # Change this to your directory
    rename_images(directory)
