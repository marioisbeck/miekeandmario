import os
import argparse
import subprocess


def create_slideshow(image_files, output_path, slide_duration=2, transition_duration=1):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a temporary text file listing all image files
    with open("images.txt", "w") as f:
        for image in image_files:
            f.write(f"file '{image}'\n")
            f.write(f"duration {slide_duration}\n")
        # Add the last image again to ensure it stays for the specified duration
        f.write(f"file '{image_files[-1]}'\n")

    # Command to create the slideshow using ffmpeg
    command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        "images.txt",
        "-vf",
        f"fps=25,format=yuv420p",
        "-pix_fmt",
        "yuv420p",
        "-y",  # Overwrite output file if it exists
        output_path,
    ]

    print(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        print(f"Slideshow created successfully: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during slideshow creation: {e}")
    finally:
        # Clean up the temporary text file
        os.remove("images.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a slideshow from a set of JPG files."
    )
    parser.add_argument(
        "image_files", type=str, nargs="+", help="Paths to the JPG files."
    )
    parser.add_argument(
        "output_path", type=str, help="Path to save the output slideshow video."
    )
    parser.add_argument(
        "--slide_duration",
        type=int,
        default=2,
        help="Duration of each slide in seconds.",
    )
    parser.add_argument(
        "--transition_duration",
        type=int,
        default=1,
        help="Duration of the transition between slides in seconds.",
    )
    args = parser.parse_args()

    create_slideshow(
        args.image_files,
        args.output_path,
        args.slide_duration,
        args.transition_duration,
    )

# Example usage:
# python slideshow_creator.py image1.jpg image2.jpg image3.jpg /path/to/output/slideshow.mp4 --slide_duration 3 --transition_duration 1
