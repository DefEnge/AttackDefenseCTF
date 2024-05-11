### BENVENUTO IN MEGASCRIPT ###
# Questo script è stato creato per automatizzare il processo di configurazione dell'infrastruttura.

set -x
set -e

## interfaccia di rete
INTERFACE="game"

#iptables rules

if ! sudo iptables -t nat -C POSTROUTING -j NFQUEUE --queue-bypass; then
	sudo iptables -t nat -A POSTROUTING -j NFQUEUE --queue-bypass
	sudo iptables -t nat -I PREROUTING 1 -j NFQUEUE --queue-bypass
fi

## cartella di destinazione per tulip e regole suricata
sudo mkdir -p /ctf
sudo mkdir /ctf/logs
sudo mkdir /ctf/logs/pcaps
sudo mkdir /ctf/logs/test_pcap
sudo apt update -y

## GIT INSTALL
sudo apt install git -y

## SURICATA INSTALL
sudo add-apt-repository ppa:oisf/suricata-stable -y
sudo apt install suricata jq -y

cp /suricata.yaml /etc/suricata/suricata.yaml

## TULIP INSTALL
cd /ctf
git clone https://github.com/alex1234ilpro/tulip

## Destructive Install
git clone https://github.com/alex1234ilpro/DestructiveFarm

# copia .env file
cd tulip
cp /envfile .env

## modifica la regex per il file .env
#FLAG_REGEX="[A-Z0-9]{31}(?:%3D|=)?"
#sudo sh -c "sed -i 's/FLAG_REGEX=.*/FLAG_REGEX=\""$FLAG_REGEX"\"/' .env"

## rimuovi file di esempio + crea cartella del capture
sudo rm -f services/test_pcap/*
mkdir -p services/pcaps

## modifica docker-compose
cp /docker-compose.yml /ctf/tulip/docker-compose.yml

## install screen if not present
sudo apt install screen -y

## CARTELLA PER LE REGOLE SURICATA
cd /ctf
mkdir -p ipsrules
cd ipsrules
touch local.rules
cd /ctf

## example rule
# alert tcp any any -> any any (msg: "Path Traversal-../"; flow:to_server; content: "../"; metadata: tag path_traversal; sid:1; rev: 1;)
### INSERT HERE RULES FOR SURICATA

## START SURICATA IPS
sudo systemctl stop suricata
screen -X -S surica quit || echo
screen -X -S capture quit || echo
sudo screen -dmS surica suricata -c /etc/suricata/suricata.yaml -q 0

## START CAPTURE
cd /ctf
cp /capture.py /ctf/tulip/services/
sudo screen -dmS capture python3 /ctf/tulip/services/capture.py $INTERFACE $USER

## START WEB MONITOR
cd /ctf/tulip
sudo usermod -aG docker $USER
sudo docker compose up
