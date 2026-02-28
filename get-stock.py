import re
import sys
import glob
import os
import html
from urllib.parse import unquote

def extract_info_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define the regex patterns for the two tokens
    pattern = r'<title>(.*?)</title>'

    # Find all matches for the pattern
    platform = re.findall(pattern, content)[0][-12:].strip()

    if(platform == "Shutterstock"):

        # Define the regex patterns for the two tokens
        pattern = r'src=\".*?-([0-9]{10})\.[jpg|JPG].*?alt=\"(.*?)\" data-testid=\".*?bodyBoldSm\">(.*?\.(jpg|JPG))'

        # Find all matches for the pattern
        matches = re.findall(pattern, content)

        # Print the results as "<value 1>,<value 2>"
        for match in matches:
            print(f"{platform},{match[2]},{match[0]},\"{html.unescape(match[1])}\"")

    elif (platform == "Adobe Stock"):
        # Define the regex patterns for the two tokens
        pattern = r'%22%2C%22original_name%22%3A%22(.*?)%22%2C%22.*?F220_F_(.*?)_.*?title%22%3A%22(.*?)%22%2C%22'

        # Find all matches for the pattern
        matches = re.findall(pattern, content)

        # Print the results as "<Filename>,<Adobe ID>,<Picture Title>"
        for match in matches:
            print(f"{platform},{match[0]},{match[1]},\"{unquote(match[2])}\"")

    else:
        print('Unsupported platfrom: ', platform)

def show_usage():
    print("Usage:")
    print("  py script.py <file_pattern>")
    print("  Example: py script.py 'Catalog Manager _ Shutterstock.html'")
    print("  Example: py script.py '*.html'")

def main():
    # Check if any arguments were provided
    if len(sys.argv) < 2:
        print("Error: No file pattern provided.")
        show_usage()
        sys.exit(1)

    # Get all file paths based on arguments passed (wildcards are supported)
    file_paths = []
    for arg in sys.argv[1:]:
        matched_files = glob.glob(arg)
        if matched_files:
            file_paths.extend(matched_files)
        else:
            print(f"Warning: No files matched for pattern '{arg}'")

    # If no valid files were found, display usage and exit
    if not file_paths:
        print("Error: No valid files found.")
        show_usage()
        sys.exit(1)

    # Process each file
    for file_path in file_paths:
        if os.path.isfile(file_path):
            #print(f"Processing file: {file_path}")
            extract_info_from_file(file_path)
        else:
            print(f"Error: '{file_path}' is not a valid file.")

if __name__ == "__main__":
    main()
