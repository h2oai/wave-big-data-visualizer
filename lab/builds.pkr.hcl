build {
  sources = [
    "source.amazon-ebs.aws-sandbox",
  ]

  provisioner "file" {
    source      = "training"
    destination = "/home/ubuntu/"
  }

  provisioner "file" {
    source      = "wave-aquarium-lab.tar.gz"
    destination = "/home/ubuntu/"
  }

  provisioner "file" {
    source      = "start-lab.sh"
    destination = "/home/ubuntu/"
  }

  provisioner "shell" {
    inline = ["/usr/bin/cloud-init status --wait"]
  }

  provisioner "shell" {
    scripts = [
      "prepare-environment.sh",
    ]
  }
}
