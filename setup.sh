#!/usr/bin/env bash
# setup.sh - Install dependencies for InstaSpear on Kali Linux using apt

set -e

echo "[+] Updating package lists..."
sudo apt update

echo "[+] Installing required packages..."
sudo apt install -y \
    python3 \
    python3-pip \
    php \
    cloudflared \
    figlet \
    python3-termcolor \
    openssh-server


echo "[+] Compiling InstaSpear.py to InstaSpear.pyc..."
python3 -m py_compile InstaSpear.py
mv __pycache__/InstaSpear.cpython-*.pyc InstaSpear.pyc
rm -rf __pycache__
chmod a+x InstaSpear.pyc
echo "[+] Setup complete!"

# Create a hidden text file with author info
echo "created by Mr-Robot-ctrl" > .mr-robot-ctrl.txt

echo "[+] Setup complete!"
