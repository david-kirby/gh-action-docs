#!/usr/bin/env python3
from glob import glob
import yaml
import logging
import sys
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--debug", action="store_true", help="Enable debug output")
args = parser.parse_args()

# Setup logger
if args.debug:
    log_level = "DEBUG"
    format = "%(levelname)s:%(message)s"
else:
    log_level = "ERROR"
    format = "%(message)s"

logging.basicConfig(format=format)
logger = logging.getLogger("main")
logger.setLevel(log_level)


action_file_name_pattern = "action.y*l"
markdown_file_name_pattern = "README.md"
start_marker = "<!--start-gh-action-docs-->"
end_marker = "<!--end-gh-action-docs-->"
input_header = "## Inputs"
output_header = "## Outputs"
supported_fields = ["inputs", "outputs"]


def update_markdown_doc(markdown=None, markdown_file=None):
    # look for start marker and end markers
    start_marker_exists = False
    end_marker_exists = False
    start_marker_index = None
    end_marker_index = None
    read_md = [line for line in open(markdown_file, "r").readlines()]
    for index, line in enumerate(read_md):
        if line.strip() == start_marker:
            start_marker_exists = True
            start_marker_index = index
        if line.strip() == end_marker:
            end_marker_exists = True
            end_marker_index = index

    # Error if not found
    if not start_marker_exists:
        logger.error(f"Missing start marker {start_marker} in {markdown_file}")
        sys.exit(1)
    if not end_marker_exists:
        logger.error(f"Missing end marker {end_marker} in {markdown_file}")
        sys.exit(1)

    # truncate contents between the start and end tags before writing to file
    del read_md[start_marker_index + 1 : end_marker_index]
    with open(markdown_file, "w") as writer:
        for index, line in enumerate(read_md):
            if line.strip() == end_marker:
                writer.write("\n\n")
            writer.write(line)
            if line.strip() == start_marker:
                writer.write("\n")
                writer.write(markdown)
    return True


def calculate_column_size():
    return


def build_table(field_name=None, field_values={}):
    logger.debug(f"Building table for {field_name}")

    """
    Validate input parameters
    """
    if not field_name:
        logging.error("Unable to build table. No field specified")
        sys.exit(1)
    elif field_name not in supported_fields:
        logging.error(f"Unable to build table. {field_name} not supported")
        sys.exit(1)

    """
    Structure of markdown table for inputs and outputs
    TODO: Support filtering out fields or sorting table by a field
    TODO: Table column ordering
    """

    logger.debug(field_values)

    section_headers = {"inputs": "## Inputs", "outputs": "## Outputs"}

    table_header_names = {
        "inputs": ["name", "description", "default", "required"],
        "outputs": ["name", "description"],
    }

    field_size = {"name": 4}

    # Calculate size of table columns
    for key in field_values.keys():
        if len(key) > field_size["name"]:
            field_size["name"] = len(key)
        for header in table_header_names[field_name]:
            if header != "name":
                header_length = len(header)
                field_length = len(str(field_values[key].get(header)))
                if header == "default":
                    field_length += 2  # Add 2 to account for the backticks we add
                # There will be no entries at first so set to length of header names
                if not field_size.get(header):
                    field_size[header] = header_length
                # Replace if a field size is larger than original header
                if field_length > field_size[header]:
                    field_size[header] = field_length

    table_divider = "".join(
        [
            f"| {'-' * field_size[header]} |"
            if index == 0
            else f" {'-' * field_size[header]} |"
            for index, header in enumerate(table_header_names[field_name])
        ]
    )

    table_headers = []
    table_rows = []
    for value in field_values:
        row = ""
        table_header_row = ""
        for index, header in enumerate(table_header_names[field_name]):
            width = field_size[header]
            if not table_headers:
                table_header_row += (
                    f'| {header:{"<"}{width}} |'
                    if index == 0
                    else f' {header:{"<"}{width}} |'
                )
            field = value if header == "name" else field_values[value].get(header)
            if field is None:
                field = "N/A"
            if type(field) == bool:
                field = str(field)
            if header == "default":
                field = f"`{field}`"
            row += (
                f'| {field:{"<"}{width}} |'
                if index == 0
                else f' {field: {"<"}{width}} |'
            )
        table_rows.append(row)
        if table_header_row:
            table_headers.append(table_header_row)
    logger.debug(f"Finished building table for {field_name}")

    fmt_table_headers = "\n".join(table_headers)
    fmt_table_rows = "\n".join(table_rows)
    return (
        f"{section_headers[field_name]}\n\n"
        f"{fmt_table_headers}\n"
        f"{table_divider}\n"
        f"{fmt_table_rows}"
    )


def action_file_to_markdown(action_file):
    body = []
    with open(action_file, "r") as stream:
        try:
            contents = yaml.safe_load(stream)
            if not contents:
                raise Exception("Action file appears empty")
            logger.debug(f"Action file contents: {contents}")
        except Exception as err:
            logger.error(err)
            sys.exit(1)
    for field in supported_fields:
        if not contents.get(field):
            logger.debug(f"No {field} found")
        else:
            logger.debug(f"Found {field}")
            body.append(build_table(field_name=field, field_values=contents.get(field)))
    results = "\n\n".join(body)
    return results


def check_for_file(pattern):
    file_search = glob(pattern)
    logger.debug(f"File(s): {file_search}")
    if len(file_search) > 1:
        logger.debug(f"Too many matches when searching for {pattern}")
        return False

    if len(file_search) == 0:
        logger.debug(f"No files found matching {pattern}")
        return False

    return file_search[0]


def main():
    logger.debug("Checking for action file")
    action_file = check_for_file(action_file_name_pattern)
    if not action_file:
        logger.error("Action file not found")
        sys.exit(1)
    logger.debug("Action file found")

    logger.debug("Checking for markdown file")
    markdown_file = check_for_file(markdown_file_name_pattern)
    if not markdown_file:
        logger.error("Markdown file not found")
        sys.exit(1)
    logger.debug("Markdown file found")
    logger.debug("Process the action file to markdown")
    markdown = action_file_to_markdown(action_file)
    logger.debug("Update markdown file with processed markdown body")
    update_markdown_doc(markdown_file=markdown_file, markdown=markdown)
    logger.debug("Finished updating markdown")


if __name__ == "__main__":
    main()
