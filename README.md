## **README.md**

```markdown
# OpenStack on VMware with Terraform & Ansible

This project automates the provisioning and configuration of an **OpenStack production cluster** on top of a VMware vSphere environment using:

- **Terraform** → Infrastructure provisioning (VMware VMs)
- **Ansible** → Configuration management & OpenStack deployment (via Kolla-Ansible)
- **Ubuntu 22.04** as the base OS
- **Makefile** for a one-command deployment

---

## 🗂 Project Structure
```

openstack-vmware/
├── terraform/                  # Terraform configs for VMware provisioning
├── ansible/                    # Ansible playbooks & inventory
├── scripts/                    # Terraform → Ansible inventory bridge
├── Makefile                    # One-command deploy/destroy
└── README.md

````

---

## 🚀 Prerequisites

1. **Local machine requirements**
   - Terraform >= 1.3
   - Ansible >= 2.14
   - Python 3.8+
   - VMware vSphere credentials
   - SSH key (`~/.ssh/id_rsa`) uploaded to your VM template

2. **vSphere environment**
   - Ubuntu 22.04 VM template available in vSphere
   - vCenter API access enabled
   - Proper permissions to create VMs, networks, and assign storage

3. **Network access**
   - Management network must be reachable from your control machine
   - OpenStack deployment ports accessible between nodes

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-org/openstack-vmware.git
cd openstack-vmware
````

### 2. Configure Terraform variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

Fill in:

* vSphere server & credentials
* Datacenter, cluster, datastore, network
* Ubuntu 22.04 VM template name
* Number of nodes, CPU, RAM, disk

### 3. Ensure your SSH key works

```bash
ssh -i ~/.ssh/id_rsa ubuntu@<any-vm-ip>
```

---

## ▶️ Deploy OpenStack

Run everything in one command:

```bash
make deploy
```

This will:

1. Provision VMs on VMware using Terraform
2. Generate Ansible inventory from Terraform output
3. Install prerequisites on all nodes
4. Deploy OpenStack using Kolla-Ansible
5. Validate the deployment

---

## 🛑 Destroy Environment

To tear everything down:

```bash
make destroy
```

> This removes all provisioned VMs in vSphere. Use with caution.

---

## 🔍 Troubleshooting

* **Terraform provider errors** → Check `provider.tf` credentials and vSphere API access.
* **Ansible SSH issues** → Ensure your SSH key is preloaded into the VM template.
* **Kolla-Ansible deployment fails** → Check `/etc/kolla/globals.yml` and logs in `/var/log/kolla`.

---

## 📜 License

MIT License

```

---

If you like, I can also **add an `ansible/group_vars/all.yml` file** to predefine Kolla-Ansible globals so the deployment works without manual prompts. That would make the `make deploy` run **100% non-interactive**.  

Do you want me to add that next?
```
