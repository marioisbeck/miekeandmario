## file is not working :-(

# import os
# import re
# import sys
# import argparse
# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
# )


# def renumber_files(file_path, start_comment, end_comment, image_folder, video_folder):
#     logging.info("Starting renumbering process")

#     # Check if the file and folders exist
#     if not os.path.isfile(file_path):
#         logging.error(f"The file {file_path} does not exist.")
#         raise FileNotFoundError(f"The file {file_path} does not exist.")
#     if not os.path.isdir(image_folder):
#         logging.error(f"The image directory {image_folder} does not exist.")
#         raise NotADirectoryError(f"The image directory {image_folder} does not exist.")
#     if not os.path.isdir(video_folder):
#         logging.error(f"The video directory {video_folder} does not exist.")
#         raise NotADirectoryError(f"The video directory {video_folder} does not exist.")

#     # Read the file and extract the relevant lines
#     with open(file_path, "r") as file:
#         lines = file.readlines()

#     start_index = None
#     end_index = None

#     start_comment_pattern = re.compile(rf"^\s*{re.escape(start_comment)}")
#     end_comment_pattern = re.compile(rf"^\s*{re.escape(end_comment)}")

#     for i, line in enumerate(lines):
#         if start_comment_pattern.match(line):
#             start_index = i
#         if end_comment_pattern.match(line):
#             end_index = i
#             break

#     if start_index is None or end_index is None:
#         logging.error("Start or end comment not found in the file.")
#         raise ValueError("Start or end comment not found in the file.")

#     relevant_lines = lines[start_index + 1 : end_index]

#     # Parse the renumbering instructions
#     valid_instructions = []
#     for line in relevant_lines:
#         match = re.match(
#             r"(\s*)\{ type: '(\w+)', src: 'images/wedding_pics/(\d+)_to_(\d+\.\d+|\d+)\.(jpg|mp4)' \}",
#             line,
#         )
#         if match:
#             indentation, file_type, old_number, new_number, extension = match.groups()
#             old_number = int(old_number) if "." not in old_number else float(old_number)
#             new_number = int(new_number) if "." not in new_number else float(new_number)
#             folder = image_folder if extension == "jpg" else video_folder
#             old_file_path = os.path.join(folder, f"{old_number}.{extension}")
#             if os.path.exists(old_file_path):
#                 valid_instructions.append((indentation, line))
#                 adjust_files(file_type, old_number, new_number, extension, folder)
#         else:
#             match = re.match(
#                 r"(\s*)\{ type: '(\w+)', src: 'images/wedding_pics/(\d+)\.(jpg|mp4)' \}",
#                 line,
#             )
#             if match:
#                 indentation, file_type, number, extension = match.groups()
#                 number = int(number) if "." not in number else float(number)
#                 folder = image_folder if extension == "jpg" else video_folder
#                 file_path = os.path.join(folder, f"{number}.{extension}")
#                 if os.path.exists(file_path):
#                     valid_instructions.append((indentation, line))

#     # Fill gaps in numbering and add unmatched files
#     fill_gaps_and_add_unmatched(image_folder, video_folder, valid_instructions)

#     # Update the file with valid instructions
#     with open(file_path, "w") as file:
#         file.writelines(lines[: start_index + 1])
#         for indentation, instruction in valid_instructions:
#             logging.debug(f"Writing instruction: {instruction.strip()}")
#             file.write(f"{indentation}{instruction}")
#         file.writelines(lines[end_index:])

#     logging.info("Renumbering process completed")


# def adjust_files(file_type, old_number, new_number, extension, folder):
#     logging.debug(f"Adjusting files in {folder} from {old_number} to {new_number}")

#     for root, _, files in os.walk(folder):
#         files = [f for f in files if f.endswith(f".{extension}")]
#         files.sort(
#             key=lambda x: (
#                 int(x.split(".")[0]) if x.split(".")[0].isdigit() else float("inf")
#             )
#         )

#         if old_number < new_number:
#             # Increase numbers for files between old_number and new_number
#             for file in reversed(files):
#                 match = re.match(r"(\d+\.\d+|\d+)\.(jpg|mp4)", file)
#                 if match:
#                     current_number, ext = match.groups()
#                     current_number = (
#                         int(current_number)
#                         if "." not in current_number
#                         else float(current_number)
#                     )
#                     if old_number < current_number <= new_number and ext == extension:
#                         new_name = f"{current_number + 1}.{ext}"
#                         os.rename(
#                             os.path.join(root, file), os.path.join(root, new_name)
#                         )
#                         logging.debug(f"Renamed {file} to {new_name}")
#         else:
#             # Decrease numbers for files between new_number and old_number
#             for file in files:
#                 match = re.match(r"(\d+\.\d+|\d+)\.(jpg|mp4)", file)
#                 if match:
#                     current_number, ext = match.groups()
#                     current_number = (
#                         int(current_number)
#                         if "." not in current_number
#                         else float(current_number)
#                     )
#                     if new_number <= current_number < old_number and ext == extension:
#                         new_name = f"{current_number + 1}.{ext}"
#                         os.rename(
#                             os.path.join(root, file), os.path.join(root, new_name)
#                         )
#                         logging.debug(f"Renamed {file} to {new_name}")

