# BakimTakip 4 ubuntu vm
#   vagrant up

ANAHTAR = File.join(__dir__, "lab_anahtar")
unless File.exist?(ANAHTAR) && File.exist?("#{ANAHTAR}.pub")
  abort "Once bu klasorde calistir: ssh-keygen -t ed25519 -N \"\" -f lab_anahtar"
end

MAKINELER = [
  # ad,        kutu,                  ip,              bellek (MB), islemci
  ["kontrol",  "bento/ubuntu-24.04", "192.168.56.12", 2048, 2],
  ["eski",     "bento/ubuntu-22.04", "192.168.56.11", 1024, 1],
  ["yeni-app", "bento/ubuntu-24.04", "192.168.56.13", 1024, 1],
  ["yeni-db",  "bento/ubuntu-24.04", "192.168.56.14", 1024, 1],
]

HOSTS = MAKINELER.map { |ad, _, ip| "#{ip} #{ad}" }.join("\n")

Vagrant.configure("2") do |config|
  config.vm.box_check_update = false
  # Paylasimli klasor kullanmiyoruz; dosyalari "file" ile kopyaliyoruz.
  config.vm.synced_folder ".", "/vagrant", disabled: true

  MAKINELER.each do |ad, kutu, ip, bellek, islemci|
    config.vm.define ad do |m|
      m.vm.box = kutu
      m.vm.hostname = ad
      m.vm.network "private_network", ip: ip

      m.vm.provider "virtualbox" do |vb|
        vb.name = "bakim-#{ad}"
        vb.memory = bellek
        vb.cpus = islemci
      end

      # Herkes herkesi adiyla bulsun
      m.vm.provision "shell", name: "hosts", inline: <<-SHELL
        sed -i '/# bakim-lab/,/# bakim-lab-son/d' /etc/hosts
        printf '# bakim-lab\n%s\n# bakim-lab-son\n' "#{HOSTS}" >> /etc/hosts
      SHELL

      # Kontrol makinesinin anahtari her makineye girebilsin
      m.vm.provision "file", source: "#{ANAHTAR}.pub", destination: "/tmp/lab_anahtar.pub"
      m.vm.provision "shell", name: "ssh-izni", inline: <<-SHELL
        AK=/home/vagrant/.ssh/authorized_keys
        grep -qxF "$(cat /tmp/lab_anahtar.pub)" "$AK" || cat /tmp/lab_anahtar.pub >> "$AK"
      SHELL

            next unless ad == "kontrol"

      # Kontrol makinesine ozel anahtar
      m.vm.provision "file", source: ANAHTAR, destination: "/home/vagrant/.ssh/id_ed25519"
      m.vm.provision "shell", name: "kontrol-hazirlik", inline: <<-SHELL
        chmod 600 /home/vagrant/.ssh/id_ed25519
        chown -R vagrant:vagrant /home/vagrant/.ssh
      SHELL
    end
  end
end
