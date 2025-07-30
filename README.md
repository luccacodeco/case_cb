# Desafio de Engenharia de Dados

Este repositório contém as soluções dos desafios de engenharia de dados propostos, divididos em duas partes principais.

## Desafio 1 – ERP e Modelagem Relacional

Transformação de um JSON de pedidos de restaurante (ERP) em um modelo relacional.

### Estrutura
- desafio1/ERP.json → Exemplo da resposta da API
- desafio1/schema.json → Schema JSON para validação
- desafio1/docs/ → Explicações da estrutura e modelagem
- desafio1/sql/modelo_sql.sql → Criação das tabelas no banco
- desafio1/etl/ → Scripts de ETL:
  - etl_exemplo_csv.py → Geração de arquivos CSV
  - etl_exemplo_banco.py → Inserção em banco relacional
  - utils.py → Funções auxiliares (validação, conexão).
- desafio1/output_csv/ → Arquivos CSV gerados
- desafio1/README.md → Explicação da abordagem usada

## Desafio 2 – Armazenamento e Organização de APIs no Data Lake

Simulação de ingestão de 5 endpoints diferentes em um Data Lake estruturado por camadas.

### Estrutura
- desafio2/datalake/bronze/ → Dados brutos organizados por data e loja
  - bi/getFiscalInvoice/...
  - res/getGuestChecks/...
  - org/getChargeBack/...
  - trans/getTransactions/...
  - inv/getCashManagementDetails/...
- desafio2/datalake/silver/ → Dados normalizados por endpoint
  - guest_checks.csv
  - transactions.csv
  - charge_backs.csv
  - fiscal_invoices.csv
  - cash_management.csv
- desafio2/datalake/gold/
  - receita_por_loja.csv → Agregação final por data e loja
- desafio2/README.md → Explicação da abordagem usada
