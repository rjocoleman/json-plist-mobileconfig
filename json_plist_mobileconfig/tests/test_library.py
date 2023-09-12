from json_plist_mobileconfig.converter import (
    read_input_file,
    convert_to_plist,
    convert_to_json,
    create_mobileconfig,
    write_to_file,
    write_json_to_file,
    determine_output_filename
)
import os
from pathlib import Path
from uuid import UUID
import pytest

def test_read_input_file_json(test_data_dir):
    data = read_input_file(test_data_dir / 'test_data.json')
    assert data == {"key": "value"}

def test_read_input_file_plist(test_data_dir):
    data = read_input_file(test_data_dir / 'test_data.plist')
    assert data == {"key": "value"}

def test_convert_to_json():
    data = {"key": "value"}
    json_data = convert_to_json(data)
    assert json_data == '{\n    "key": "value"\n}'

def test_create_mobileconfig():
    plist_data = b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n\t<key>key</key>\n\t<string>value</string>\n</dict>\n</plist>\n'
    uuid = "123e4567-e89b-12d3-a456-426614174000"
    removal_disallowed = False
    identifier = "com.example.customsettings"
    payload_version = 1
    payload_display_name = "Custom Settings"
    domain = "com.example"
    mobileconfig_data = create_mobileconfig(plist_data, uuid, removal_disallowed, identifier, payload_version, payload_display_name, domain)
    assert b"123e4567-e89b-12d3-a456-426614174000" in mobileconfig_data
    assert b"com.example.customsettings" in mobileconfig_data
    assert b"Custom Settings" in mobileconfig_data

def test_write_to_file(test_data_dir):
    data = b'Test data'
    output_file = test_data_dir / 'test_output_file.mobileconfig'
    write_to_file(data, output_file)
    with output_file.open('rb') as file:
        assert file.read() == data
    output_file.unlink()

def test_write_json_to_file(test_data_dir):
    data = '{"key": "value"}'
    output_file = test_data_dir / 'test_output_file.json'
    write_json_to_file(data, output_file)
    with output_file.open('r') as file:
        assert file.read() == data
    output_file.unlink()

def test_determine_output_filename(test_data_dir):
    input_file = test_data_dir / 'test_data.json'
    extension = '.plist'
    output_filename = determine_output_filename(input_file, extension, Path(test_data_dir))
    assert Path(output_filename) == test_data_dir / 'test_data.plist'

def test_convert_to_plist():
    data = {"key": "value"}
    plist_data = convert_to_plist(data)
    assert plist_data == b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n\t<key>key</key>\n\t<string>value</string>\n</dict>\n</plist>\n'
