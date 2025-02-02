import re
import requests
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

def download_file_from_url(url):
    """
    Downloads a text file from the given URL and returns its content as a list of lines.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the download fails
    return response.text.splitlines()

def process_config_file(input_url, output_file, new_name):
    """
    Processes the config file from a URL and saves the updated configs to the output file.
    """
    # Download the config file from the URL
    config_lines = download_file_from_url(input_url)

    # Process each line
    updated_lines = []
    for line in config_lines:
        line = line.strip()
        if line:
            updated_line = extract_and_replace_display_name(line, new_name)
            updated_lines.append(updated_line)

    # Save the updated configs to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(updated_lines))

# Get user input
input_url = input("Enter the URL of the config file: ")
output_file = input("Enter the output file path: ")
new_name = input("Enter the new display name: ")

# Process the file
process_config_file(input_url, output_file, new_name)
print("✅ FUCKED URL successfully!")
