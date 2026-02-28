import re
import sys
import glob
import os
import html
from urllib.parse import unquote

def extract_info_from_file(file_path, forced_platform=None):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Determine platform
    if forced_platform:
        platform = forced_platform
    else:
        pattern = r'<title>(.*?)</title>'
        matches = re.findall(pattern, content)
        if not matches:
            print("Could not detect platform from title.")
            return
        platform = matches[0][-12:].strip()

    if platform == "Shutterstock":
        pattern = r'src=\".*?-([0-9]{10})\.[jpg|JPG].*?alt=\"(.*?)\" data-testid=\".*?bodyBoldSm\">(.*?\.(jpg|JPG))'
        matches = re.findall(pattern, content)

        for match in matches:
            print(f"{platform},{match[2]},{match[0]},\"{html.unescape(match[1])}\"")

    elif platform == "Adobe Stock":
        pattern = r'%22%2C%22original_name%22%3A%22(.*?)%22%2C%22.*?F220_F_(.*?)_.*?title%22%3A%22(.*?)%22%2C%22'
        matches = re.findall(pattern, content)

        for match in matches:
            print(f"{platform},{match[0]},{match[1]},\"{unquote(match[2])}\"")

    else:
        print('Unsupported platform:', platform)

def show_usage():
    print("Usage:")
    print("  py script.py <file_pattern>")
    print("  py script.py <file_pattern> --platform adobe")
    print("  py script.py <file_pattern> --platform shutterstock")
    print("  Example: py script.py '*.html' --platform adobe")

def main():
    if len(sys.argv) < 2:
        print("Error: No file pattern provided.")
        show_usage()
        sys.exit(1)

    forced_platform = None
    args = sys.argv[1:]

    # Detect optional --platform flag
    if "--platform" in args:
        idx = args.index("--platform")
        try:
            value = args[idx + 1].lower()
        except IndexError:
            print("Error: --platform requires a value (adobe or shutterstock).")
            sys.exit(1)

        if value == "adobe":
            forced_platform = "Adobe Stock"
        elif value == "shutterstock":
            forced_platform = "Shutterstock"
        else:
            print("Error: Platform must be 'adobe' or 'shutterstock'.")
            sys.exit(1)

        # Remove the flag and its value from args
        del args[idx:idx+2]

    # Expand file patterns
    file_paths = []
    for arg in args:
        matched_files = glob.glob(arg)
        if matched_files:
            file_paths.extend(matched_files)
        else:
            print(f"Warning: No files matched for pattern '{arg}'")

    if not file_paths:
        print("Error: No valid files found.")
        show_usage()
        sys.exit(1)

    for file_path in file_paths:
        if os.path.isfile(file_path):
            extract_info_from_file(file_path, forced_platform)
        else:
            print(f"Error: '{file_path}' is not a valid file.")

if __name__ == "__main__":
    main()
