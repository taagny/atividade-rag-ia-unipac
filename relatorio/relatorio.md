# Relatório — Pipeline RAG

**Aluno:** `[INSIRA SEU NOME AQUI]`  
**Curso:** Inteligência Artificial — UNIPAC Barbacena

## Item 1 — Captura de tela

Insira aqui o print do terminal executando os Desafios 1 e 2, incluindo as perguntas dentro e fora do contexto:

![Print do terminal](../capturas/print_terminal.png)

## Item 2 — Análise do Desafio 1

No modo RAG OFF, o modelo recebe somente a pergunta. Por isso, sua resposta pode ser genérica ou alucinada: ele não tem acesso às políticas privadas da empresa. No modo RAG ON, o contexto recuperado orienta a resposta com os dados da base: a solicitação é feita pelo portal **Serviços-TI**, até o **dia 15 de cada mês**, com **nota fiscal emitida no CPF do colaborador**.

Essa diferença ocorre porque a memória paramétrica do modelo pode falhar em dados corporativos: as informações podem ser privadas, não fazer parte do conjunto de treinamento, estar desatualizadas ou não possuir uma fonte verificável. O RAG reduz esse problema ao buscar o conteúdo relevante em uma fonte externa e fornecê-lo ao modelo no momento da pergunta.
