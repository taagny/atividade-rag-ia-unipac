"""Laboratório didático de RAG para a atividade da UNIPAC."""


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
