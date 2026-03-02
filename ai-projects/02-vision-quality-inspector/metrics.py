from dataclasses import dataclass


@dataclass
class ClassificationMetrics:
    precision: float
    recall: float
    f1: float


def compute_f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
