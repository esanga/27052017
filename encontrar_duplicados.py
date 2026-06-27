#!/usr/bin/env python3
"""
Encontra arquivos duplicados em uma pasta (útil para analisar backup do celular).
Uso: python3 encontrar_duplicados.py /caminho/da/pasta
"""

import os
import sys
import hashlib
from collections import defaultdict


def hash_arquivo(caminho, bloco=65536):
    h = hashlib.md5()
    with open(caminho, "rb") as f:
        while chunk := f.read(bloco):
            h.update(chunk)
    return h.hexdigest()


def formatar_tamanho(bytes_):
    for unidade in ("B", "KB", "MB", "GB"):
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unidade}"
        bytes_ /= 1024
    return f"{bytes_:.1f} TB"


def encontrar_duplicados(raiz):
    tamanhos = defaultdict(list)

    print(f"Varrendo: {raiz}")
    total = 0
    for dirpath, _, arquivos in os.walk(raiz):
        for nome in arquivos:
            caminho = os.path.join(dirpath, nome)
            try:
                tamanho = os.path.getsize(caminho)
                if tamanho > 0:
                    tamanhos[tamanho].append(caminho)
                    total += 1
            except (OSError, PermissionError):
                pass

    print(f"Arquivos encontrados: {total}\n")

    # Agrupa por hash apenas arquivos com mesmo tamanho (otimização)
    hashes = defaultdict(list)
    candidatos = [c for c in tamanhos.values() if len(c) > 1]
    for grupo in candidatos:
        for caminho in grupo:
            try:
                h = hash_arquivo(caminho)
                hashes[h].append(caminho)
            except (OSError, PermissionError):
                pass

    duplicados = {h: caminhos for h, caminhos in hashes.items() if len(caminhos) > 1}

    if not duplicados:
        print("Nenhum arquivo duplicado encontrado.")
        return

    espaco_desperdicado = 0
    print(f"{'='*60}")
    print(f"DUPLICADOS ENCONTRADOS: {len(duplicados)} grupos\n")

    for h, caminhos in sorted(duplicados.items()):
        tamanho = os.path.getsize(caminhos[0])
        desperdicado = tamanho * (len(caminhos) - 1)
        espaco_desperdicado += desperdicado
        print(f"[{formatar_tamanho(tamanho)} cada | desperdício: {formatar_tamanho(desperdicado)}]")
        for c in caminhos:
            print(f"  {c}")
        print()

    print(f"{'='*60}")
    print(f"Espaço desperdicado em duplicatas: {formatar_tamanho(espaco_desperdicado)}")


if __name__ == "__main__":
    pasta = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isdir(pasta):
        print(f"ERRO: '{pasta}' não é uma pasta válida.")
        sys.exit(1)
    encontrar_duplicados(pasta)
