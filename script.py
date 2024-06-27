import requests
import json
import argparse
from rich.console import Console
from rich.table import Table

def check_url_status(url, session, headers=None):
    """Check if the URL returns a 200 status code."""
    response = session.get(url, headers=headers) if headers else session.get(url)
    if response.status_code != 200:
        raise ValueError(f"URL '{url}' returned status code {response.status_code}. Domain might not be correct.")
    return response

def validate_domain_with_branch(domain, session):
    """Validate domain using the Apple CDN for App Site Association."""
    domain_url = f"https://app-site-association.cdn-apple.com/a/v1/{domain}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    response = check_url_status(domain_url, session, headers)
    return response.json()

def fetch_assetlinks_json(domain, session):
    """Fetch the assetlinks.json file from the domain."""
    assetlinks_url = f"https://www.{domain}/.well-known/assetlinks.json"
    response = check_url_status(assetlinks_url, session)
    return response.json()

def print_table_data(console, title, columns, rows):
    """Print data in table format using rich."""
    table = Table(title=title)
    for col in columns:
        table.add_column(col, justify="left", style="cyan", no_wrap=False)
    for row in rows:
        table.add_row(*row)
    console.print(table)

def print_json_data(console, data):
    """Print data in JSON format."""
    console.print(json.dumps(data, indent=4))

def validate_domain(domain, output_format):
    """Main function to validate the domain and print information."""
    session = requests.Session()
    console = Console()

    try:
        # Validate domain using Apple CDN
        data = validate_domain_with_branch(domain, session)
        
        # Format data for output
        webcredentials_apps = data.get("webcredentials", {}).get("apps", [])
        applinks_details = data.get("applinks", {}).get("details", [])

        if output_format == "json":
            domain_info = {
                "domain": domain,
                "webcredentials_apps": webcredentials_apps,
                "applinks_details": applinks_details
            }
            print_json_data(console, domain_info)
        else:
            rows = [
                (
                    domain,
                    json.dumps(webcredentials_apps),
                    detail.get("appID", ""),
                    json.dumps(detail.get("paths", []))
                )
                for detail in applinks_details
            ]
            columns = ["Domain", "Webcredentials Apps", "Applinks App ID", "Applinks Paths"]
            print_table_data(console, "Domain Information", columns, rows)
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")

    try:
        # Fetch assetlinks.json
        assetlinks_data = fetch_assetlinks_json(domain, session)

        if output_format == "json":
            print_json_data(console, assetlinks_data)
        else:
            rows = [
                (
                    target.get("package_name", ""),
                    target.get("namespace", ""),
                    "\n".join(target.get("sha256_cert_fingerprints", [])),
                    "\n".join(item.get("relation", []))
                )
                for item in assetlinks_data
                for target in [item.get("target", {})]
            ]
            columns = ["Package Name", "Namespace", "SHA256 Cert Fingerprints", "Relation"]
            print_table_data(console, "Assetlinks.json Information", columns, rows)
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate domain and print information.")
    parser.add_argument("domain", help="The domain to validate")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    output_format = "json" if args.json else "table"
    validate_domain(args.domain, output_format)
