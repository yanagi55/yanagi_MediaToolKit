# coding: utf-8
### ★強引で汚いけど、とりあえずGCEでDockerコンテナが動くまで全自動でやるやつ(Debian)↓ ###
### $ itamae ssh -h xx.xx.xx.xx recipe.rb のように使う
execute '
sudo apt-get update -y
sudo apt-get upgrade -y
'
execute '
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
'
execute '
curl -fsSL https://download.docker.com/linux/debian/gpg | \
    sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg --yes
'
execute '
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
'
execute '
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
'

execute '
sudo curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
'

execute '
mkdir yfweb
mkdir postgres
cd yfweb
mkdir conf.d
cd ../..
'

# # 注：以下、動作未確認
execute '
sudo timedatectl set-timezone Asia/Tokyo
sudo docker swarm init --advertise-addr 127.0.0.1 --listen-addr 127.0.0.1:2377
sudo docker network create -d overlay --attachable yfnetwork
'
# execute '
# sudo apt-get -y install task-japanese locales-all
# sudo localectl set-locale LANG=ja_JP.UTF-8 LANGUAGE="ja_JP:ja"
# source /etc/default/locale
# '
