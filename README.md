# Data Science Project Template (Copier + uv)

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted.json)](https://github.com/copier-org/copier)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checker: Pyright](https://img.shields.io/badge/type%20checker-pyright-green.svg)](https://microsoft.github.io/pyright/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Template de arquitetura moderna, modular e reproduzível para projetos de **Ciência de Dados e Machine Learning**, baseado em **[Copier](https://copier.readthedocs.io/)**, **[uv](https://docs.astral.sh/uv/)**, **Ruff**, **Pyright** e **Pytest**.

---

## 📑 Sumário

- [Visão Geral & Decisões Arquiteturais](#-visão-geral--decisões-arquiteturais)
- [Estrutura do Repositório do Template](#-estrutura-do-repositório-do-template)
- [Variáveis e Ciclo de Vida do Copier](#-variáveis-e-ciclo-de-vida-do-copier)
- [Estrutura dos Projetos Gerados](#-estrutura-dos-projetos-gerados)
- [Guia Rápido de Uso](#-guia-rápido-de-uso)
  - [1. Gerando um Novo Projeto](#1-gerando-um-novo-projeto)
  - [2. Publicando e Versionando o Template](#2-publicando-e-versionando-o-template)
  - [3. Atualizando Projetos Existentes (copier update)](#3-atualizando-projetos-existentes-copier-update)
- [Qualidade de Código & CI/CD](#-qualidade-de-código--cicd)
  - [Pre-commit & Pre-push](#pre-commit--pre-push)
  - [GitHub Actions CI](#github-actions-ci)
- [Testes Locais do Template](#-testes-locais-do-template)

---

## 🏛️ Visão Geral & Decisões Arquiteturais

### 1. Copier vs. Cookiecutter: Por que Copier?
Diferente do Cookiecutter (que opera como gerador estático unidirecional), o **Copier** mantém o estado da geração gravado no arquivo de respostas (`.copier-answers.yml`). Isso confere um diferencial crítico:
- **Evolução Contínua (`copier update`):** Quando regras de linting, scripts de CI ou dependências base são aprimorados no template, projetos antigos podem receber as atualizações via algoritmo de *three-way merge* sem sobrescrever código de negócio ou análises já desenvolvidas.
- **Automação Pós-Geração (`_tasks`):** Execução determinística de comandos do sistema imediatamente após o scaffold (`git init`, `uv sync`, instalação de hooks do Git).
- **Subdiretório Isolado (`_subdirectory: template`):** Separa a definição do template (`copier.yml`) dos arquivos copiados, mantendo o repositório gerador limpo e evitando vazamento de metadados do gerador para os projetos finais.

### 2. uv: Ecossistema Python Unificado em Rust
- Gerenciamento ultrarrápido de dependências e ambientes virtuais (`.venv`).
- Resolução de dependências estrita via lockfile multiplataforma (`uv.lock`).
- Execução isolada de ferramentas sem necessidade de instalação global (`uvx`, `uv tool run`).

### 3. Stack de Engenharia de Software Aplicada a Dados
- **Build Backend:** `hatchling` (conforme PEP 517/PEP 621), com mapeamento explícito do pacote (`tool.hatch.build.targets.wheel.packages = ["src/{{ package_name }}"]`).
- **Linter & Formatter:** `ruff` com 18 categorias de regras ativadas (incluindo `pandas-vet`, `flake8-bugbear`, `numpy-specific`, `security`, `import-sorting`), formatador determinístico e suporte nativo a Jupyter Notebooks (`*.ipynb`).
- **Tipagem Estática:** `pyright` e `ty` configurados em modo `standard`, garantindo rigor em pipelines e classes sem sobrecarregar a exploração em notebooks.
- **Testes:** `pytest` com `pytest-xdist`, configurado com `testpaths = ["tests"]` e `pythonpath = ["src"]`.

---

## 📂 Estrutura do Repositório do Template

```text
ds-template/
├── copier.yml                                  # Manifesto do template (prompts, validações e _tasks)
├── README.md                                   # Documentação técnica do template
└── template/                                   # Raiz do projeto de Ciência de Dados a ser gerado
    ├── .github/
    │   └── workflows/
    │       └── ci.yml.jinja                    # Workflow GitHub Actions com setup-uv e checagens completas
    ├── .vscode/
    │   └── settings.json                       # Configurações do VS Code (Ruff format-on-save, Pyright)
    ├── data/
    │   ├── 01_raw/.gitkeep                     # Dados brutos e imutáveis
    │   ├── 02_interim/.gitkeep                 # Dados em estágios intermediários de limpeza
    │   ├── 03_processed/.gitkeep               # Dados canônicos prontos para modelagem/consumo
    │   └── 04_external/.gitkeep                # Dados de terceiros ou fontes externas
    ├── models/.gitkeep                         # Modelos serializados (.joblib, .pt, .onnx)
    ├── notebooks/.gitkeep                      # Cadernos interativos de exploração
    ├── reports/
    │   └── figures/.gitkeep                    # Figuras, gráficos e relatórios visuais
    ├── src/
    │   └── {{ package_name }}/                 # Pacote Python com nomenclatura dinâmica
    │       ├── __init__.py                     # Inicialização do pacote
    │       └── config.py                       # Caminhos de filesystem centralizados com pathlib
    ├── tests/
    │   ├── __init__.py                         # Inicialização dos testes
    │   └── test_smoke.py.jinja                 # Teste de fumaça inicial garantindo importabilidade
    ├── .env.example                            # Variáveis de ambiente de exemplo
    ├── .gitignore                              # Gitignore com exclusões específicas de Data Science
    ├── .pre-commit-config.yaml                 # Configuração de hooks git (pre-commit e pre-push)
    ├── .python-version.jinja                   # Posição da versão do Python selecionada
    ├── pyproject.toml.jinja                    # Manifesto PEP 621 com grupos dev e notebooks
    ├── README.md.jinja                         # README customizado do projeto criado
    └── {{ _copier_conf.answers_file }}.jinja   # Arquivo de estado para permitir copier update
```

---

## ⚙️ Variáveis e Ciclo de Vida do Copier

O arquivo `copier.yml` solicita as seguintes configurações no momento da criação:

| Variável | Tipo | Descrição | Validação / Default |
| :--- | :--- | :--- | :--- |
| `project_name` | `str` | Nome do repositório/projeto | Regex: `^[a-z][a-z0-9\-]+$` (apenas minúsculas, números e hífens) |
| `package_name` | `str` | Nome do módulo Python em `src/` | Default: `project_name` com `-` substituído por `_`. Validação: `^[a-z][a-z0-9_]+$` |
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

Essas tarefas inicializam o repositório Git no branch `main`, sincronizam todas as dependências gerando o `uv.lock`, colocam os arquivos sob monitoramento do Git e instalam os hooks de `pre-commit` e `pre-push`.

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
uvx copier copy --trust gh:SEU-USUARIO/ds-template ./meu-projeto
```

#### A partir de um diretório local do template:
```bash
uvx copier copy --trust /caminho/para/ds-template ./meu-projeto
```

> **Atenção:** A flag `--trust` é **obrigatória** no Copier para permitir a execução de `_tasks` (scripts automatizados pós-criação). Sem `--trust`, o Copier bloqueia a execução de comandos do sistema por segurança.

### 2. Publicando e Versionando o Template

O Copier utiliza as **tags do Git** para identificar versões estáveis do template. Ao criar ou atualizar o template, publique-o com versionamento semântico:

```bash
# Dentro do diretório ds-template
git init -b main
git add .
git commit -m "feat: initial Data Science template with uv, Ruff, Pyright and Copier"
git tag v1.0.0

# Conectar ao seu repositório remoto no GitHub
git remote add origin https://github.com/SEU-USUARIO/ds-template.git
git push -u origin main --tags
```

### 3. Atualizando Projetos Existentes (`copier update`)

Se você adicionar uma nova biblioteca às dependências padrão, atualizar as regras do Ruff ou aprimorar o GitHub Actions no repositório `ds-template`:

1. Faça o commit e publique uma nova tag no template (ex: `git tag v1.1.0 && git push --tags`).
2. Entre em qualquer projeto de Ciência de Dados criado anteriormente e execute:

```bash
uvx copier update --trust
```

O Copier lê o `.copier-answers.yml`, calcula o *diff* entre as versões do template e aplica as novidades automaticamente via 3-way merge, preservando seu código e customizações.

---

## 🛡️ Qualidade de Código & CI/CD

### Pre-commit & Pre-push

A configuração em `.pre-commit-config.yaml` divide as checagens em dois estágios:

- **Estágio `pre-commit` (rápido, a cada `git commit`):**
  - Remoção de espaços em branco no final de linhas (`trailing-whitespace`).
  - Ajuste de quebras de linha final de arquivo (`end-of-file-fixer`).
  - Validação sintática de arquivos YAML e TOML (`check-yaml`, `check-toml`).
  - Bloqueio de arquivos maiores que 50MB (`check-added-large-files`).
  - Detecção de marcadores de conflito do Git (`check-merge-conflict`).
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

---

## 🔬 Testes Locais do Template

Para validar e inspecionar o template antes de publicar novas alterações no Git:

```bash
# Gerar um projeto de teste em pasta temporária usando defaults
uvx copier copy --trust --defaults . /tmp/test-ds-project

# Verificar se o projeto gerado compila e passa nos testes
cd /tmp/test-ds-project
uv run pytest
uv run ruff check .
uv run pyright
uv run test-project   # Executa o CLI configurado
```
