# lint all markdown protocol files in the repository

import os
import sys
import frontmatter

has_error = False
# get all markdown files not in root directory
markdown_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".md"):
            markdown_files.append(os.path.join(root, file))

# remove template files and Readme.md (only lint protocol files)
markdown_files.remove("./Vorstandssitzungen/protokollvorlage.md")
markdown_files.remove("./Mitgliederversammlungen/protokollvorlage.md")
markdown_files.remove("./Rechenschaftsberichte/protokollvorlage.md")
markdown_files.remove("./Readme.md")

# get frontmatter from "Vorstandssitzungen/protokollvorlage.md" and "Mitgliederversammlungen/protokollvorlage.md"
metadata_vorstand = frontmatter.load("Vorstandssitzungen/protokollvorlage.md")
metadata_mitgliederversammlung = frontmatter.load("Mitgliederversammlungen/protokollvorlage.md")
metadata_rechenschaftsbericht = frontmatter.load("Rechenschaftsberichte/protokollvorlage.md")

# lint all markdown files
for file in markdown_files:
    if file.startswith("./Vorstandssitzungen/"):
        reference_metadata = metadata_vorstand
    elif file.startswith("./Mitgliederversammlungen/"):
        reference_metadata = metadata_mitgliederversammlung
    elif file.startswith("./Rechenschaftsberichte/"):
        reference_metadata = metadata_rechenschaftsbericht
    else:
        print("---")
        print("Unknown file type: " + file)
        print("---")
        has_error = True
        continue
    
    # get frontmatter from file
    metadata = frontmatter.load(file)

    # check if all keys are present
    for key in reference_metadata.keys():
        if key not in metadata.keys():
            print("---")
            print("Key " + key + " not found in " + file)
            print("---")
            has_error = True
    
    # check if all keys have meaningful values
    for key in reference_metadata.keys():
        if key != "type" and key != "published":
            if metadata[key] == "":
                print("---")
                print("Key " + key + " is empty in " + file)
                print("---")
                has_error = True
            elif metadata[key] == reference_metadata[key]:
                print("---")
                print("Key " + key + " has default value in " + file)
                print("---")
                has_error = True
    
    # check if all headings are sorrounded by newlines
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                # check if heading is sorrounded by newlines
                if lines[lines.index(line) - 1] != "\n":
                    print("---")
                    print("Heading not sorrounded by newlines in " + file)
                    print("This is needed for pandoc to display the heading correct.")
                    print("Please add a newline before the heading:" + line)
                    print("---")
                    has_error = True
                elif lines[lines.index(line) + 1] != "\n":
                    print("---")
                    print("Heading not sorrounded by newlines in " + file)
                    print("This is needed for pandoc to display the heading correct.")
                    print("Please add a newline after the heading:" + line)
                    print("---")
                    has_error = True

    # check if files end with exactly one newline
    with open(file, 'rb') as f:
        f.seek(-2, 2)  # Seek to the second-to-last byte from the end of the file
        last_chars = f.read(2)
        if last_chars == b'\n\n':
            print("---")
            print("File ends with more than one newline " + file)
            print("---")
            has_error = True
        else:
            f.seek(-1, 2)  # Seek to the last byte from the end of the file
            last_chars = f.read(1)
            if last_chars != b'\n':
                print("---")
                print("File does not end with a newline " + file)
                print("---")
                has_error = True
    
if has_error:
    sys.exit(1)
else:
    sys.exit(0)
