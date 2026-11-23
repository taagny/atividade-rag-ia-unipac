# Relatório — Pipeline RAG

**Aluno:** `[INSIRA SEU NOME AQUI]`  
**Curso:** Inteligência Artificial — UNIPAC Barbacena

## Item 1 — Captura de tela

Insira aqui o print do terminal executando os Desafios 1 e 2, incluindo as perguntas dentro e fora do contexto:

![Print do terminal](../capturas/print_terminal.png)

## Item 2 — Análise do Desafio 1

No modo RAG OFF, o modelo recebe somente a pergunta. Por isso, sua resposta pode ser genérica ou alucinada: ele não tem acesso às políticas privadas da empresa. No modo RAG ON, o contexto recuperado orienta a resposta com os dados da base: a solicitação é feita pelo portal **Serviços-TI**, até o **dia 15 de cada mês**, com **nota fiscal emitida no CPF do colaborador**.

Essa diferença ocorre porque a memória paramétrica do modelo pode falhar em dados corporativos: as informações podem ser privadas, não fazer parte do conjunto de treinamento, estar desatualizadas ou não possuir uma fonte verificável. O RAG reduz esse problema ao buscar o conteúdo relevante em uma fonte externa e fornecê-lo ao modelo no momento da pergunta.

## Item 3 — Análise do Desafio 2

Na execução registrada, a configuração **chunk 40 / overlap 10** causou Retrieval Failure didático: embora os três resultados tenham similaridades próximas (0,547787, 0,537774 e 0,474530), os trechos recuperados são fragmentos curtos e não concentram, em uma única unidade, a consequência da falta, a necessidade de justificativa em 24 horas e a advertência após reincidência. Assim, a busca encontra palavras relacionadas, mas perde o sentido completo da regra.

Com **chunk 500 / overlap 50**, o primeiro resultado teve similaridade **0,662807** e apresentou a regra completa sobre o dia presencial, a justificativa em até 24 horas, o registro e a advertência. Esse resultado foi mais útil para responder à pergunta.

O trade-off é que chunks muito pequenos preservam alta precisão local, mas podem perder contexto e sentido. Chunks muito grandes preservam mais contexto, mas podem diluir a similaridade vetorial ao misturar assuntos diferentes. A configuração adequada depende do tamanho e da organização dos documentos.

## Item 4 — Cálculo manual da Similaridade de Cosseno

Para `u = [1, 2]` e `v = [2, 1]`:

1. Produto escalar: `u · v = 1 × 2 + 2 × 1 = 4`.
2. Norma de `u`: `||u|| = √(1² + 2²) = √5`.
3. Norma de `v`: `||v|| = √(2² + 1²) = √5`.
4. Similaridade: `cos(θ) = 4 / (√5 × √5) = 4/5 = 0,8`.

O resultado 0,8 indica uma alta semelhança entre os vetores, embora eles não tenham a mesma direção. Em um sistema RAG, valores maiores representam embeddings mais próximos semanticamente, de acordo com o espaço vetorial aprendido pelo modelo.
