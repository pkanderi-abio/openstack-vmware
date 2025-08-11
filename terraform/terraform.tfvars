# vSphere credentials
vsphere_user     = "administrator@vsphere.local"
vsphere_password = "P@ssw0rd"
vsphere_server   = "vc.nextgenitcareers.com"

# vSphere environment details
datacenter    = "Datacenter"
cluster       = "LAB-CL01"
datastore     = "LAB-LUN01"
network       = "LAB-VMs-vLAN_100"

# VM template for Ubuntu 22.04
template_name = "ubuntu-22.04-template"

# VM deployment parameters
vm_count = 3
vm_cpu   = 4         # Number of vCPUs per VM
vm_ram   = 8192      # RAM in MB
vm_disk  = 40        # Disk size in GB
vm_folder = "OpenStack"  # Folder in vSphere to store VMs
