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
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
python rag_lab.py --desafio 1 2>$null | Out-File -Encoding utf8 capturas/saida_desafio1.txt
```

Desafio 2 — testa chunks pequenos:

```powershell
python rag_lab.py --desafio 2 --chunk 40 --overlap 10 2>$null | Out-File -Encoding utf8 capturas/saida_desafio2_chunk40.txt
```

Desafio 2 — testa chunks grandes:

```powershell
python rag_lab.py --desafio 2 --chunk 500 --overlap 50 2>$null | Out-File -Encoding utf8 capturas/saida_desafio2_chunk500.txt
```

As saídas devem ser salvas em UTF-8 nos arquivos `capturas/saida_desafio1.txt`, `capturas/saida_desafio2_chunk40.txt` e `capturas/saida_desafio2_chunk500.txt`. O `stderr` é descartado nos comandos acima para evitar mensagens do PowerShell misturadas à captura; erros reais continuam visíveis quando o script é executado diretamente.

Para tirar o print do terminal, execute o desafio sem `2>$null`, sem `| Out-File` e sem redirecionamento. Assim, as perguntas, os chunks, as similaridades e as respostas ficam visíveis no console:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
python rag_lab.py --desafio 1
```

Depois, tire o print do terminal executando o script e salve-o em `capturas/print_terminal.png`. Esse arquivo agora pode ser versionado.

## Estrutura de pastas

```text
.
├── dados/
│   └── politicas_empresa.txt
├── capturas/
│   ├── saida_desafio1.txt
│   ├── saida_desafio2_chunk40.txt
│   ├── saida_desafio2_chunk500.txt
│   └── print_terminal.png
├── relatorio/
│   └── relatorio.md
├── .env.example
├── .gitignore
├── rag_lab.py
└── requirements.txt
```
