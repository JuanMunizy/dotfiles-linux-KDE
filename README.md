# dotfiles

Configurações do meu CachyOS (Arch) com KDE Plasma 6 — ricing estilo Lain/Monochrome.

## Conteúdo

```
home/            -> ~/        (.zshrc, .bashrc, .bash_profile)
config/          -> ~/.config (KDE/Plasma, Alacritty, Kitty, Neofetch, CAVA, micro,
                               Kvantum, Klassy, MangoHud, vkBasalt, GTK, fontconfig...)
local/bin/       -> ~/.local/bin (scripts: oled-like-setup, gaming-sysctl, steam-performance)
local/share/     -> ~/.local/share (wallpapers, widgets, temas, ícones, fontes)
```

### Temas
- **GTK/Qt/Kvantum:** Monochrome
- **Plasma (look-and-feel + desktoptheme):** Nothing, Monochrome, blackglass
- **Janelas (Klassy):** Monochrome
- **Ícones:** YAMIS — **Cursor:** WhiteSur-cursors
- **Fontes:** Fira Sans, Zilla Slab, Mom's Typewriter, Love Letter

### Widgets / plasmoids
Hiragana.Calendar, org.ruiny.NowPlaying, luisbocanegra.video.wallpaper, com.axzoros.yorhahud,
KdeControlStation, luisbocanegra.panel.colorizer, apdatifier, catwalkr, audio.visualizer,
Minimal.chaac.weather, thermalmonitor, CircleClock, stdout, spotify.

### Wallpapers
- `wallhaven-gwd5ee_1920x1080.png` (desktop)
- `silver-haired-warrior-live-wallpaper.mp4` (live wallpaper 94 MB)
- pacotes `Nothing`, `BlackGlass` e `Arch*` em `local/share/wallpapers/`
- imagem do neofetch em `local/share/neofetch/wall.png`

## Instalação

```bash
git clone https://github.com/<seu-user>/dotfiles.git ~/dotfiles
cd ~/dotfiles
bash install.sh
```

O script move o que já existir para `*.bak` e cria symlinks para o repositório.
Dependências (Apps, paru/pacman, tema Monochrome, ícones YAMIS, etc.) precisam estar instaladas.

> Nota: o vídeo de 94 MB ultrapassa 50 MB — o GitHub exibe um aviso mas aceita o push.

## O que ficou de fora (intencional)

- **Segredos/contas:** Discord, Vencord, Vesktop, Heroic, Lutris, qBittorrent, Steam, Wine, config.json (token).
- **Grande demais:** GIFs do Lain (~113 MB), pacotes de ícones não usados (Cawnonical, Breeze-Blue-Light, BRIT, Simply-Night-Blue-Circles, YaruPlasma-Dark, shelly-icons), VS Code (`~/.config/Code`, 225 MB), hidra AppImage.
- **Cache/estado:** `.cache`, `.oh-my-zsh` (gerenciado pelo próprio OMZ), `.bun`, `.cargo`, etc.