VM_COUNT = 30

Vagrant.configure("2") do |c|
  (1..VM_COUNT).each do |i|
    c.vm.define "dojo#{i}" do |config|
      config.vm.box = "dojo_ipv6"
      config.vm.network "forwarded_port", guest: 22, host: 50000+i , id: 'ssh'
      config.vm.network "private_network", ip: "192.168.1.#{100+i}",
        virtualbox__intnet: "vboxnet#{(i+1)/2}"
      
      config.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--nic3", "natnetwork"]
        vb.customize ["modifyvm", :id, "--nat-network3", "dojonetwork"]
        vb.name = "Dojo #{i}"
        vb.memory = "256"
        vb.linked_clone = true
        vb.check_guest_additions = false
      end
    
      config.vm.provision "prepare", type: "shell" do |s|
        s.inline = <<-SHELL
          useradd -m -p $(openssl passwd -crypt $2) -s /bin/bash $1
          echo "$1 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
          echo "Match User $1\n\tPasswordAuthentication yes" >> /etc/ssh/sshd_config
          systemctl reload ssh
          mkdir -p /var/update_sheet
          cp /vagrant/update_sheet.py /vagrant/token.pickle /var/update_sheet/
          cp /vagrant/update_sheet.service /etc/systemd/system/
          sed -i "s/NUMBER/$3/g" /etc/systemd/system/update_sheet.service
          systemctl enable update_sheet
          systemctl start update_sheet
        SHELL
        s.args = ["dojo#{i}", "dojobeto", i]
      end

      config.vm.provision "network", type: "shell", run: "always" do |s|
        s.inline = <<-SHELL
          echo "nameserver 1.1.1.1" > /etc/resolv.conf
          ip link set eth2 down
          ip addr flush dev eth2
          ip addr add 192.168.0.$1/24 dev eth2
          ip link set eth2 up
          ip route del default
          ip route add default via 192.168.0.1 dev eth2
        SHELL
        s.args = [100+i]
      end
    end
  end
end
