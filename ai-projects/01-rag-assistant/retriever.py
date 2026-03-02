from dataclasses import dataclass
from typing import List


@dataclass
class Chunk:
    text: str
    score: float


def retrieve_top_k(query: str, k: int = 3) -> List[Chunk]:
    # Placeholder retrieval function
    dummy = [
        Chunk(text="Gold is traded globally.", score=0.91),
        Chunk(text="XAUUSD pairs gold vs USD.", score=0.88),
        Chunk(text="Risk management is critical in trading systems.", score=0.84),
    ]
    return dummy[:k]
