import re
from urllib.parse import unquote, urlparse, parse_qs, urlencode, urlunparse

def extract_and_replace_display_name(config_line, new_name):
    """
    Extracts the display name from any part of the config (parameters or end of the link) and replaces it.
    """
    # Attempt to extract the display name from the end of the link (after #)
    if '#' in config_line:
        parts = config_line.split('#', 1)
        config_part, display_part = parts[0], parts[1]
        # Remove extra spaces and characters
        display_name = display_part.split()[0] if ' ' in display_part else display_part
        updated_line = f"{config_part}#{new_name}"
        return updated_line

    # Parse the URL to check for possible parameters (e.g., ps= or remarks=)
    parsed_url = urlparse(config_line)
    query_params = parse_qs(parsed_url.query)
    
    # Check for possible parameters containing the display name
    display_keys = ['ps', 'remarks', 'name', 'display']
    for key in display_keys:
        if key in query_params:
            query_params[key][0] = new_name
            break
    else:
        # If no parameter is found, add the display name to the end of the link
        return f"{config_line}#{new_name}"

    # Rebuild the URL with updated parameters
    updated_query = urlencode(query_params, doseq=True)
    updated_url = parsed_url._replace(query=updated_query)
    return urlunparse(updated_url)

def process_config_file(input_file, output_file, new_name):
    with open(input_file, 'r', encoding='utf-8') as file:
        config_lines = file.readlines()

    updated_lines = []
    for line in config_lines:
        line = line.strip()
        if line:
            updated_line = extract_and_replace_display_name(line, new_name)
            updated_lines.append(updated_line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(updated_lines))

# Get user input
input_file = input("Enter the input file path: ")
output_file = input("Enter the output file path: ")
new_name = input("Enter the new display name: ")

# Process the file
process_config_file(input_file, output_file, new_name)
print("✅ File updated successfully!")
