#!/usr/bin/env python3
import json
import subprocess
import os

TF_DIR = "terraform"

print("[INFO] Getting Terraform outputs...")
tf_output = subprocess.check_output(
    ["terraform", "output", "-json"], cwd=TF_DIR
)
data = json.loads(tf_output)

if "vms" not in data:
    raise SystemExit("[ERROR] No 'vms' output found in Terraform config!")

hostvars = {}
hosts = []
for vm in data["vms"]["value"]:
    ip = vm.get("ip")
    name = vm.get("name", ip)
    if not ip:
        print(f"[WARNING] VM {name} has no IP assigned yet!")
        continue

    hosts.append(name)
    hostvars[name] = {
        "ansible_host": ip,
        "ansible_user": "ubuntu",
        "ansible_ssh_private_key_file": os.path.expanduser("~/.ssh/my-key-pair")
    }

inventory = {
    "_meta": {
        "hostvars": hostvars
    },
    "all": {
        "hosts": hosts
    }
}

inv_dir = os.path.join("ansible", "inventory")
os.makedirs(inv_dir, exist_ok=True)

inv_path = os.path.join(inv_dir, "dynamic_inventory.json")
with open(inv_path, "w") as f:
    json.dump(inventory, f, indent=2)

print(f"[INFO] Ansible inventory saved to {inv_path}")
