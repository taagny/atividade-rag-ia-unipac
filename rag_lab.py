"""Laboratório didático de RAG para a atividade da UNIPAC."""

from functools import lru_cache

import numpy as np


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
