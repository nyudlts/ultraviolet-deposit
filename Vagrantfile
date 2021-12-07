Vagrant.configure("2") do |config|
  config.vm.box = "bento/centos-7"
  
  # Enable GUI
  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 2
  end
  
  #For compatability with vbguest later versions 
  config.vbguest.installer_options = { allow_kernel_upgrade: true }

  # Create a synced folder
  config.vm.synced_folder ".", "/home/vagrant/ultraviolet-deposit"

  # Install development environment prerequisites
  config.vm.provision "shell", path: "scripts/vagrant/bootstrap.sh"

  #Install pyenv and python
  config.vm.provision "shell", path: "scripts/vagrant/pyenv_install.sh", privileged: false

  # Redis
  config.vm.network "forwarded_port", guest: 6379, host: 6374
  # RabbitMQ
  config.vm.network "forwarded_port", guest: 15672, host: 15673
  config.vm.network "forwarded_port", guest: 5672,  host: 5673
  # Elasticsearch
  config.vm.network "forwarded_port", guest: 9200, host: 9202
end
