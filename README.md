# JSON-Plist-Mobileconfig Converter

JSON-Plist-Mobileconfig Converter is a Python package that facilitates the conversion between JSON, plist, and mobileconfig ("Custom Settings") formats.

## Features

- **JSON to Plist**: Convert JSON files to plist format.
- **Plist to JSON**: Convert plist files to JSON format.
- **Plist to Mobileconfig**: Embed plist files into a mobileconfig file for distributing, or forcing, custom settings on Apple devices.
- **JSON to Mobileconfig**: Directly convert JSON files to mobileconfig format for distributing, or forcing, custom settings on Apple devices.


## Installation

You can install the package from PyPI using the following command:

```sh
pip install json-plist-mobileconfig
```

Alternatively, you can clone the repository to your local machine:

```sh
git clone https://github.com/rjocoleman/json-plist-mobileconfig.git
```

Navigate to the project directory:

```sh
cd json-plist-mobileconfig
```

Although the script uses only the Python standard library, if you add any external dependencies in the future, you can install them using:

```sh
pip install -r requirements.txt
```

## Usage

### As a Command-Line Tool

You can use the script as a command-line tool with the following syntax:

```sh
json-plist-mobileconfig input_file [--plist] [--json] [--mobileconfig] [options]
```

(Or not installed via the PyPI package `python ./json-plist-mobileconfig.py`)

#### Arguments

- `input_file`: The path to the input JSON or plist file. (Required)
- `--plist`: If specified, outputs a plist file.
- `--json`: If specified, outputs a JSON file.
- `--mobileconfig`: If specified, outputs a mobileconfig file with embedded plist data.

#### Options

- `--uuid UUID`: Specifies the UUID for the mobileconfig file. A new UUID is generated if not specified.
- `--removal_disallowed`: Disallows removal of the mobileconfig file. Default is false.
- `--identifier IDENTIFIER`: Specifies the identifier for the mobileconfig file. Default is 'com.example.customsettings'.
- `--payload_version PAYLOAD_VERSION`: Specifies the payload version for the mobileconfig file. Default is 1.
- `--payload_display_name PAYLOAD_DISPLAY_NAME`: Specifies the payload display name for the mobileconfig file. Default is 'Custom Settings'.
- `--version`: Displays the version of the script.

### As a Library

You can also use the script as a library in other Python scripts. Here's an example of how to use the functions in the script:

```python
import script_name

# Read data from a JSON or plist file
data = script_name.read_input_file('input_file.json')

# Convert data to plist format
plist_data = script_name.convert_to_plist(data)

# Convert data to JSON format
json_data = script_name.convert_to_json(data)

# Create a mobileconfig file with embedded plist data
mobileconfig_data = script_name.create_mobileconfig(plist_data, uuid, removal_disallowed, identifier, payload_version, payload_display_name)
```

## Credits

[mcxToProfile](https://github.com/timsutton/mcxToProfile) - does something similar, and has a different feature set but relies on external libraries and was harder for me to run

## License

[MIT](LICENSE)
