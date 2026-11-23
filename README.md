# Atividade RAG — Inteligência Artificial

Projeto acadêmico da UNIPAC Barbacena que demonstra, de forma didática, um pipeline de Retrieval-Augmented Generation (RAG). O script divide uma base de políticas em chunks, gera embeddings multilíngues, recupera os trechos mais similares por cosseno e compara respostas com RAG OFF e RAG ON.

## Instalação

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuração do LLM

Copie `.env.example` para `.env` e escolha um provedor:

```powershell
Copy-Item .env.example .env
```

Para usar Ollama localmente, instale e inicie o Ollama, baixe um modelo (por exemplo, `ollama pull llama3.2:3b`) e mantenha `LLM_PROVIDER=ollama`. Para usar a API da OpenAI, configure `LLM_PROVIDER=openai`, o nome do modelo em `LLM_MODEL` e `OPENAI_API_KEY`.

Se `LLM_PROVIDER` não estiver configurado, o script não quebra: ele exibe a mensagem de ausência do LLM e o prompt que seria enviado. A chave de API deve ficar somente no `.env`, que não é versionado.

## Execução dos desafios

Desafio 1 — compara RAG OFF e RAG ON para a pergunta de reembolso e para uma pergunta fora do contexto:

```powershell
python rag_lab.py --desafio 1
```

Desafio 2 — testa chunks pequenos:

```powershell
python rag_lab.py --desafio 2 --chunk 40 --overlap 10
```

Desafio 2 — testa chunks grandes:

```powershell
python rag_lab.py --desafio 2 --chunk 500 --overlap 50
```

As saídas reais usadas no relatório estão em `capturas/saida_desafio1.txt`, `capturas/saida_desafio2_chunk40.txt` e `capturas/saida_desafio2_chunk500.txt`.

## Estrutura de pastas

```text
.
├── dados/
│   └── politicas_empresa.txt
├── capturas/
│   ├── saida_desafio1.txt
│   ├── saida_desafio2_chunk40.txt
│   └── saida_desafio2_chunk500.txt
├── relatorio/
│   └── relatorio.md
├── .env.example
├── .gitignore
├── rag_lab.py
└── requirements.txt
```
