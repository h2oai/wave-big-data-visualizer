locals {
  image_name   = "wave-aquarium-lab-{{timestamp}}"
  volume_size  = 64
  ssh_username = "ubuntu"
}

source "amazon-ebs" "aws-sandbox" {
  subnet_id = "subnet-073a42fd74ac5ba3e"

  ami_name = local.image_name

  instance_type = "m5.large"

  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = local.volume_size
    delete_on_termination = true
  }

  source_ami_filter {
    filters = {
      virtualization-type = "hvm"
      name                = "ubuntu/images/*ubuntu-focal-20.04-amd64-server-*"
      root-device-type    = "ebs"
    }

    owners      = ["099720109477"]
    most_recent = true
  }

  communicator = "ssh"
  ssh_username = local.ssh_username
}

