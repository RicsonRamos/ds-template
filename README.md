# Data Science Project Template (Copier + uv)

[![Validate Template](https://github.com/RicsonRamos/ds-template/actions/workflows/validate-template.yml/badge.svg)](https://github.com/RicsonRamos/ds-template/actions/workflows/validate-template.yml)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted.json)](https://github.com/copier-org/copier)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checker: Pyright](https://img.shields.io/badge/type%20checker-pyright-green.svg)](https://microsoft.github.io/pyright/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Template de arquitetura modular, escalável e reproduzível para projetos de **Ciência de Dados, Machine Learning e MLOps**, baseado em **[Copier](https://copier.readthedocs.io/)**, **[uv](https://docs.astral.sh/uv/)**, **Ruff**, **Pyright** e **Pytest**.

Oferece suporte nativo a **3 Níveis de Complexidade Arquitetural (`project_level`)**, adaptando automaticamente pastas, scripts, endpoints de API, manifesto de dependências e contêinerização ao escopo do seu projeto.

---

## 📑 Sumário

- [Visão Geral & Decisões Arquiteturais](#-visão-geral--decisões-arquiteturais)
- [Arquitetura em 3 Níveis de Complexidade](#-arquitetura-em-3-níveis-de-complexidade)
- [Estrutura do Repositório do Template](#-estrutura-do-repositório-do-template)
- [Variáveis e Ciclo de Vida do Copier](#-variáveis-e-ciclo-de-vida-do-copier)
- [Estrutura dos Projetos Gerados](#-estrutura-dos-projetos-gerados)
- [Guia Rápido de Uso](#-guia-rápido-de-uso)
  - [1. Gerando um Novo Projeto](#1-gerando-um-novo-projeto)
  - [2. Publicando e Versionando o Template](#2-publicando-e-versionando-o-template)
  - [3. Atualizando Projetos Existentes (copier update)](#3-atualizando-projetos-existentes-copier-update)
- [Segurança & Auditoria de Tarefas (_tasks)](#-segurança--auditoria-de-tarefas-_tasks)
- [Governança e Reprodutibilidade de Dados](#-governança-e-reprodutibilidade-de-dados)
- [Qualidade de Código & CI/CD](#-qualidade-de-código--cicd)
  - [Pre-commit & Pre-push](#pre-commit--pre-push)
  - [GitHub Actions CI](#github-actions-ci)
- [Contêinerização de Produção com Docker & UV](#-contêinerização-de-produção-com-docker--uv)
- [Testes Locais do Template](#-testes-locais-do-template)

---

## 🏛️ Visão Geral & Decisões Arquiteturais

### 1. Copier vs. Cookiecutter: Por que Copier?
Diferente do Cookiecutter (que opera como gerador estático unidirecional), o **Copier** mantém o estado da geração gravado no arquivo de respostas (`.copier-answers.yml`). Isso confere diferenciais críticos:
- **Evolução Contínua (`copier update`):** Quando regras de linting, scripts de CI, hooks de pre-commit ou dependências base são aprimorados no template, projetos antigos podem receber as atualizações via algoritmo de *three-way merge* sem sobrescrever código de negócio ou análises já desenvolvidas.
- **Automação Pós-Geração (`_tasks`):** Execução determinística de comandos do sistema imediatamente após o scaffold (`git init`, `uv sync`, instalação de hooks do Git).
- **Estrutura Direta na Raiz (`_exclude`):** Todos os arquivos de template residem na raiz do repositório, com exclusão declarativa em `copier.yml` para metadados internos e renderização condicional baseada no nível escolhido.

### 2. uv: Ecossistema Python Unificado em Rust
- Gerenciamento ultrarrápido de dependências e ambientes virtuais (`.venv`).
- Resolução de dependências estrita via lockfile multiplataforma (`uv.lock`).
- Execução isolada de ferramentas sem necessidade de instalação global (`uvx`, `uv tool run`).

### 3. Stack de Engenharia de Software Aplicada a Dados
- **Build Backend:** `hatchling` (conforme PEP 517/PEP 621), com mapeamento explícito do pacote (`tool.hatch.build.targets.wheel.packages = ["src/{{ package_name }}"]`).
- **I/O Moderno com Parquet:** Suporte nativo a leitura/escrita de arquivos `.parquet` com `polars` e `pandas` (via `pyarrow>=18.0.0`).
- **Limpeza de Notebooks (`nbstripout`):** Higienização automática de saídas visuais, contagens de execução e dados sensíveis em notebooks `.ipynb` antes de cada commit.
- **Linter & Formatter:** `ruff` com 18 categorias de regras ativadas (incluindo `pandas-vet`, `flake8-bugbear`, `numpy-specific`, `security`, `import-sorting`), formatador determinístico e suporte nativo a Jupyter Notebooks (`*.ipynb`).
- **Tipagem Estática:** `pyright` e `ty` configurados em modo `standard`, garantindo rigor em pipelines e classes sem sobrecarregar a exploração em notebooks.
- **Testes:** `pytest` com `pytest-xdist`, configurado com `testpaths = ["tests"]` e `pythonpath = ["src"]`.

---

## 🎚️ Arquitetura em 3 Níveis de Complexidade

Nem todo projeto de dados requer uma API em contêiner ou modelos serializados. Por isso, o template oferece o seletor `project_level`:

| Recurso / Componente | Nível 1: Análise & EDA | Nível 2: DS & ML (Padrão) | Nível 3: MLOps & Produção |
| :--- | :---: | :---: | :---: |
| **Foco Principal** | Análise exploratória, dashboards, relatórios | Modelagem preditiva tabular, engenharia de features | Microsserviços de inferência, pipelines, contêineres |
| `data/01_raw`, `data/03_processed` | Sim | Sim | Sim |
| `data/02_interim`, `data/04_external` | Não | Sim | Sim |
| Diretório `models/` | Não | Sim | Sim |
| `notebooks/` & `reports/figures/` | Sim | Sim | Sim |
| `src/<pkg>/config.py` (caminhos pathlib) | Sim | Sim | Sim |
| `src/<pkg>/features.py` (Transformers) | Não | Sim | Sim |
| `src/<pkg>/train.py` (Pipeline de treino) | Não | Sim | Sim |
| `src/<pkg>/predict.py` (Inferência em lote) | Não | Sim | Sim |
| `src/<pkg>/api/` (FastAPI + Pydantic) | Não | Não | Sim |
| `Dockerfile` & `.dockerignore` | Não | Não | Sim |
| Testes unitários do modelo (`test_ml.py`) | Não | Sim | Sim |
| Testes de integração da API (`test_api.py`) | Não | Não | Sim |
| Bibliotecas: `scikit-learn`, `joblib` | Não | Sim | Sim |
| Bibliotecas: `fastapi`, `uvicorn`, `pydantic`, `mlflow` | Não | Não | Sim |

---

## 📂 Estrutura do Repositório do Template

```text
ds-template/
├── .dockerignore                               # Exclusões de build Docker (Nível 3)
├── .env.example                                # Variáveis de ambiente de exemplo
├── .github/
│   └── workflows/
│       ├── ci.yml.jinja                        # CI dos projetos gerados (setup-uv, checagens, Docker)
│       └── validate-template.yml               # CI do template gerador (testa níveis 1, 2 e 3 + Docker)
├── .gitignore                                  # Gitignore com exclusões específicas de Data Science
├── .pre-commit-config.yaml                     # Configuração de hooks git (nbstripout, ruff, pyright)
├── .python-version.jinja                       # Versão do Python selecionada
├── .vscode/
│   └── settings.json                           # Configurações do VS Code (Ruff format-on-save, Pyright)
├── Dockerfile.jinja                            # Dockerfile multi-stage de produção otimizado com UV (Nível 3)
├── README.md                                   # Documentação técnica do template gerador
├── README.md.jinja                             # README adaptativo do projeto gerado
├── copier.yml                                  # Manifesto do template (prompts, validações, excludes e _tasks)
├── data/
│   ├── 01_raw/.gitkeep                         # Dados brutos e imutáveis
│   ├── 02_interim/.gitkeep                     # Dados em estágios intermediários (Níveis 2 e 3)
│   ├── 03_processed/.gitkeep                   # Dados canônicos prontos para modelagem/consumo
│   └── 04_external/.gitkeep                    # Dados de terceiros ou fontes externas (Níveis 2 e 3)
├── models/.gitkeep                             # Modelos serializados (.joblib, .pt, .onnx) (Níveis 2 e 3)
├── notebooks/.gitkeep                          # Cadernos interativos de exploração
├── pyproject.toml.jinja                        # Manifesto PEP 621 com dependências dinâmicas por nível
├── reports/
│   └── figures/.gitkeep                        # Figuras, gráficos e relatórios visuais
├── src/
│   └── {{ package_name }}/                     # Pacote Python com nomenclatura dinâmica
│       ├── __init__.py                         # Inicialização do pacote
│       ├── config.py                           # Caminhos de filesystem centralizados com pathlib
│       ├── features.py                         # Pipelines de pré-processamento (Níveis 2 e 3)
│       ├── train.py.jinja                      # Script de treino baseline e serialização (Níveis 2 e 3)
│       ├── predict.py.jinja                    # Pipeline de inferência em lote (Níveis 2 e 3)
│       └── api/                                # Microsserviço FastAPI (Nível 3)
│           ├── __init__.py
│           ├── app.py.jinja                    # Endpoints /health e /predict com lifespan
│           └── schemas.py                      # Modelos Pydantic para I/O estrito
├── tests/
│   ├── __init__.py                             # Inicialização dos testes
│   ├── test_smoke.py.jinja                     # Teste de fumaça inicial
│   ├── test_ml.py.jinja                        # Testes das rotinas de ML (Níveis 2 e 3)
│   └── test_api.py.jinja                       # Testes de integração da API FastAPI (Nível 3)
└── {{ _copier_conf.answers_file }}.jinja       # Arquivo de estado para permitir copier update
```

---

## ⚙️ Variáveis e Ciclo de Vida do Copier

O arquivo `copier.yml` solicita as seguintes configurações no momento da criação:

| Variável | Tipo | Descrição | Validação / Default |
| :--- | :--- | :--- | :--- |
| `project_name` | `str` | Nome do repositório/projeto | Default: `"meu-projeto"`. Regex: `^[a-z][a-z0-9\-]*$` (letras minúsculas, números e hífens) |
| `package_name` | `str` | Nome do módulo Python em `src/` | Default: `project_name` com `-` substituído por `_`. Regex: `^[a-z][a-z0-9_]*$` |
| `project_level`| `str` | Nível de complexidade do projeto | Opções: `1` (Análise/EDA), `2` (DS & ML Tabular - Padrão), `3` (MLOps & Produção) |
| `description` | `str` | Descrição sucinta do projeto | Default: `"Projeto de Ciência de Dados e Machine Learning"` |
| `author_name` | `str` | Nome do autor/mantenedor | Default: `"Seu Nome"` |
| `author_email`| `str` | E-mail do autor | Default: `"seu@email.com"` |
| `python_version`| `str` | Versão do Python | Escolha entre `3.12` e `3.13` (Default: `3.12`) |

### Tarefas de Automação Pós-Geração (`_tasks`)
Ao concluir o preenchimento interativo, o Copier executa automaticamente em sequência dentro do diretório gerado:

```bash
git init -b main
uv sync --all-groups
git add .
uv tool run pre-commit install --install-hooks
uv tool run pre-commit install --hook-type pre-push
```

---

## 🏗️ Estrutura dos Projetos Gerados

Cada projeto gerado adota as melhores práticas de Engenharia de Dados e Ciência de Dados:

1. **Gestão de Dados em Camadas:**
   - `01_raw`: Camada imutável (fonte única da verdade original).
   - `02_interim`: Camada tratada intermediária.
   - `03_processed`: Datasets prontos para treinamento ou dashboards.
   - `04_external`: Metadados, dicionários ou tabelas auxiliares.
2. **Caminhos Robustos via `pathlib`:**
   O arquivo `src/<package_name>/config.py` centraliza todos os diretórios do projeto relativos a `PROJ_ROOT = Path(__file__).resolve().parents[2]`. Isso impede caminhos frágeis baseados no diretório atual de trabalho (`os.getcwd()`), funcionando de maneira homogênea tanto em scripts do terminal quanto dentro de notebooks ou subdiretórios.
3. **Ponto de Entrada CLI Automático:**
   Cada projeto gerado já vem com um CLI executável via `uv run <project_name>` mapeado para `<package_name>.config:info`.

---

## 🚀 Guia Rápido de Uso

### 1. Gerando um Novo Projeto

Não é necessário instalar o Copier globalmente. O comando `uvx` baixa e executa o Copier em ambiente isolado e temporário:

#### A partir de um repositório GitHub publicado:
```bash
uvx copier copy --trust gh:RicsonRamos/ds-template ./meu-projeto
```

#### A partir de um diretório local do template:
```bash
uvx copier copy --trust /caminho/para/ds-template ./meu-projeto
```

> **Atenção:** A flag `--trust` é **obrigatória** no Copier para permitir a execução de `_tasks` (scripts automatizados pós-criação). Sem `--trust`, o Copier bloqueia a execução de comandos do sistema por segurança.

### 2. Publicando e Versionando o Template

O Copier utiliza as **tags do Git** para identificar versões estáveis do template. Ao criar ou atualizar o template, publique-o com versionamento semântico:

```bash
git add .
git commit -m "feat: implement 3-level tiering architecture (EDA, DS/ML, MLOps)"
git tag v2.0.0
git push origin main --tags
```

### 3. Atualizando Projetos Existentes (`copier update`)

Se você adicionar uma nova biblioteca às dependências padrão, atualizar as regras do Ruff ou aprimorar o GitHub Actions no repositório `ds-template`:

```bash
uvx copier update --trust
```

O Copier lê o `.copier-answers.yml`, calcula o *diff* entre as versões do template e aplica as novidades automaticamente via 3-way merge, preservando seu código e customizações.

---

## 🔒 Segurança & Auditoria de Tarefas (`_tasks`)

Por segurança, o Copier requer a flag `--trust` para executar qualquer template que contenha diretivas `_tasks`. Isso garante que o usuário esteja ciente de que scripts do sistema operacional serão executados em sua máquina.

### Comandos Executados na Inicialização

O manifesto `copier.yml` deste repositório executa **estritamente** os 5 comandos a seguir:

| Ordem | Comando | Propósito |
| :---: | :--- | :--- |
| 1 | `git init -b main` | Inicializa o repositório Git local no branch padrão `main` |
| 2 | `uv sync --all-groups` | Cria o ambiente virtual `.venv` e resolve dependências gerando `uv.lock` |
| 3 | `git add .` | Adiciona os arquivos iniciais e o `uv.lock` ao índice do Git |
| 4 | `uv tool run pre-commit install --install-hooks` | Instala o hook de `pre-commit` e pré-baixa os ambientes isolados |
| 5 | `uv tool run pre-commit install --hook-type pre-push` | Registra a checagem de tipos (`pyright`) e testes (`pytest`) para o `git push` |

---

## 📊 Governança e Reprodutibilidade de Dados

A arquitetura de diretórios `data/` implementa o padrão industrial de segregação por ciclo de vida e imutabilidade:

```text
data/
├── 01_raw/          # IMUTÁVEL: Dumps brutos, snapshots de banco de dados, APIs externas. Nunca edite ou sobrescreva.
├── 02_interim/      # TRATADO: Dados intermediários normalizados, imputados ou enriquecidos.
├── 03_processed/    # CANÔNICO: Datasets prontos para treinamento de modelos, matrizes de features ou dashboards.
└── 04_external/     # EXTERNO: Dicionários de dados, tabelas de CEP/IBGE, metadados de domínio público.
```

### Boas Práticas de Reprodutibilidade
1. **Imutabilidade em `01_raw`:** Trate qualquer arquivo depositado nesta pasta como somente-leitura. Todo processamento deve gerar novos arquivos em `02_interim` ou `03_processed`.
2. **Formato Parquet Padronizado:** Utilize arquivos `.parquet` para I/O de dados colunares. Com `pyarrow>=18.0.0` no ambiente, tanto `pandas` (`df.to_parquet()`) quanto `polars` oferecem compressão Snappy rápida e preservação rigorosa de tipos de dados.
3. **Versionamento de Datasets:** O `.gitignore` ignora dados volumosos por padrão (mantendo apenas os `.gitkeep`). Para rastreamento de dados em equipe, recomenda-se conectar o repositório a uma ferramenta de data-versioning (como [DVC](https://dvc.org/) ou armazenamento em bucket S3/GCS com versionamento de objetos habilitado).

---

## 🛡️ Qualidade de Código & CI/CD

### Pre-commit & Pre-push

A configuração em `.pre-commit-config.yaml` divide as checagens em dois estágios:

- **Estágio `pre-commit` (rápido, a cada `git commit`):**
  - Remoção de espaços em branco no final de linhas (`trailing-whitespace`).
  - Ajuste de quebras de linha final de arquivo (`end-of-file-fixer`).
  - Validação sintática de arquivos YAML e TOML (`check-yaml`, `check-toml`).
  - Bloqueio de arquivos maiores que 1MB (`check-added-large-files`).
  - Detecção de marcadores de conflito do Git (`check-merge-conflict`).
  - Prevenção de conflito de caixa em sistemas de arquivos (`check-case-conflict`).
  - Limpeza automática de saídas visuais e dados sensíveis de notebooks Jupyter (`nbstripout`).
  - Linting e correção automática via `ruff`.
  - Formatação padronizada via `ruff-format`.

- **Estágio `pre-push` (profundo, a cada `git push`):**
  - Checagem estática de tipos com `pyright`.
  - Execução dos testes automatizados com `pytest`.

### GitHub Actions CI

O arquivo gerado em `.github/workflows/ci.yml` automatiza a validação em pull requests e no branch principal utilizando a action oficial `astral-sh/setup-uv@v5`:

1. Instalação do `uv` com cache habilitado.
2. Instalação da versão do Python definida no `.python-version`.
3. Sincronização determinística das dependências (`uv sync --all-groups`).
4. Verificação de lint (`uv run ruff check .`).
5. Verificação de formatação (`uv run ruff format --check .`).
6. Checagem de tipos (`uv run pyright`).
7. Execução dos testes (`uv run pytest`).
8. Validação de build da imagem Docker (quando `project_level == '3'`).

---

## 🐳 Contêinerização de Produção com Docker & UV

Para projetos de Nível 3 (MLOps & Produção), o template gera automaticamente um `Dockerfile` multi-stage altamente otimizado e um arquivo `.dockerignore` dedicado:

1. **Separação em Múltiplos Estágios (`Multi-Stage Build`):**
   - **Estágio 1 (Builder):** Baixa o binário do `uv` direto da imagem oficial (`ghcr.io/astral-sh/uv:latest`), copia manifestos e sincroniza o `.venv` de produção usando cache de montagem (`--mount=type=cache,target=/root/.cache/uv`).
   - **Estágio 2 (Runtime Final):** Imagem limpa (`python:{{ python_version }}-slim-bookworm`) sem ferramentas de build ou binários do uv, apenas o `.venv` final e código compilado.
2. **Cache Agressivo de Camadas:** A separação de cópia de `pyproject.toml`/`uv.lock` antes do código-fonte (`src/`) impede que alterações em scripts ou modelos invalidem o cache de download de dependências.
3. **Segurança (Princípio do Menor Privilégio):** O container executa sob o usuário não-root `appuser` (UID 1001).
4. **Execução Padronizada:** O comando de inicialização executa a API FastAPI pronta para tráfego via Uvicorn na porta 8000.

```bash
# Construir a imagem Docker do projeto
docker build -t meu-projeto:v1 .

# Executar o container
docker run --rm -p 8000:8000 --name meu-projeto-app meu-projeto:v1
```

---

## 🔬 Testes Locais do Template

Para validar e inspecionar o template antes de publicar novas alterações no Git:

```bash
# Nível 2 (Padrão: DS & ML Clássico)
uvx copier copy --trust --defaults -d project_level="2" . /tmp/test-project-lvl2
cd /tmp/test-project-lvl2
uv run pytest
uv run ruff check .
uv run pyright
uv run meu-projeto

# Nível 1 (Análise & EDA)
uvx copier copy --trust --defaults -d project_level="1" . /tmp/test-project-lvl1
cd /tmp/test-project-lvl1
uv run pytest

# Nível 3 (MLOps & Produção com Docker)
uvx copier copy --trust --defaults -d project_level="3" . /tmp/test-project-lvl3
cd /tmp/test-project-lvl3
uv run pytest
docker build -t test-mlops:ci .
```
