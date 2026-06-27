# Ferramentas para limpar arquivos desnecessários do celular

Dois scripts para identificar o que está ocupando espaço no seu Android.

## 1. Análise direta via ADB (`analisar_celular.sh`)

Conecta ao celular pelo cabo USB e gera um relatório de:
- Espaço total em disco
- 20 arquivos maiores
- Pastas que mais ocupam espaço
- Caches e arquivos temporários
- APKs baixados
- Vídeos

**Pré-requisitos:**
- `adb` instalado ([Platform Tools](https://developer.android.com/studio/releases/platform-tools))
- Celular conectado por USB com **Depuração USB** ativada (Configurações → Opções do desenvolvedor)

**Como usar:**
```bash
chmod +x analisar_celular.sh
./analisar_celular.sh
```

---

## 2. Encontrar duplicados (`encontrar_duplicados.py`)

Varre uma pasta (por exemplo, um backup do celular no computador) e lista todos os arquivos duplicados, mostrando quanto espaço está sendo desperdiçado.

**Pré-requisitos:** Python 3.8+

**Como usar:**
```bash
python3 encontrar_duplicados.py /caminho/para/backup
```

---

## Dicas rápidas para liberar espaço sem ferramentas

| O que limpar | Onde fica (Android) |
|---|---|
| Cache dos apps | Configurações → Apps → [app] → Armazenamento → Limpar cache |
| Downloads antigos | Gerenciador de arquivos → Downloads |
| Fotos duplicadas | Google Fotos → Utilitários → Liberar espaço |
| Status do WhatsApp | WhatsApp/Media/.Statuses |
| APKs baixados | Downloads → arquivos `.apk` |
| Vídeos longos | DCIM/Camera ou WhatsApp/Media/WhatsApp Video |