#         # Rename the original file
#         old_file = f"{old_number}.{extension}"
#         new_file = f"{new_number}.{extension}"
#         if os.path.exists(os.path.join(root, old_file)):
#             os.rename(os.path.join(root, old_file), os.path.join(root, new_file))
#             logging.debug(f"Renamed {old_file} to {new_file}")


# def fill_gaps_and_add_unmatched(image_folder, video_folder, valid_instructions):
#     logging.debug(
#         f"Filling gaps and adding unmatched files in {image_folder} and {video_folder}"
#     )

#     files = []
#     for folder in [image_folder, video_folder]:
#         for root, _, filenames in os.walk(folder):
#             for filename in filenames:
#                 if filename.endswith((".jpg", ".mp4")):
#                     files.append(os.path.join(root, filename))

#     files.sort(
#         key=lambda x: (
#             float(os.path.basename(x).split(".")[0])
#             if "." in os.path.basename(x).split(".")[0]
#             else int(os.path.basename(x).split(".")[0])
#         )
#     )

#     expected_number = 1
#     for file in files:
#         match = re.match(r"(\d+\.\d+|\d+)\.(jpg|mp4)", os.path.basename(file))
#         if match:
#             current_number, ext = match.groups()
#             current_number = (
#                 int(current_number)
#                 if "." not in current_number
#                 else float(current_number)
#             )
#             if current_number != expected_number:
#                 new_name = (
#                     f"{expected_number:.1f}.{ext}"
#                     if ext == "mp4"
#                     else f"{expected_number}.{ext}"
#                 )
#                 os.rename(file, os.path.join(os.path.dirname(file), new_name))
#                 file = os.path.join(os.path.dirname(file), new_name)
#                 logging.debug(f"Renamed {file} to {new_name}")
#             expected_number += 1 if ext == "jpg" else 0.1
#         else:
#             new_name = (
#                 f"{expected_number:.1f}.{ext}"
#                 if ext == "mp4"
#                 else f"{expected_number}.{ext}"
#             )
#             os.rename(file, os.path.join(os.path.dirname(file), new_name))
#             file = os.path.join(os.path.dirname(file), new_name)
#             valid_instructions.append(
#                 (
#                     "\t\t\t",
#                     f"{{ type: '{'image' if ext == 'jpg' else 'video'}', src: 'images/{'wedding_pics' if ext == 'jpg' else 'videos'}/{new_name}' }}\n",
#                 )
#             )
#             logging.debug(f"Added unmatched file {file} as {new_name}")
#             expected_number += 1 if ext == "jpg" else 0.1


# def main():
#     parser = argparse.ArgumentParser(
#         description="Renumber images and videos in an HTML file.",
#         epilog="Example: python renumber_files.py ./0d0b4267be8885ac8aae5358dab94d6da880d184/index.html "
#         '"// START RENUMBERING IMAGES - DO NOT REMOVE THIS COMMENT" '
#         '"// END RENUMBERING IMAGES - DO NOT REMOVE THIS COMMENT" '
#         "./0d0b4267be8885ac8aae5358dab94d6da880d184/images/wedding_pics "
#         "./0d0b4267be8885ac8aae5358dab94d6da880d184/images/videos",
#     )
#     parser.add_argument("file_path", type=str, help="Path to the HTML file")
#     parser.add_argument(
#         "start_comment", type=str, help="Start comment to look for in the file"
#     )
#     parser.add_argument(
#         "end_comment", type=str, help="End comment to look for in the file"
#     )
#     parser.add_argument(
#         "image_folder", type=str, help="Path to the folder containing images"
#     )
#     parser.add_argument(
#         "video_folder", type=str, help="Path to the folder containing videos"
#     )

#     args = parser.parse_args()

#     try:
#         renumber_files(
#             args.file_path,
#             args.start_comment,
#             args.end_comment,
#             args.image_folder,
#             args.video_folder,
#         )
#     except Exception as e:
#         logging.error(f"Error: {e}")
#         sys.exit(1)


# if __name__ == "__main__":
#     main()
