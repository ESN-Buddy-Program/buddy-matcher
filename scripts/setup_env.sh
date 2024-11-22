#!/bin/bash
# Installs required system dependencies based on the operating system

ensure_mac_brew(){
  if ! command -v brew > /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  brew update
}

install_python_mac(){
  ensure_mac_brew
  command -v python3.10 > /dev/null && return
  brew install python@3.10
}

install_python_apt(){
  sudo apt update
  sudo apt install -y python3.10
}

install_python_dnf(){
  sudo dnf install -y python3.10
}

install_python_pacman(){
  sudo pacman -S --noconfirm python3.10
}

ensure_python(){
  case "$(uname)" in
    Darwin) install_python_mac ;;
    *)
      if command -v apt >/dev/null 2>&1; then install_python_apt; fi
      if command -v dnf >/dev/null 2>&1; then install_python_dnf; fi
      if command -v pacman >/dev/null 2>&1; then install_python_pacman; fi
  esac
}

if [ "$(id -u)" -eq 0 ]; then
  echo "This script should not be run as root or with sudo. Exiting."
  exit 1
fi

ensure_python
