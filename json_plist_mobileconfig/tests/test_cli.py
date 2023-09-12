import subprocess
import json
import plistlib
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

def test_cli_json_to_plist(test_data_dir):
    with TemporaryDirectory() as temp_dir:
        input_file = test_data_dir / 'test_data.json'
        output_file = Path(temp_dir) / 'test_data.plist'

        subprocess.run(['python', '-m', 'json_plist_mobileconfig.converter', str(input_file), '--plist', '--output-dir', temp_dir])

        assert output_file.exists()

def test_cli_plist_to_json(test_data_dir):
    with TemporaryDirectory() as temp_dir:
        input_file = test_data_dir / 'test_data.plist'
        output_file = Path(temp_dir) / 'test_data.json'

        subprocess.run(['python', '-m', 'json_plist_mobileconfig.converter', str(input_file), '--json', '--output-dir', temp_dir])

        assert output_file.exists()


def test_cli_json_to_mobileconfig(test_data_dir):
    with TemporaryDirectory() as temp_dir:
        input_file = test_data_dir / 'test_data.json'
        output_file = Path(temp_dir) / 'test_data.mobileconfig'

        subprocess.run(['python', '-m', 'json_plist_mobileconfig.converter', str(input_file), '--mobileconfig', '--domain', 'com.example', '--output-dir', temp_dir])

        assert output_file.exists()

        with output_file.open('rb') as f:
            data = plistlib.load(f)
            assert data['PayloadContent'][0]['PayloadContent']['com.example']['Forced'][0]['mcx_preference_settings'] == {"key": "value"}

        output_file.unlink()
