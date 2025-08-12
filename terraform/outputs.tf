output "vms" {
  value = [
    for vm in vsphere_virtual_machine.vm :
    {
      name = vm.name
      ip   = vm.default_ip_address
    }
  ]
}
