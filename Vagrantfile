# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$PROVISION_SCRIPT = <<SCRIPT

apt-get update
apt-get install -y mongodb postgresql libpq-dev python python-dev python-pip python-virtualenv

cd /vagrant

virtualenv env
source env/bin/activate

pip install -r requirements.txt

SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Use a standard Ubuntu 12.04 LTS image
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  
  # Install required packages (using script above)
  config.vm.provision :shell, :inline => $PROVISION_SCRIPT

  # Use VBoxManage to increase memory from default
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  # This is the IP address you can access the VM at
  config.vm.network :private_network, ip: "192.168.33.10"

  config.vm.hostname = "oabutton-dev.local"

end
