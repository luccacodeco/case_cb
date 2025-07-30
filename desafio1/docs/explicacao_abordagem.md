# Abordagem e Justificativas

## 1. Objetivo
O objetivo é transformar os dados brutos de pedidos do ERP (no formato JSON) em **tabelas relacionais normalizadas**, de forma que possam ser facilmente consultadas, agregadas e analisadas em contextos como relatórios de vendas, cálculos de impostos, controle de pedidos e integrações com BI.

---

## 2. Princípios de Modelagem
- **Normalização**:  
  Separar entidades em tabelas específicas para evitar redundância e inconsistências. Por exemplo:
  - `guest_checks` representa o pedido.
  - `taxes` armazena os impostos relacionados a cada pedido.
  - `detail_lines` representa cada item do pedido.
  - `menu_items` guarda informações do item do cardápio.

- **Relacionamentos 1:N**:  
  Um `guest_check` pode ter vários `detail_lines` e cada `detail_line` pode estar ligado a um `menu_item`.  
  Isso foi mantido com chaves estrangeiras (`guestCheckId`, `guestCheckLineItemId`).

- **Chaves naturais**:  
  Os IDs vindos do ERP (`guestCheckId` e `guestCheckLineItemId`) foram mantidos como **PRIMARY KEY**, evitando duplicação de dados e garantindo consistência entre sistemas.

- **Tipos de dados adequados**:  
  - Valores monetários: `NUMERIC(12,2)` para evitar problemas de arredondamento.
  - Datas e horários: `DATE` e `TIMESTAMP` para possibilitar filtros por tempo e análises temporais.
  - Campos booleanos (`clsdFlag`, `modFlag`) para facilitar queries simples (por exemplo, pedidos abertos/fechados).

---

## 3. ETL (Extract, Transform, Load)
- **Extract**:  
  O `ERP.json` é lido e validado contra um **JSON Schema**, garantindo que a estrutura do arquivo está correta antes de processar.

- **Transform**:  
  Os dados são “achatados” (normalizados) usando `pandas.json_normalize`, gerando tabelas intermediárias para `guest_checks`, `taxes`, `detail_lines` e `menu_items`.

- **Load**:  
  - Para este desafio, o ETL pode salvar em **CSV** (para visualização rápida) ou **inserir em um banco relacional** já existente usando **SQLAlchemy**.
  - Caso o dado já exista, o `guestCheckId` é usado como referência para evitar inserções duplicadas (em um ambiente real, seria usado `UPSERT`).

---

## 4. Boas Práticas Aplicadas
- **Validação com JSON Schema**:  
  Antes da transformação, o arquivo `ERP.json` é validado usando a biblioteca `jsonschema`, garantindo que campos obrigatórios e tipos estão corretos. Isso evita falhas em produção.

- **.env para credenciais**:  
  Informações sensíveis (como `DATABASE_URL`) são lidas de variáveis de ambiente via `python-dotenv`, em vez de serem hardcoded no código.

- **Separação em módulos (`utils.py`)**:  
  Funções auxiliares (validação e conexão) ficam isoladas para tornar o código mais limpo e reutilizável.

- **Logging e CLI**:  
  O script `etl_exemplo.py` utiliza `argparse` para permitir rodar etapas separadas (`--validate`, `--csv`, `--load`), simulando pipelines reais.

---

## 5. Por que esse modelo faz sentido para restaurantes?
- Cada **pedido (`guest_check`)** pode conter:
  - Diversos **itens de menu (`menu_items`)**,  
  - Diversas **linhas de detalhe (`detail_lines`)** (por exemplo, bebidas, pratos principais, sobremesas),
  - Vários **impostos (`taxes`)** aplicados (por estado, município ou tipo de produto).

- Essa modelagem permite responder perguntas como:
  - **Qual o total de vendas e impostos por dia?**
  - **Quais os itens de menu mais vendidos?**
  - **Quanto de desconto foi aplicado em determinado período?**
  - **Qual foi a média de clientes por mesa e ticket médio?**

---

## 6. Extensibilidade
No futuro, se `detailLines` também incluir objetos como `discount`, `serviceCharge`, `tenderMedia` ou `errorCode`, basta criar tabelas adicionais (`detail_line_discounts`, `detail_line_service_charges`, etc.) **sem alterar a estrutura principal**.

---

## 7. Possíveis Melhorias Futuras
- Implementar **particionamento por data** nas tabelas para melhorar performance em consultas com grandes volumes.
- Criar **índices** em campos como `opnBusDt` (data de abertura) para otimizar consultas por períodos.

