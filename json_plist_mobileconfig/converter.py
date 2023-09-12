import json
import plistlib
import argparse
import os
from uuid import uuid4
import importlib.metadata

try:
    __version__ = importlib.metadata.version('json-plist-mobileconfig')
except importlib.metadata.PackageNotFoundError:
    __version__ = 'dev'

def read_input_file(input_file):
    """Reads and returns data from the input JSON or plist file."""
    file_extension = os.path.splitext(input_file)[1]
    with open(input_file, 'rb') as file:
        if file_extension == '.json':
            return json.load(file)
        elif file_extension == '.plist':
            return plistlib.load(file)
        else:
            raise ValueError("Unsupported file type. Please provide a JSON or plist file.")

def convert_to_plist(data):
    """Converts data to plist format."""
    return plistlib.dumps(data, fmt=plistlib.FMT_XML)

def convert_to_json(data):
    """Converts plist data to JSON format."""
    return json.dumps(data, indent=4)

def create_mobileconfig(plist_data, uuid, removal_disallowed, identifier, payload_version, payload_display_name, domain):
    """Creates a mobileconfig file with the plist data embedded as Custom Settings."""
    mobileconfig_dict = {
        "PayloadContent": [
            {
                "PayloadContent": {
                    domain: {
                        "Forced": [
                            {
                                "mcx_preference_settings": plistlib.loads(plist_data)
                            }
                        ]
                    }
                },
                "PayloadEnabled": True,
                "PayloadType": "com.apple.ManagedClient.preferences",
                "PayloadVersion": payload_version,
                "PayloadUUID": uuid,
                "PayloadIdentifier": identifier,
            }
        ],
        "PayloadDisplayName": payload_display_name,
        "PayloadDescription": f"Custom Settings for {domain}",
        "PayloadIdentifier": identifier,
        "PayloadRemovalDisallowed": removal_disallowed,
        "PayloadUUID": uuid,
        "PayloadVersion": payload_version,
    }
    return plistlib.dumps(mobileconfig_dict, fmt=plistlib.FMT_XML)

def write_to_file(data, output_file):
    """Writes data to a file."""
    with open(output_file, 'wb') as file:
        file.write(data)

def write_json_to_file(data, output_file):
    """Writes JSON data to a file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(data)

def determine_output_filename(input_file, extension, output_dir):
    """Determines the output filename based on the input filename and the specified extension."""
    base_name = os.path.basename(os.path.splitext(input_file)[0])
    return os.path.join(output_dir, base_name + extension)

def main():
    parser = argparse.ArgumentParser(description='Convert files between JSON, plist, and mobileconfig formats.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON or plist file')
    parser.add_argument('--output-dir', type=str, default='.', help='Directory to output the files (default is the current directory)')
    parser.add_argument('--plist', action='store_true', help='Output as plist file')
    parser.add_argument('--json', action='store_true', help='Output as JSON file')
    parser.add_argument('--mobileconfig', action='store_true', help='Output as mobileconfig file with embedded plist data')
    parser.add_argument('--domain', type=str, required=False, help='The domain for the settings to apply to in mobileconfig mode (no default value)')
    parser.add_argument('--uuid', type=str, default=str(uuid4()), help='UUID for the mobileconfig file (a new UUID will be generated if not specified)')
    parser.add_argument('--removal-disallowed', action='store_true', default=False, help='Disallow removal of the mobileconfig file (default is false)')
    parser.add_argument('--identifier', type=str, default='com.example.customsettings', help='Identifier for the mobileconfig file (default is com.example.customsettings)')
    parser.add_argument('--payload-version', type=int, default=1, help='Payload version for the mobileconfig file (default is 1)')
    parser.add_argument('--payload-display-name', type=str, default='Custom Settings', help='Payload display name for the mobileconfig file (default is "Custom Settings")')
    parser.add_argument('--version', action='version', version=f'json-plist-mobileconfig version: {__version__}')

    args = parser.parse_args()

    if not args.input_file:
        parser.print_help()
        return

    try:
        # Read the input file (JSON or plist)
        data = read_input_file(args.input_file)

        if args.mobileconfig and not args.domain:
            parser.error("--mobileconfig requires --domain")

        output_dir = args.output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Convert data to plist format and write to file if --plist flag is specified
        if args.plist:
            plist_data = convert_to_plist(data)
            plist_output_file = determine_output_filename(args.input_file, '.plist', output_dir)
            write_to_file(plist_data, plist_output_file)
            print(f"Plist conversion successful! Output written to {plist_output_file}")

        # Convert data to JSON format and write to file if --json flag is specified
        if args.json:
            json_data = convert_to_json(data)
            json_output_file = determine_output_filename(args.input_file, '.json', output_dir)
            write_json_to_file(json_data, json_output_file)
            print(f"JSON conversion successful! Output written to {json_output_file}")

        # Create mobileconfig file with embedded plist data if --mobileconfig flag is specified
        if args.mobileconfig:
            plist_data = convert_to_plist(data)
            mobileconfig_data = create_mobileconfig(plist_data, args.uuid, args.removal_disallowed, args.identifier, args.payload_version, args.payload_display_name, args.domain)
            mobileconfig_output_file = determine_output_filename(args.input_file, '.mobileconfig', output_dir)
            write_to_file(mobileconfig_data, mobileconfig_output_file)
            print(f"Mobileconfig creation successful! Output written to {mobileconfig_output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
