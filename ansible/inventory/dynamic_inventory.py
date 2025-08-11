#!/usr/bin/env python3
import json
import os
import sys

inv_file = os.path.join(os.path.dirname(__file__), "dynamic_inventory.json")

if not os.path.exists(inv_file):
    sys.stderr.write(f"[ERROR] Inventory file {inv_file} not found!\n")
    sys.exit(1)

with open(inv_file) as f:
    inventory = json.load(f)

# Output exactly what was stored by tf_to_inventory.py
print(json.dumps(inventory))
