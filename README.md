# [BIX Tecnologia] Desafio Técnico - Vaga Engenheira(o) de Dados - Junior
### Candidato: Victor Buendia Cruz de Alvim

Este repositório tem a solução ao desafio técnico proposto para a vaga de Engenheiro de Dados Júnior.

## Visão Geral

![Diagrama](img/diagrama.png)

O projeto possui a arquitetura ilustrada acima, na qual dados de três fontes distintas (um banco PostGres, uma API e um arquivo Parquet) são ingeridos e transformados dentro da aplicação usando Python.

Depois, utilizando a biblioteca Pydantic, faz-se uma validação dos tipos de dado de cada modelo ingerido e, a partir dessa validação, os dados são inseridos no banco de dados local (que é um banco PostGres).

Nesta solução, utilizo o Pydantic para garantir a validação dos dados, mas isso só é possível considerando uma quantidade pequena de dados, como do desafio. Se fôssemos escalar essa validação, seria melhor colocá-la em uma etapa posterior ou então fazê-la em pequenos batches.

O pipeline está orquestrado com o Airflow, que executa a rotina de ingestão diariamente às 00:00 no horário UTC e toda a aplicação está containerizada utilizando Docker, para uma execução correta em qualquer máquina.

# Como executar o projeto

## Variáveis de ambiente

É preciso criar um arquivo `.env` com as variáveis de ambiente antes de iniciar o projeto.

```.env
BIX_DB_HOST=
BIX_DB_PORT=5432
BIX_DB_USER=
BIX_DB_PASS=
BIX_DB_NAME=postgres

BIX_ENDPOINT_FUNCIONARIOS=
BIX_ENDPOINT_CATEGORIAS=

DOCKER_DB_HOST=banco
DOCKER_DB_PORT=5432
```

Se estiver usando Linux, duas variáveis de ambiente serão adicionadas para que o Airflow tenha permissão sobre os arquivos. O comando abaixo já é automaticamente executado.

```bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

Todo esse processo já é feito automaticamente usando `make deploy`, mas é possível executá-lo com `make check-env`.

Basta um comando para subir todos os serviços:
	
```bash
make deploy
```

> *Observação:* É preciso ter instalado o Docker, Docker Compose (>=1.2.9) e Make na sua máquina.

Duas categorias de serviço subirão após o comando ser executado:

1. banco
2. airflow
   1. postgres
   2. redis
   3. airflow-web-server
   4. airflow-scheduler
   5. airflow-worker
   6. airflow-triggerer
   7. airflow-init
   8. airflow-cli
   9. flower
   
O serviço de `banco` possui o banco de dados PostGres para a ingestão dos dados, enquanto os serviços do `airflow` são relativos a seu funcionamento.

# Estrutura do código

Um resumo de como está organizada a estrutura de pasta pode ser vista abaixo:

```bash
.
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── config                    # AIRFLOW
│   └── airflow.cfg           # AIRFLOW
├── dags                      # AIRFLOW
│   ├── daily_ingestion.py    # AIRFLOW
│   └── dummy_dag.py          # AIRFLOW
├── docker-compose.yaml       # AIRFLOW
├── logs                      # AIRFLOW
├── plugins                   # AIRFLOW
├── postgres-db-volume        
├── postgres_data
├── requirements.txt
├── scripts                   # CÓDIGO
│   ├── api.py                # CÓDIGO: Classe para ingerir dados do PostGres e fazer requisição para a API
│   ├── connector.py          # CÓDIGO: Classe que cria conexão de dados com o PostGres
│   ├── environment.py        # CÓDIGO: Classe que gerencia as variáveis de ambiente
│   ├── helper.py             # CÓDIGO: Arquivo com funções para ajudar no processamento de dados
│   ├── inserter.py           # CÓDIGO: Classe para ingerir os dados no banco de dados destino
│   ├── models                # CÓDIGO
│   │   ├── categoria.py      # CÓDIGO: Modelo ORM de uma categoria
│   │   ├── funcionario.py    # CÓDIGO: Modelo ORM de um funcionário
│   │   └── venda.py          # CÓDIGO: Modelo ORM de uma venda
│   └── pipeline.py           # CÓDIGO: Arquivo com o pipeline
└── .env  
```

# Considerações

- Utilização de ORM no SQLAlchemy para padronização.
  - Pressupondo o uso de Data Mesh no qual o time de produto precisa se comprometer de entregar o dado de acordo com a ingestão, e portanto ajudar o time de data com schema evolution.
- Containerização usando Docker para isolamento de ambientes. Poderia ser evoluído com Kubernetes para gerenciamento dos containers, na qual as instâncias de container seriam efêmeras, apenas para realizar as tasks do Airflow, que funciona apenas como orquestrador.
- O banco de dados final é um PostGres em um container, mas poderia ser uma ferramenta especializada na Cloud (ex.: RDS), provisionado usando Terraform (IaC), ou também um data warehouse especializado (ex.: Redshift).
- Ingestão com Python e bibliotecas, mas poderia ser feito com alguma ferramenta como o AirByte, que é open-source.
- A transformação de dado está sendo feita com Python, mas também poderia ser feita com uma ferramenta específica, como o dbt.
- Validação de dados feita com a biblioteca Pydantic.
- Orquestração do pipeline feita usando Airflow.
