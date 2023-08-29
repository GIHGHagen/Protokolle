#!/usr/bin/env python3
import pypandoc
import argparse
import frontmatter
import subprocess
import imt_names
import sys

def generate_html(protocol_path, output):
    # read protocol

    content = pypandoc.convert_file(
        protocol_path, "html", extra_args=["--metadata", "metadata.yaml"]
    )

    with open("protocol.html", "w") as output_file:
        output_file.write(content)




def generate_pdf(protocol_path, output, signature):
    # read protocol

    content = pypandoc.convert_file(
        protocol_path, "tex", extra_args=["--metadata", "metadata.yaml"]
    )

    # read template

    with open("template.tex", "r") as template:
        template_content = template.read()

    # read metadata

    metadata = frontmatter.load(protocol_path)

    # replace placeholders

    template_content = template_content.replace("REPLACE_TYPE", str(metadata["type"]))
    template_content = template_content.replace("REPLACE_DATE", str(metadata["date"]))
    template_content = template_content.replace("REPLACE_BEGIN", str(metadata["begin"]))
    template_content = template_content.replace("REPLACE_END", str(metadata["end"]))
    template_content = template_content.replace(
        "REPLACE_SITZUNGSLEITUNG", imt_names.name_lookup(str(metadata["sitzungsleitung"]))
    )
    template_content = template_content.replace(
        "REPLACE_PROTOKOLL_NAME", imt_names.name_lookup(str(metadata["protokoll"]))
    )
    template_content = template_content.replace(
        "REPLACE_PROTOKOLL_TITLE", imt_names.protocol_title_lookup(str(metadata["protokoll"]))
    )

    if signature:
        content += "\\signatureline"

    template_content = template_content.replace("REPLACE_CONTENT", content)

    # write to file
    with open("protocol.tex", "w") as output_file:
        output_file.write(template_content)

    # generate pdf
    subprocess.run(
        ["latexmk", "-pdf", "-lualatex", "-jobname=" + output, "protocol.tex"]
    )

    # cleanup
    subprocess.run(["latexmk", "-c", "-jobname=" + output, "protocol.tex"])
    subprocess.run(["rm", "protocol.tex"])


# Parse arguments
parser = argparse.ArgumentParser(description="Generate protocol PDF.")

# Type of protocol

parser.add_argument(
    "-t",
    "--type",
    choices=["v", "Vorstandssitzungen", "m", "Mitgliederversammlungen"],
    type=str,
    help="Protokoll Typ",
)

# Date of protocol
parser.add_argument("-d ", "--date", type=str, help="Protokoll Datum (YYYY-MM-DD)")

# Format of protocol
parser.add_argument(
    "-f",
    "--format",
    choices=["pdf", "html"],
    type=str,
    help="Protokoll Format",
    default="pdf",
    required=False,
)

# Signature
parser.add_argument(
    "-s",
    "--signature",
    action="store_true",
    help="Protokoll mit Unterschriften",
    required=False,
)

args = parser.parse_args()


protocol_type = str()
if args.type in ["v", "Vorstandssitzungen"]:
    protocol_type = "Vorstandssitzungen"
elif args.type in ["m", "Mitgliederversammlungen"]:
    protocol_type = "Mitgliederversammlungen"
else:
    print("Error: Unknown protocol type.")
    exit(1)

protocol_path = (
    protocol_type
    + "/"
    + args.date.split("-")[0]
    + "/"
    + args.date.split("-")[1]
    + "/"
    + args.date
    + ".md"
)


if args.format == "pdf":
    generate_pdf(
        protocol_path,
        protocol_type[:-2] + "_" + args.date,
        args.signature,
    )
elif args.format == "html":
    if args.signature:
        print("Error: HTML Protocols can't have signatures."
                "Use PDF instead.", file=sys.stderr)
        generate_html(protocol_path, protocol_type[:-2] + "_" + args.date)
        exit(1)
    generate_html(protocol_path, protocol_type[:-2] + "_" + args.date)
else:
    print("Error: Unknown protocol format.")
    exit(1)
