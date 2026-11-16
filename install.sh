#!/bin/bash
echo "====================================================="
echo "   🃏 INSTALLATEUR INTELLIGENT SHACOMARUX 🃏         "
echo "====================================================="

MISSING=()
for tool in python3 nmap ffuf curl; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "✅ $tool : déjà installé"
    else
        echo "❌ $tool : manquant"
        MISSING+=("$tool")
    fi
done

if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ python3-tk : déjà installé"
else
    echo "❌ python3-tk : manquant"
    MISSING+=("python3-tk")
fi

if [ ${#MISSING[@]} -gt 0 ]; then
    echo ""
    echo "[*] Installation automatique des outils manquants : ${MISSING[*]}..."
    sudo apt update && sudo apt install -y "${MISSING[@]}"
else
    echo ""
    echo "🎉 Tous les outils système sont déjà installés !"
fi

if [ ! -f ~/rockyou.txt ] && [ ! -f /usr/share/wordlists/rockyou.txt ]; then
    echo "[*] Téléchargement de rockyou.txt..."
    U="https://github.com"
    curl -sL "$U" -o ~/rockyou.txt
else
    echo "✅ rockyou.txt : prêt"
fi

DIR="$(cd "$(dirname "$0")" && pwd)"
DESK=$(xdg-user-dir DESKTOP)
chmod +x "$DIR/shacomarux.py"

cat << DESKTOP > "$DESK/ShacoMarux.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=ShacoMarux
Comment=Outil d'audit réseau et web (Shaco Edition)
Exec=python3 $DIR/shacomarux.py
Icon=$DIR/shaco.png
Terminal=false
Categories=Utility;Security;
DESKTOP

chmod +x "$DESK/ShacoMarux.desktop"
gio set "$DESK/ShacoMarux.desktop" metadata::trusted true 2>/dev/null || true

echo ""
echo "====================================================="
echo "🃏 ShacoMarux est prêt ! Lancez-le depuis votre Bureau."
echo "====================================================="
