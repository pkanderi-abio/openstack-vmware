variable "vsphere_user" {}
variable "vsphere_password" {
  sensitive = true
}
variable "vsphere_server" {}

variable "datacenter" {}
variable "cluster" {}
variable "datastore" {}
variable "network" {}
variable "template_name" {}
variable "vm_count" {
  default = 3
}
variable "vm_cpu" {
  default = 4
}
variable "vm_ram" {
  default = 8192
}
variable "vm_disk" {
  default = 40
}
variable "vm_folder" {
  default = "OpenStack"
}
