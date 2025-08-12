#!/usr/bin/env python3
import json
import os
import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

def load_inventory(file_path):
    """Load and validate the dynamic inventory JSON file."""
    if not os.path.exists(file_path):
        logging.error(f"Inventory file '{file_path}' not found!")
        sys.exit(1)

    try:
        with open(file_path, "r") as f:
            inventory = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse inventory JSON: {e}")
        sys.exit(1)

    if "_meta" not in inventory or "hostvars" not in inventory["_meta"]:
        logging.warning("Inventory file is missing expected structure.")
    return inventory

def main():
    parser = argparse.ArgumentParser(description="Dynamic inventory loader for Ansible.", add_help=False)
    parser.add_argument(
        "--list", action="store_true",
        help="Output full inventory (required by Ansible)"
    )
    parser.add_argument(
        "--host", help="Output variables for a single host (required by Ansible)"
    )
    parser.add_argument(
        "-f", "--file",
        default=os.path.join(os.path.dirname(__file__), "dynamic_inventory.json"),
        help="Path to dynamic inventory JSON file"
    )
    args, unknown = parser.parse_known_args()  # ignore unknown args to avoid errors

    inventory = load_inventory(args.file)

    if args.list:
        print(json.dumps(inventory, indent=2))
    elif args.host:
        # Return host-specific variables or empty dict if not found
        hostvars = inventory.get("_meta", {}).get("hostvars", {})
        print(json.dumps(hostvars.get(args.host, {}), indent=2))
    else:
        # If no args are provided, behave like `--list`
        print(json.dumps(inventory, indent=2))

if __name__ == "__main__":
    main()
