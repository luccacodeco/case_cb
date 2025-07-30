# Desafio 2 – Engenharia de Dados

## **Objetivo**
Analisar e armazenar as respostas de 5 endpoints de APIs para uma rede de restaurantes, garantindo:
- Histórico confiável dos dados (auditoria e reprocessamento).
- Estrutura otimizada para consultas e relatórios.
- Capacidade de lidar com alterações de schema.

---

## **1. Por que armazenar as respostas das APIs?**
- **Histórico e auditoria:** Permite reprocessar e validar dados a qualquer momento.
- **Independência da API:** Não dependemos de disponibilidade online.
- **Controle de qualidade:** Detectar erros ou inconsistências nos dados de origem.
- **Base única de verdade (Data Lake):** Centraliza todos os dados de diferentes sistemas.

---

## **2. Estrutura do Data Lake**
O Data Lake está dividido em 3 camadas:
```
datalake/
  bronze/
    res/getGuestChecks/bus_dt=2024-07-01/store_id=001/response.json
    ...
  silver/
    guest_checks.csv
    transactions.csv
    ...
  gold/
    receita_por_loja.csv
```

### **Bronze Layer**
- Dados brutos (JSON) exatamente como retornados.
- Partições por **data (`busDt`)** e **loja (`storeId`)**.

### **Silver Layer**
- Dados normalizados (CSV/Parquet) para fácil consulta.
- Ex.: `guest_checks.csv` contém os checks do endpoint `getGuestChecks`.

### **Gold Layer**
- Dados agregados para BI e relatórios.
- Ex.: `receita_por_loja.csv` soma a receita total por loja e data.

---

## **3. Alterações de Schema**
Se a API alterar `guestChecks.taxes` para `guestChecks.taxation`:
- **Bronze:** Nada muda.
- **Silver:** Atualizamos o ETL para mapear `taxation → taxes`.
- **Gold:** Continua funcionando após a normalização.

---

## **4. Exemplo de Agregação**
```sql
-- Receita total por loja e data
SELECT busDt, storeId, SUM(chkTtl) AS receita_total
FROM guest_checks
GROUP BY busDt, storeId;
```
---

## **5. Próximos Passos**
- Automatizar ingestão
- Converter CSV para Parquet para consultas mais rápidas.
- Analisar métricas, criar dashboards.


# Explicação da Abordagem 

## 1. Camadas do Data Lake
- **Bronze:** Mantém os dados brutos (JSON).
- **Silver:** Converte dados em formato tabular (CSV/Parquet) para consultas SQL.
- **Gold:** Realiza agregações e métricas, preparando dados para dashboards.

## 2. Transformações
- **De JSON para CSV:** Campos aninhados (como `taxes` e `items`) são achatados em tabelas (ex: `guest_checks.csv`).
- **Agregações:** Para `receita_por_loja.csv`, aplicamos:
```sql
SELECT busDt, storeId, SUM(chkTtl) AS receita_total
FROM guest_checks
GROUP BY busDt, storeId;
```

## 3. Alterações de Schema
- Caso `guestChecks.taxes` seja renomeado para `guestChecks.taxation`, a Bronze não muda (mantemos como vem).
- No ETL da Silver, usamos lógica condicional:
```python
taxes = data.get("guestChecks", {}).get("taxation", data.get("guestChecks", {}).get("taxes", []))
```

## 4. Benefícios da Arquitetura
- Rápida localização de dados usando partições (`bus_dt` e `store_id`).
- Histórico completo preservado.
- Suporte a análises BI sem consultas complexas sobre JSON.
