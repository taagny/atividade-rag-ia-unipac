"""Laboratório didático de RAG para a atividade da UNIPAC."""

import argparse
from functools import lru_cache
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv


def criar_chunks(texto: str, tamanho_chunk: int, sobreposicao: int) -> list[str]:
    """Divide um texto em janelas de caracteres com sobreposição configurável."""
    if tamanho_chunk <= 0:
        raise ValueError("tamanho_chunk deve ser maior que zero")
    if sobreposicao < 0 or sobreposicao >= tamanho_chunk:
        raise ValueError("sobreposicao deve estar entre zero e tamanho_chunk - 1")

    passo = tamanho_chunk - sobreposicao
    return [
        texto[inicio : inicio + tamanho_chunk]
        for inicio in range(0, len(texto), passo)
        if texto[inicio : inicio + tamanho_chunk]
    ]


@lru_cache(maxsize=1)
def carregar_modelo_embeddings():
    """Carrega sob demanda um modelo leve e multilíngue."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def gerar_embeddings(textos: list[str] | str) -> np.ndarray:
    """Gera vetores de embeddings para um texto ou lista de textos."""
    lista = [textos] if isinstance(textos, str) else textos
    if not lista:
        return np.empty((0, 0), dtype=float)
    return np.asarray(carregar_modelo_embeddings().encode(lista), dtype=float)


def similaridade_coseno(vetor_a: np.ndarray, vetor_b: np.ndarray) -> float:
    """Calcula manualmente o cosseno entre dois vetores."""
    norma_a = np.linalg.norm(vetor_a)
    norma_b = np.linalg.norm(vetor_b)
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return float(np.dot(vetor_a, vetor_b) / (norma_a * norma_b))


def recuperar_top_k(
    pergunta: str, chunks: list[str], k: int = 3
) -> list[tuple[str, float]]:
    """Retorna até k chunks mais similares à pergunta."""
    if k <= 0:
        raise ValueError("k deve ser maior que zero")
    if not chunks:
        return []

    embedding_pergunta = gerar_embeddings(pergunta)[0]
    embeddings_chunks = gerar_embeddings(chunks)
    resultados = [
        (chunk, similaridade_coseno(embedding_pergunta, embedding_chunk))
        for chunk, embedding_chunk in zip(chunks, embeddings_chunks)
    ]
    return sorted(resultados, key=lambda item: item[1], reverse=True)[:k]


def chamar_llm(prompt: str) -> str:
    """Chama o provedor configurado ou retorna o prompt para inspeção local."""
    load_dotenv()
    provedor = os.getenv("LLM_PROVIDER", "").strip().lower()
    modelo = os.getenv("LLM_MODEL", "llama3.2:3b")

    if provedor == "ollama":
        import requests

        resposta = requests.post(
            os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/api/generate",
            json={"model": modelo, "prompt": prompt, "stream": False},
            timeout=120,
        )
        resposta.raise_for_status()
        return resposta.json()["response"]

    if provedor == "openai":
        from openai import OpenAI

        cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resposta = cliente.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
        )
        return resposta.choices[0].message.content or "(LLM não retornou conteúdo.)"

    return "LLM não configurado. Prompt que seria enviado:\n\n" + prompt


def responder_rag_off(pergunta: str) -> str:
    """Responde diretamente à pergunta, sem contexto recuperado."""
    return chamar_llm(pergunta)


def montar_prompt(pergunta: str, resultados: list[tuple[str, float]]) -> str:
    """Monta o prompt do RAG ON com o contexto recuperado."""
    contexto = "\n\n".join(
        f"[Chunk {indice}]\n{chunk}"
        for indice, (chunk, _similaridade) in enumerate(resultados, start=1)
    )
    return (
        "Responda à pergunta usando somente o contexto abaixo. "
        "Se a informação não estiver no contexto, diga que não encontrou a resposta.\n\n"
        f"Contexto:\n{contexto}\n\nPergunta: {pergunta}"
    )


def responder_rag_on(pergunta: str, resultados: list[tuple[str, float]]) -> str:
    """Responde usando os chunks recuperados como contexto."""
    return chamar_llm(montar_prompt(pergunta, resultados))


def carregar_base(caminho: str = "dados/politicas_empresa.txt") -> str:
    """Lê a base de conhecimento a partir da raiz do projeto."""
    return Path(caminho).read_text(encoding="utf-8")


def imprimir_comparacao(pergunta: str, chunks: list[str]) -> None:
    """Exibe lado a lado as respostas sem e com contexto."""
    resultados = recuperar_top_k(pergunta, chunks)
    resposta_off = responder_rag_off(pergunta)
    resposta_on = responder_rag_on(pergunta, resultados)
    print(f"\nPERGUNTA: {pergunta}")
    print("\n--- RAG OFF (sem contexto) ---")
    print(resposta_off)
    print("\n--- RAG ON (com contexto) ---")
    print(resposta_on)


def executar_desafio1(chunks: list[str]) -> None:
    """Executa as perguntas dentro e fora do contexto da base."""
    imprimir_comparacao(
        "Como funciona a solicitação de reembolso de equipamentos de TI na empresa?",
        chunks,
    )
    imprimir_comparacao(
        "Qual é a política da empresa para viagens interplanetárias?",
        chunks,
    )


def main() -> None:
    """Ponto de entrada do laboratório."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--desafio", choices=["1"], default="1")
    args = parser.parse_args()
    chunks = criar_chunks(carregar_base(), tamanho_chunk=500, sobreposicao=50)
    if args.desafio == "1":
        executar_desafio1(chunks)


if __name__ == "__main__":
    main()
