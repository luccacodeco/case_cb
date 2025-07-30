# Desafio 1 - Engenharia de Dados (Profissional)

Este projeto contém a solução para o **Desafio 1** do desafio de engenharia de dados.

## Estrutura

- **ERP.json**: Arquivo original da API ERP.
- **schema.json**: JSON Schema para validação do ERP.json.
- **docs/**:
  - `esquema_json.md`: Esquema simplificado do JSON.
  - `explicacao_abordagem.md`: Justificativa da modelagem.
- **sql/**:
  - `modelo_sql.sql`: DDL para criação das tabelas no banco.
- **etl/**:
  - `etl_exemplo_banco.py`: Script de ETL que lê o ERP.json e insere no banco.
  - `etl_exemplo_csv.py`: Script de ETL que lê o ERP.json e insere em arquivos CSVs.
  - `utils.py`: Funções auxiliares (validação, conexão).
- **requirements.txt**: Dependências para rodar o ETL.

## Como usar
Instale as dependências:
```bash
pip install -r requirements.txt
```
### Validar o JSON
    ```bash
    python desafio1/etl/etl_exemplo_banco.py --validate
    ``` 
ou
    ```bash
    python desafio1/etl/etl_exemplo_csv.py --validate
    ``` 
### Carregar dados em CSVs
1. Rode:
   ```bash
   python desafio1/etl/etl_exemplo_csv.py --csv
   ```

### Carregar dados no banco
1. Configure as credenciais no arquivo `.env`:
   ```
   DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/meubanco
   ```

2. Rode:
   ```bash
   python desafio1/etl/etl_exemplo_banco.py --load
   ```

## Objetivo
Transformar e validar os dados de pedidos do ERP em tabelas normalizadas, prontas para análises de BI.
