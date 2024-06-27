## WTPN

This script is a hobby project designed to validate a domain's Universal Links and Apple App Site Association configuration. It utilizes both the Apple CDN check and fetches the `assetlinks.json` file to provide detailed information on the domain's configuration.

### Features

* Checks domain validity using the Apple App Site Association CDN.
* Fetches and parses the `assetlinks.json` file for further details.
* Outputs information in a user-friendly table format or JSON format.

### Usage

The script can be run from the command line using Python. Here's how:

```python
python script.py <domain> [--json]
```

* `<domain>`: The domain you want to validate (e.g., `example.com`).
* `--json` (Optional): Flag to output the information in JSON format. By default, the output is in a table format.

### Example

```python
python script.py google.com --json
```

This command will validate `google.com` and print the information in JSON format.

### Installation

**Dependencies:**

This script requires the following Python libraries:

* `requests`
* `json`
* `argparse`
* `rich` (for rich text formatting)

You can install them using pip:

```
pip install requests json argparse rich
```

### Contributing

Feel free to explore the code and play around! If you find any bugs or have suggestions for improvement, consider opening an issue on this repository.

### License

This script is licensed under the MIT License. See the LICENSE.md file for details.
