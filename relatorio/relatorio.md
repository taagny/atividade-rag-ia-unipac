# Relatório — Pipeline RAG

**Aluno:** `Taagny Augusto Reis da Silva`  
**Curso:** Ciência da Computação  
**Disciplina:** Inteligência Artificial  
**Instituição:** UNIPAC Barbacena  
**Professor:** Felipe Roncalli de Paula Carneiro  
**Data:** 19/11/2026

## Item 1 — Captura de tela

Insira aqui o print do terminal executando os Desafios 1 e 2, incluindo as perguntas dentro e fora do contexto:

![Print do terminal](../capturas/print_terminal.png)

## Item 2 — Análise do Desafio 1

Na execução real, o RAG OFF respondeu com um procedimento genérico de várias etapas, incluindo “Declaração de Uso”, verificação do uso e documentos não previstos na base. Ele não informou o portal, o prazo do dia 15 nem a exigência do CPF. Já o RAG ON respondeu que a solicitação deve ser enviada até o **dia 15 de cada mês**, com **nota fiscal emitida no CPF do colaborador**, e também informou a análise no ciclo seguinte para pedidos fora do prazo ou sem documentação. Embora o contexto recuperado contenha o portal **“Serviços-TI”**, a resposta final capturada não o repetiu; portanto, não atribuo esse acerto à resposta real do modelo.

Na pergunta fora do contexto, sobre viagens interplanetárias, o RAG OFF produziu uma resposta genérica sobre limitações tecnológicas, riscos, custos e até programas de astronautas. O RAG ON foi mais adequado ao contexto da aplicação: respondeu **“Não encontrou a resposta”**, explicando que a base não contém essa política.

Essa diferença ocorre porque a memória paramétrica do modelo pode falhar em dados corporativos: as informações podem ser privadas, não fazer parte do conjunto de treinamento, estar desatualizadas ou não possuir uma fonte verificável. O RAG reduz esse problema ao buscar o conteúdo relevante em uma fonte externa e fornecê-lo ao modelo no momento da pergunta.

## Item 3 — Análise do Desafio 2

Na execução registrada, a configuração **chunk 40 / overlap 10** causou Retrieval Failure didático: os três resultados tiveram similaridades de **0,547787**, **0,537774** e **0,474530**, mas os trechos recuperados são fragmentos curtos e não concentram, em uma única unidade, a consequência da falta, a necessidade de justificativa em 24 horas e a advertência após reincidência. Assim, a busca encontra palavras relacionadas, mas pode perder o sentido completo da regra.

Com **chunk 500 / overlap 50**, o primeiro resultado teve similaridade **0,662807** e apresentou a regra completa sobre o dia presencial, a justificativa em até 24 horas, o registro e a advertência. Esse resultado foi mais útil para responder à pergunta.

O melhor resultado de **chunk 500 / overlap 50** teve similaridade **0,662807**, acima do melhor resultado do chunk 40, e trouxe junto da regra do dia presencial trechos de férias e vale-refeição. Isso evidencia a diluição: o vetor carrega mais contexto, mas mistura assuntos diferentes na mesma unidade. Chunks pequenos carregam pouco contexto por unidade e podem recuperar fragmentos sem sentido completo; chunks grandes preservam mais contexto, mas podem diluir a similaridade vetorial. Além disso, a divisão por caracteres corta palavras no meio, como em **“corporat”**, o que também prejudica a qualidade dos embeddings.

## Item 4 — Cálculo manual da Similaridade de Cosseno

Para `u = [1, 2]` e `v = [2, 1]`:

1. Produto escalar: `u · v = 1 × 2 + 2 × 1 = 4`.
2. Norma de `u`: `||u|| = √(1² + 2²) = √5`.
3. Norma de `v`: `||v|| = √(2² + 1²) = √5`.
4. Similaridade: `cos(θ) = 4 / (√5 × √5) = 4/5 = 0,8`.

O resultado 0,8 indica uma alta semelhança entre os vetores, embora eles não tenham a mesma direção. Em um sistema RAG, valores maiores representam embeddings mais próximos semanticamente, de acordo com o espaço vetorial aprendido pelo modelo.
