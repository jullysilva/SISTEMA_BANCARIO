# Sistema Bancário

🇧🇷 Português | [🇺🇸 English](README.en.md)

Sistema bancário de terminal em **Python**, desenvolvido em etapas nos desafios da [DIO](https://www.dio.me/). Cada arquivo representa uma evolução do mesmo sistema, aplicando um novo conceito da linguagem.

## Funcionalidades

- Cadastro de clientes (CPF, nome, data de nascimento e endereço)
- Criação e listagem de contas correntes (agência `0001`)
- Depósito, saque e extrato
- Regras de saque: limite de **R$ 500,00** por operação e **3 saques** por dia

## Desafios

| Arquivo | Conceitos aplicados |
|---|---|
| `1#desafio-estrutura-de-dados.py` | Listas, dicionários e funções com argumentos posicionais (`/`) e nomeados (`*`) |
| `2#desafio-decoradores-geradores-iteradores.py` | Decorador de log de transações, gerador de relatórios e iterador de contas |
| `3#desafio-manipulando-arquivos.py` | Gravação do log de transações em `log.txt` |
| `4#desafio-gerenciamento-pacotes.py` | Organização do código pensando em pacotes e dependências |

## Como rodar

Pré-requisito: **Python 3.8+**. Não há dependências externas.

```bash
python "1#desafio-estrutura-de-dados.py"
```

Troque o nome do arquivo para executar os outros desafios. O menu interativo aparece no terminal.
