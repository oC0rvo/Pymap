# Pymap

# 🔍 PyMap - Advanced TCP Port Scanner

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/status-active-brightgreen.svg)


O **PyMap** é uma ferramenta de varredura e reconhecimento de rede desenvolvida em Python. O projeto foi projetado com foco em alta performance, utilizando execução simultânea (*multithreading*) para identificar portas TCP abertas, medir a latência da conexão (RTT) e capturar banners de serviços (*Banner Grabbing*).

Ideal para estudos de cibersegurança, administração de redes e auditorias básicas de infraestrutura.

---

## 🚀 Funcionalidades

- **Escaneamento Multithreaded:** Utiliza `concurrent.futures.ThreadPoolExecutor` para realizar centenas de testes por segundo.
- **Detecção de Serviços (Banner Grabbing):** Interage com a porta aberta para identificar a versão ou software rodando (ex: OpenSSH, Apache, Nginx).
- **Cálculo de Latência (RTT):** Mede o tempo de resposta em milissegundos para cada porta aberta.
- **Mapeamento de Protocolos:** Traduz automaticamente o número da porta para o nome do serviço associado (ex: Porta 80 -> HTTP).
- **Interface via CLI:** Entrada de argumentos dinâmica e amigável usando `argparse`.
- **Relatório Formatado:** Exibe os resultados em uma tabela limpa e ordenada numericamente por porta.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3** (Standard Library)
  - `socket` — Manipulação de conexões de rede em baixo nível.
  - `concurrent.futures` — Gerenciamento de pool de threads para execução concorrente.
  - `argparse` — Construção da interface de linha de comando.
  - `time` — Medição precisa da latência da conexão.

---

## 📥 Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior instalado.
- Git instalado (opcional).

  
Legal Disclaimer / Aviso Legal:Esta ferramenta foi desenvolvida exclusivamente para fins educacionais e auditorias de segurança autorizadas. O uso do PyMap contra alvos sem autorização prévia e expressa do proprietário do sistema é estritamente proibido e pode violar leis locais e internacionais de cibersegurança. O autor não se responsabiliza pelo uso indevido desta ferramenta.
---
