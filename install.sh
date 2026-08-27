#!/usr/bin/env bash
#
# Installer das dotfiles
# Cria symlinks a partir deste repositório para $HOME.
# Arquivos existentes no destino são movidos para *.bak antes.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

step() { printf '\033[1;36m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m!!  %s\033[0m\n' "$*"; }

backup_and_link() {
    local src="$1" dst="$2"
    if [ -e "$dst" ] || [ -L "$dst" ]; then
        warn "backup de $dst -> $dst.bak"
        mv "$dst" "$dst.bak"
    fi
    ln -s "$src" "$dst"
    printf 'link  %s\n' "$dst"
}

link_entries() {
    local src_dir="$1" dst_dir="$2" name
    mkdir -p "$dst_dir"
    for entry in "$src_dir"/*; do
        [ -e "$entry" ] || continue
        name="$(basename "$entry")"
        backup_and_link "$entry" "$dst_dir/$name"
    done
}

[ -d "$REPO" ] || { echo "dotfiles nao encontrado em $REPO"; exit 1; }

step "Ligando configs do shell ($REPO/home -> ~)"
link_entries "$REPO/home" "$HOME"

step "Ligando ~/.config"
link_entries "$REPO/config" "$HOME/.config"

step "Ligando ~/.local/bin"
link_entries "$REPO/local/bin" "$HOME/.local/bin"

step "Ligando ~/.local/share"
link_entries "$REPO/local/share/icons" "$HOME/.local/share/icons"
link_entries "$REPO/local/share/fonts" "$HOME/.local/share/fonts"
link_entries "$REPO/local/share/color-schemes" "$HOME/.local/share/color-schemes"
link_entries "$REPO/local/share/themes" "$HOME/.local/share/themes"
link_entries "$REPO/local/share/aurorae" "$HOME/.local/share/aurorae"
link_entries "$REPO/local/share/wallpapers" "$HOME/.local/share/wallpapers"
link_entries "$REPO/local/share/neofetch" "$HOME/.local/share/neofetch"

for sub in plasmoids look-and-feel desktoptheme; do
    link_entries "$REPO/local/share/plasma/$sub" "$HOME/.local/share/plasma/$sub"
done

step "Pronto! Remova os .bak para desfazer ou restaure com git."