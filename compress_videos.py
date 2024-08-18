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


def convert_to_mp4(file_path, output_dir, fps=24):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    new_file_name = os.path.splitext(os.path.basename(file_path))[0] + ".mp4"
    new_file_path = os.path.join(output_dir, new_file_name)
    command = [
        "ffmpeg",
        "-i",
        file_path,
        "-vcodec",
        "libx264",
        "-crf",
        "28",  # Constant Rate Factor, lower value means better quality but larger file size
        "-preset",
        "veryslow",  # Compression speed: "ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"
        "-acodec",
        "aac",
        "-b:a",
        "128k",  # Audio bitrate
        "-r",
        str(fps),  # Set the frame rate
        new_file_path,
    ]
    print(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful: {new_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
    return new_file_path


def compress_videos(path, output_dir, fps=24):
    if os.path.isfile(path):
        new_file_path = convert_to_mp4(path, output_dir, fps)
        print(f"Compressed {path} to {new_file_path}")
    elif os.path.isdir(path):
        files = get_video_files(path)
        for file_path in files:
            new_file_path = convert_to_mp4(file_path, output_dir, fps)
            print(f"Compressed {file_path} to {new_file_path}")
    else:
        print(f"Invalid path: {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress videos to MP4 with H.264 and AAC codecs."
    )
    parser.add_argument(
        "path", type=str, help="Path to the video file or directory containing videos."
    )
    parser.add_argument(
        "output_dir", type=str, help="Directory to save the compressed videos."
    )
    parser.add_argument(
        "--fps", type=int, default=24, help="Frame rate for the output video."
    )
    args = parser.parse_args()

    compress_videos(args.path, args.output_dir, args.fps)

# python compress_videos.py /path/to/file_or_directory /path/to/output_directory --fps 24
