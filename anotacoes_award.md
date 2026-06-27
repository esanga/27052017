# Bilhetes Award Smiles — Europa em Business

## Critérios de busca

| Campo           | Valor                              |
|-----------------|------------------------------------|
| Origem          | GRU (São Paulo – Guarulhos)        |
| Destinos        | LIS · CDG · AMS · MUC             |
| Cabine          | Business                           |
| Limite de milhas| até 400.000 por trecho (ida)       |
| Programa        | Smiles (GOL)                       |

---

## Registros de disponibilidade

<!-- Adicione aqui cada vez que encontrar disponibilidade -->

| Data registro | Data voo | Rota | Cia | Voo | Milhas | Taxas (R$) | Conexões | Observações |
|---------------|----------|------|-----|-----|--------|------------|----------|-------------|
|               |          |      |     |     |        |            |          |             |

---

## Dicas de uso

### Monitoramento automático

```bash
# Instala dependências
pip install requests

# Define a chave da API (obtida no DevTools do smiles.com.br)
export SMILES_API_KEY=sua_chave_aqui

# ── Canal Telegram (recomendado) ──────────────────────────────────────────
export TELEGRAM_TOKEN=seu_token_do_botfather
export TELEGRAM_CHAT_ID=seu_chat_id

# ── Canal WhatsApp via CallMeBot ──────────────────────────────────────────
export CALLMEBOT_PHONE=5511999999999   # DDI + DDD + número, sem +
export CALLMEBOT_APIKEY=sua_apikey_callmebot

# ── Canal e-mail (opcional) ───────────────────────────────────────────────
export EMAIL_DE=seu@gmail.com
export EMAIL_PARA=destino@email.com
export EMAIL_SENHA=senha_de_app       # senha de app do Gmail

# Roda em loop (1x/hora) — dispara em todos os canais configurados
python3 monitorar_smiles.py

# Ou apenas uma verificação
python3 monitorar_smiles.py --once
```

### Como configurar o Telegram

1. Fale com **@BotFather** no Telegram → `/newbot` → siga as instruções
2. Copie o **token** (formato `123456:ABC-...`)
3. Envie qualquer mensagem para o seu bot
4. Acesse `https://api.telegram.org/bot<TOKEN>/getUpdates` no navegador
5. Copie o valor de `result[0].message.chat.id` → esse é o `TELEGRAM_CHAT_ID`

### Como configurar o WhatsApp (CallMeBot)

1. Salve o número **+34 644 59 78 46** nos seus contatos
2. Envie a mensagem: `I allow callmebot to send me messages`
3. Em alguns segundos você receberá a `apikey` por WhatsApp
4. Use o seu número no formato internacional sem `+` (ex: `5511999887766`)

### Como obter a x-api-key do Smiles

1. Acesse [smiles.com.br](https://www.smiles.com.br) e faça uma busca de voo
2. Abra o **DevTools** (F12) → aba **Network**
3. Filtre por `search` ou `airlines`
4. Clique numa requisição para `api-air-flightsearch-prd.smiles.com.br`
5. Copie o valor do header `x-api-key`

### Ajustes no script

| Variável de ambiente  | Descrição                                        |
|-----------------------|--------------------------------------------------|
| `SMILES_API_KEY`      | Chave da API do Smiles (DevTools → Network)      |
| `TELEGRAM_TOKEN`      | Token do bot (@BotFather)                        |
| `TELEGRAM_CHAT_ID`    | ID do chat Telegram                              |
| `CALLMEBOT_PHONE`     | Número WhatsApp com DDI (sem `+`)                |
| `CALLMEBOT_APIKEY`    | Chave CallMeBot recebida por WhatsApp            |
| `EMAIL_DE`            | Remetente Gmail                                  |
| `EMAIL_PARA`          | Destinatário e-mail                              |
| `EMAIL_SENHA`         | Senha de app do Gmail                            |

| Variável no script    | Descrição                                        |
|-----------------------|--------------------------------------------------|
| `MAX_MILHAS`          | Teto de milhas por trecho                        |
| `DIAS_A_PARTIR_DE`    | Início da janela de datas (dias a partir de hoje)|
| `JANELA_DIAS`         | Quantos dias à frente verificar                  |
| `INTERVALO_SEGUNDOS`  | Frequência do loop (padrão: 1h)                  |

---

## Notas gerais

- Awards GRU→Europa biz via Smiles costumam usar **Air France, Lufthansa, TAP ou Turkish** como parceiras
- A Smiles cobra taxas em R$ (STPC) — verifique se o cartão cobre
- O limite de 400k mi cobre rotas como GRU→CDG direto (AF) que giram em ~110k–130k mi/trecho em biz
- Validade das milhas Smiles: 24 meses (prorrogável com transações)
- Melhor disponibilidade costuma aparecer com **330–180 dias de antecedência** ou **próximos 14 dias** (last-minute)
