import os
import re
import json


def get_sorted_files(directory, pattern):
    files = []
    for file in os.listdir(directory):
        if re.match(pattern, file, re.IGNORECASE):
            files.append(file)
    return sorted(files, key=lambda x: (tuple(map(int, re.findall(r"\d+", x))), x))


def generate_media_files(images_dir, videos_dir):
    image_pattern = r".*\.(jpg|jpeg|png|gif)$"
    video_pattern = r".*\.(mp4|avi|mov|wmv|flv|mkv|webm)$"

    images = get_sorted_files(images_dir, image_pattern)
    videos = get_sorted_files(videos_dir, video_pattern)

    media_files = []

    image_index = 0
    video_index = 0

    while image_index < len(images) or video_index < len(videos):
        if image_index < len(images):
            image_number = int(re.findall(r"\d+", images[image_index])[0])
        else:
            image_number = float("inf")

        if video_index < len(videos):
            video_number = float(re.findall(r"\d+\.\d+", videos[video_index])[0])
        else:
            video_number = float("inf")

        if image_number < video_number:
            media_files.append(
                {"type": "image", "src": f"{images_dir}/{images[image_index]}"}
            )
            image_index += 1
        else:
            media_files.append(
                {"type": "video", "src": f"{videos_dir}/{videos[video_index]}"}
            )
            video_index += 1

    return media_files


if __name__ == "__main__":
    images_dir = "0d0b4267be8885ac8aae5358dab94d6da880d184/images/wedding_pics"
    videos_dir = "0d0b4267be8885ac8aae5358dab94d6da880d184/images/videos"

    media_files = generate_media_files(images_dir, videos_dir)

    # Print the media files array in the desired format
    print("const mediaFiles = [")
    for file in media_files:
        print(f"    {{ type: '{file['type']}', src: '{file['src']}' }},")
    print("];")
