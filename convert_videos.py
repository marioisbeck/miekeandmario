import os
import re
import argparse
import subprocess


def get_video_files(directory):
    # Get all video files in the directory and subdirectories
    video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if re.match(r".*\.(avi|mov|wmv|flv|mkv|webm|mp4)$", file, re.IGNORECASE):
                video_files.append(os.path.join(root, file))
    return sorted(
        video_files, key=lambda x: (tuple(map(int, re.findall(r"\d+", x))), x)
    )


def convert_to_mp4(file_path):
    new_file_path = os.path.splitext(file_path)[0] + ".mp4"
    command = [
        "ffmpeg",
        "-i",
        file_path,
        "-vcodec",
        "libx264",
        "-acodec",
        "aac",
        "-strict",
        "experimental",
        "-b:a",
        "192k",
        new_file_path,
    ]
    subprocess.run(command, check=True)
    os.remove(file_path)
    return new_file_path


def process_videos(directory):
    files = get_video_files(directory)
    for file_path in files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext != ".mp4":
            new_file_path = convert_to_mp4(file_path)
            print(f"Converted {file_path} to {new_file_path}")
        else:
            print(f"Skipped {file_path} (already in MP4 format)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert videos to MP4 with H.264 and AAC codecs."
    )
    parser.add_argument(
        "directory", type=str, help="Path to the directory containing videos."
    )
    args = parser.parse_args()

    process_videos(args.directory)

# python convert_video.py /images/videos
