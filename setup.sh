
#!/usr/bin/env bash
# setup.sh - Cross-platform dependency installer for InstaSpear
set -e

# ---------------------------
# Dependency lists
# ---------------------------
REQUIRED_PKGS=(python3 python3-pip php figlet)
PYTHON_PKGS=(termcolor)

# ---------------------------
# Installers for each platform
# ---------------------------
install_debian() {
    echo "[+] Detected Debian/Ubuntu/Kali. Using apt."
    sudo apt update
    sudo apt install -y "${REQUIRED_PKGS[@]}" python3-termcolor cloudflared openssh-server
}

install_arch() {
    echo "[+] Detected Arch Linux. Using pacman."
    sudo pacman -Sy --noconfirm "${REQUIRED_PKGS[@]}" cloudflared openssh
    sudo pip install "${PYTHON_PKGS[@]}"
}

install_fedora() {
    echo "[+] Detected Fedora. Using dnf."
    sudo dnf install -y "${REQUIRED_PKGS[@]}" cloudflared openssh-server
    sudo pip3 install "${PYTHON_PKGS[@]}"
}

install_macos() {
    echo "[+] Detected macOS. Using Homebrew."
    if ! command -v brew >/dev/null; then
        echo "[!] Homebrew not found. Please install Homebrew first: https://brew.sh/"
        exit 1
    fi
    brew update
    brew install python php figlet cloudflared openssh
    pip3 install --user "${PYTHON_PKGS[@]}"
}

install_termux() {
    echo "[+] Detected Termux environment. Using pkg."
    pkg update -y
    pkg install -y python python-pip php figlet openssh
    # cloudflared may not be available in all Termux repos
    if pkg install -y cloudflared; then
        echo "[+] cloudflared installed."
    else
        echo "[!] cloudflared not available in your Termux repo. Please install manually if needed."
    fi
    pip install --user termcolor
}

# ---------------------------
# OS Detection and Dispatch
# ---------------------------
echo "[+] Detecting OS..."
OS="$(uname -s)"

if [ -n "$PREFIX" ] && [ -x "$(command -v termux-info 2>/dev/null)" ]; then
    # Termux environment
    install_termux
else
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    else
        DISTRO=""
    fi
    case "$OS" in
        Linux)
            case "$DISTRO" in
                ubuntu|debian|kali)
                    install_debian ;;
                arch)
                    install_arch ;;
                fedora)
                    install_fedora ;;
                *)
                    echo "[!] Unsupported Linux distribution: $DISTRO"
                    echo "[!] Please install dependencies manually."
                    exit 1 ;;
            esac
            ;;
        Darwin)
            install_macos ;;
        *)
            echo "[!] Unsupported OS: $OS"
            echo "[!] Please install dependencies manually."
            exit 1 ;;
    esac
fi

# ---------------------------
# Post-install steps
# ---------------------------
echo "[+] Compiling InstaSpear.py to InstaSpear.pyc..."
python3 -m py_compile InstaSpear.py
mv __pycache__/InstaSpear.cpython-*.pyc InstaSpear.pyc
rm -rf __pycache__
chmod a+x InstaSpear.pyc

# Create a hidden text file with author info
echo "created by Mr-Robot-ctrl" > .mr-robot-ctrl.txt

echo "[+] Setup complete!"

echo "[+] Setup complete!"
