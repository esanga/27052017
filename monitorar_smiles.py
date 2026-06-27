#!/usr/bin/env python3
"""
Monitor de bilhetes award em business no Smiles.

Verifica disponibilidade nas rotas GRU → LIS/CDG/AMS/MUC
e alerta quando encontrar assentos dentro do limite de milhas.

Como obter a x-api-key:
  1. Abra smiles.com.br e faça uma busca qualquer
  2. Abra DevTools → Network → filtre por "search"
  3. Copie o valor do header "x-api-key" de qualquer requisição
  4. Cole no campo API_KEY abaixo ou exporte: export SMILES_API_KEY=...
"""

import os
import time
import json
import smtplib
import itertools
import argparse
from datetime import date, timedelta
from email.mime.text import MIMEText

import requests

# ── Configuração ────────────────────────────────────────────────────────────

ROTAS = [
    ("GRU", "LIS"),
    ("GRU", "CDG"),
    ("GRU", "AMS"),
    ("GRU", "MUC"),
]

MAX_MILHAS = 400_000          # limite por trecho (ida)
CABINE = "business"
ADULTOS = 1

# Janela de datas a verificar (a partir de hoje)
DIAS_A_PARTIR_DE = 30         # começa daqui a N dias
JANELA_DIAS = 180             # verifica os próximos N dias

# Intervalo entre verificações completas (segundos)
INTERVALO_SEGUNDOS = 3600     # 1 hora

# API
API_KEY = os.getenv("SMILES_API_KEY", "")  # prefira variável de ambiente
BASE_URL = "https://api-air-flightsearch-prd.smiles.com.br/v1/airlines/search"

# Notificação por e-mail (opcional — deixe em branco para desativar)
EMAIL_DE      = os.getenv("EMAIL_DE", "")
EMAIL_PARA    = os.getenv("EMAIL_PARA", "")
EMAIL_SENHA   = os.getenv("EMAIL_SENHA", "")   # senha de app do Gmail
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587

# ── Helpers ─────────────────────────────────────────────────────────────────

def datas_para_verificar() -> list[str]:
    inicio = date.today() + timedelta(days=DIAS_A_PARTIR_DE)
    return [
        (inicio + timedelta(days=i)).isoformat()
        for i in range(JANELA_DIAS)
    ]


def buscar_voos(origem: str, destino: str, data: str) -> list[dict]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.smiles.com.br",
        "Referer": "https://www.smiles.com.br/",
        "region": "br",
        "channel": "web",
    }
    if API_KEY:
        headers["x-api-key"] = API_KEY

    params = {
        "adults": ADULTOS,
        "children": 0,
        "infants": 0,
        "tripType": 1,          # 1=ida simples, 2=ida e volta
        "originAirportCode": origem,
        "destinationAirportCode": destino,
        "departureDate": data,
        "cabinType": CABINE,
        "forceCongener": "false",
    }

    try:
        resp = requests.get(BASE_URL, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("requestedFlightSegmentList", [{}])[0].get("flightList", [])
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            print(f"  [!] Erro de autenticação — verifique SMILES_API_KEY")
        else:
            print(f"  [!] HTTP {e.response.status_code if e.response else '?'}: {origem}→{destino} {data}")
        return []
    except Exception as e:
        print(f"  [!] Erro: {e}")
        return []


def filtrar_award(voos: list[dict]) -> list[dict]:
    resultados = []
    for voo in voos:
        fare = voo.get("fare", {})
        milhas = fare.get("miles", 0) or 0
        if milhas and milhas <= MAX_MILHAS:
            resultados.append(voo)
    return resultados


def formatar_voo(voo: dict, origem: str, destino: str, data: str) -> str:
    fare      = voo.get("fare", {})
    milhas    = fare.get("miles", "?")
    taxas     = fare.get("airlineTax", "?")
    cia       = voo.get("airline", {}).get("code", "?")
    numero    = voo.get("flightNumber", "?")
    partida   = voo.get("departure", {}).get("date", "?")
    chegada   = voo.get("arrival", {}).get("date", "?")
    stops     = len(voo.get("stops", []))
    conexao   = f"{stops} conexão(ões)" if stops else "direto"
    return (
        f"  {origem}→{destino}  {data}  {cia}{numero}  "
        f"{milhas:,} milhas  R${taxas}  {conexao}  "
        f"({partida} → {chegada})"
    )


def enviar_email(assunto: str, corpo: str):
    if not all([EMAIL_DE, EMAIL_PARA, EMAIL_SENHA]):
        return
    msg = MIMEText(corpo, "plain", "utf-8")
    msg["Subject"] = assunto
    msg["From"]    = EMAIL_DE
    msg["To"]      = EMAIL_PARA
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.ehlo()
            s.starttls()
            s.login(EMAIL_DE, EMAIL_SENHA)
            s.sendmail(EMAIL_DE, EMAIL_PARA, msg.as_string())
        print("  [✓] E-mail enviado")
    except Exception as e:
        print(f"  [!] Falha ao enviar e-mail: {e}")


# ── Loop principal ───────────────────────────────────────────────────────────

def verificar_uma_vez(datas: list[str]) -> list[str]:
    encontrados = []
    for (origem, destino), data in itertools.product(ROTAS, datas):
        voos = buscar_voos(origem, destino, data)
        awards = filtrar_award(voos)
        for v in awards:
            linha = formatar_voo(v, origem, destino, data)
            print(f"  ✈ AWARD {linha}")
            encontrados.append(linha)
        time.sleep(1)   # respeita rate-limit
    return encontrados


def main():
    parser = argparse.ArgumentParser(description="Monitor de award Smiles biz GRU→Europa")
    parser.add_argument("--once", action="store_true", help="Executa uma vez e sai")
    args = parser.parse_args()

    if not API_KEY:
        print(
            "[AVISO] SMILES_API_KEY não definida.\n"
            "  Obtenha a chave em DevTools → Network no smiles.com.br\n"
            "  e exporte: export SMILES_API_KEY=sua_chave\n"
        )

    datas = datas_para_verificar()
    print(
        f"Monitorando {len(ROTAS)} rotas × {len(datas)} datas "
        f"| cabine={CABINE} | limite={MAX_MILHAS:,} milhas\n"
        f"Datas: {datas[0]} a {datas[-1]}\n"
    )

    rodada = 0
    while True:
        rodada += 1
        agora = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"── Rodada {rodada}  {agora} ──────────────────────────────")
        encontrados = verificar_uma_vez(datas)

        if encontrados:
            corpo = "\n".join(encontrados)
            print(f"\n[!] {len(encontrados)} award(s) encontrado(s)!")
            enviar_email(
                f"[Smiles] {len(encontrados)} award biz GRU→Europa ≤{MAX_MILHAS//1000}k mi",
                f"Awards encontrados em {agora}:\n\n{corpo}"
            )
        else:
            print("  Nenhum award dentro do limite nesta rodada.")

        if args.once:
            break

        proxima = time.strftime("%H:%M:%S", time.localtime(time.time() + INTERVALO_SEGUNDOS))
        print(f"\nPróxima verificação às {proxima}. Ctrl+C para parar.\n")
        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()
