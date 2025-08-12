#!/usr/bin/env python3
import json
import subprocess
import os
import argparse
import logging
import ipaddress
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

def get_terraform_output(tf_dir):
    """Run terraform output and return parsed JSON."""
    try:
        output = subprocess.check_output(
            ["terraform", "output", "-json"],
            cwd=tf_dir,
            timeout=60
        )
        return json.loads(output)
    except subprocess.CalledProcessError as e:
        logging.error(f"Terraform command failed: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON from terraform output: {e}")
        raise
    except subprocess.TimeoutExpired:
        logging.error("Terraform command timed out after 60s")
        raise

def validate_ip(ip):
    """Validate IP address format."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def build_inventory(vms, ssh_user, ssh_key_path):
    """Build inventory dict from Terraform VM output."""
    hostvars = {}
    hosts = []
    for vm in vms:
        ip = vm.get("ip")
        name = vm.get("name", ip)

        if not ip or not validate_ip(ip):
            logging.warning(f"Skipping VM {name} due to invalid/missing IP.")
            continue

        hosts.append(name)
        hostvars[name] = {
            "ansible_host": ip,
            "ansible_user": ssh_user,
            "ansible_ssh_private_key_file": os.path.expanduser(ssh_key_path)
        }

    return {
        "_meta": {"hostvars": hostvars},
        "all": {"hosts": hosts}
    }

def main():
    parser = argparse.ArgumentParser(description="Convert Terraform output to Ansible dynamic inventory.")
    parser.add_argument("--tf-dir", default="terraform", help="Terraform project directory")
    parser.add_argument("--ssh-user", default="ubuntu", help="Default SSH user for Ansible")
    parser.add_argument("--ssh-key", default="~/.ssh/my-key-pair", help="SSH private key file path")
    parser.add_argument("--output", default="ansible/inventory/dynamic_inventory.json", help="Output inventory file path")
    args = parser.parse_args()

    logging.info("Getting Terraform outputs...")
    data = get_terraform_output(args.tf_dir)

    if "vms" not in data or "value" not in data["vms"]:
        logging.error("No 'vms' output found in Terraform config!")
        sys.exit(1)

    inventory = build_inventory(data["vms"]["value"], args.ssh_user, args.ssh_key)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)

    logging.info(f"Ansible inventory saved to {output_path}")

if __name__ == "__main__":
    main()
