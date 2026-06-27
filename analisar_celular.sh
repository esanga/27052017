#!/usr/bin/env bash
# Analisa arquivos desnecessários no celular Android via ADB
# Requer: adb instalado e celular conectado com depuração USB ativada

set -euo pipefail

check_adb() {
    if ! command -v adb &>/dev/null; then
        echo "ERRO: adb não encontrado. Instale o Android SDK Platform Tools."
        exit 1
    fi

    if ! adb devices | grep -q "device$"; then
        echo "ERRO: Nenhum dispositivo conectado. Conecte o celular e ative a depuração USB."
        exit 1
    fi
}

echo "=== Verificando conexão com o celular ==="
check_adb

echo ""
echo "=== Espaço em disco ==="
adb shell df -h /sdcard 2>/dev/null || adb shell df /sdcard

echo ""
echo "=== Top 20 arquivos maiores em /sdcard ==="
adb shell find /sdcard -type f -printf '%s %p\n' 2>/dev/null \
    | sort -rn \
    | head -20 \
    | awk '{ size=$1; $1=""; printf "%8.1f MB  %s\n", size/1048576, $0 }'

echo ""
echo "=== Pastas que mais ocupam espaço ==="
adb shell du -sh /sdcard/* 2>/dev/null | sort -rh | head -20

echo ""
echo "=== Arquivos temporários e de cache ==="
TEMP_DIRS=(
    "/sdcard/Android/data/*/cache"
    "/sdcard/.thumbnails"
    "/sdcard/DCIM/.thumbnails"
    "/sdcard/WhatsApp/Media/.Statuses"
)
for dir in "${TEMP_DIRS[@]}"; do
    adb shell "du -sh $dir 2>/dev/null" || true
done

echo ""
echo "=== APKs baixados (instaladores) ==="
adb shell find /sdcard/Download -name "*.apk" -printf '%s %p\n' 2>/dev/null \
    | sort -rn \
    | awk '{ size=$1; $1=""; printf "%8.1f MB  %s\n", size/1048576, $0 }'

echo ""
echo "=== Vídeos (potencialmente grandes) ==="
adb shell find /sdcard -name "*.mp4" -o -name "*.mkv" -o -name "*.avi" 2>/dev/null \
    | head -30

echo ""
echo "Análise concluída. Revise os itens acima para liberar espaço."
