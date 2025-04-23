#!/usr/local/bin/python3
"""
Extract chapters from podcast JSON summary.
"""
import argparse
import json
import os
import re
import sys


def extract_chapters(json_file):
    """
    Extract chapters from podcast JSON summary.
    """

    # Load JSON data
    with open(json_file, "r") as f:
        data = json.load(f)

    # Extract the Notes section (a list with a single string)
    if "Notes" not in data or not data["Notes"]:
        return []

    notes_text = data["Notes"][0]

    # Split the string by newline characters
    lines = notes_text.split("\n")

    # Initialize a list to store the chapters with a default chapter for the beginning
    # chapters = ["00:00 Welcome"]
    chapters = []

    # Regular expression to match chapter lines
    pattern = r"##### (.*?)\*\*(.*?)\*\* \((\d+:\d+) - \d+:\d+\)"

    for line in lines:
        match = re.search(pattern, line)
        if match:
            # emoji = match.group(1).strip()
            title = match.group(2).strip()
            start_time = match.group(3)

            chapters.append(f"{start_time} {title}")

    return chapters


def main():
    """
    Main function.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Extract chapters from podcast JSON summary."
    )
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("--output", "-o", help="Output file path (optional)")

    # Parse arguments
    args = parser.parse_args()

    # Create default output file name if not provided
    if args.output:
        output_file = args.output
    else:
        # Get base name of input file without extension and append _chapters.txt
        base_name = os.path.basename(args.json_file)
        base_name_no_ext = os.path.splitext(base_name)[0]
        output_file = f"{base_name_no_ext}_chapters.txt"

    try:
        # Extract chapters
        chapters = extract_chapters(args.json_file)

        if chapters:
            # Write to output file
            with open(output_file, "w") as f:
                for chapter in chapters:
                    f.write(f"{chapter}\n")

            print(f"\n# Extracted {len(chapters)} chapters from {args.json_file}")
            print(f"# Results saved to {output_file}")

            # Also print to console
            print("\n# Extracted Chapters:\n")
            for chapter in chapters:
                print(chapter)
        else:
            print(f"No chapters found in the JSON file: {args.json_file}")

        print("\n")

    except FileNotFoundError:
        print(f"Error: File '{args.json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{args.json_file}'.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
