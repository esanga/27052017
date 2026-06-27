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

# Alerta por e-mail (opcional — use senha de app do Gmail)
export EMAIL_DE=seu@gmail.com
export EMAIL_PARA=destino@email.com
export EMAIL_SENHA=senha_de_app

# Roda em loop (1x/hora)
python3 monitorar_smiles.py

# Ou apenas uma verificação
python3 monitorar_smiles.py --once
```

### Como obter a x-api-key do Smiles

1. Acesse [smiles.com.br](https://www.smiles.com.br) e faça uma busca de voo
2. Abra o **DevTools** (F12) → aba **Network**
3. Filtre por `search` ou `airlines`
4. Clique numa requisição para `api-air-flightsearch-prd.smiles.com.br`
5. Copie o valor do header `x-api-key`

### Ajustes no script

| Variável              | Arquivo              | Descrição                          |
|-----------------------|----------------------|------------------------------------|
| `MAX_MILHAS`          | `monitorar_smiles.py`| Teto de milhas por trecho          |
| `DIAS_A_PARTIR_DE`    | `monitorar_smiles.py`| Início da janela de datas          |
| `JANELA_DIAS`         | `monitorar_smiles.py`| Quantos dias à frente verificar    |
| `INTERVALO_SEGUNDOS`  | `monitorar_smiles.py`| Frequência do loop (padrão: 1h)    |

---

## Notas gerais

- Awards GRU→Europa biz via Smiles costumam usar **Air France, Lufthansa, TAP ou Turkish** como parceiras
- A Smiles cobra taxas em R$ (STPC) — verifique se o cartão cobre
- O limite de 400k mi cobre rotas como GRU→CDG direto (AF) que giram em ~110k–130k mi/trecho em biz
- Validade das milhas Smiles: 24 meses (prorrogável com transações)
- Melhor disponibilidade costuma aparecer com **330–180 dias de antecedência** ou **próximos 14 dias** (last-minute)
