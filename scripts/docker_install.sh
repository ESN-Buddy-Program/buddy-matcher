#!/bin/bash
# Install Docker based on the operating system, with checks to see if Docker is already installed

check_docker_installed() {
  if command -v docker >/dev/null 2>&1; then
    echo "Docker is already installed."
    exit 0
  fi
}

install_docker_mac() {
  echo "Installing Docker for macOS..."
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew is not installed. Please install Homebrew first: https://brew.sh/"
    exit 1
  fi
  brew install --cask docker
  open /Applications/Docker.app
}

install_docker_apt() {
  echo "Installing Docker for apt-based systems..."
  if ! command -v apt >/dev/null 2>&1; then
    echo "apt package manager not found. This script is meant for apt-based systems."
    exit 1
  fi
  sudo apt update
  sudo apt install -y docker.io
  sudo systemctl start docker
  sudo systemctl enable docker
}

install_docker_dnf() {
  echo "Installing Docker for dnf-based systems..."
  if ! command -v dnf >/dev/null 2>&1; then
    echo "dnf package manager not found. This script is meant for dnf-based systems."
    exit 1
  fi
  sudo dnf install -y docker-ce docker-ce-cli containerd.io
  sudo systemctl start docker
  sudo systemctl enable docker
}

install_docker_pacman() {
  echo "Installing Docker for pacman-based systems..."
  if ! command -v pacman >/dev/null 2>&1; then
    echo "pacman package manager not found. This script is meant for pacman-based systems."
    exit 1
  fi
  sudo pacman -Syu --noconfirm
  sudo pacman -S --noconfirm docker
  sudo systemctl start docker
  sudo systemctl enable docker
}

check_docker_installed # Check if Docker is already installed

case "$(uname)" in
  Darwin) install_docker_mac ;;
  *)
    if command -v apt >/dev/null 2>&1; then install_docker_apt; fi
    if command -v dnf >/dev/null 2>&1; then install_docker_dnf; fi
    if command -v pacman >/dev/null 2>&1; then install_docker_pacman; fi
    ;;
esac

docker pull python:3.10-slim
