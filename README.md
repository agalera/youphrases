# youphrases

## install debian

```
echo "deb http://www.deb-multimedia.org jessie main non-free" >> /etc/apt/sources.list
apt-get update -y
apt-get install -y gcc
apt-get install -y deb-multimedia-keyring --force-yes
apt-get install -y ffmpeg --force-yes
apt-get install python3 python3-pip
pip3 install -r requirements.txt
```
## run docker
TODO
