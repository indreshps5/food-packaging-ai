from dataclasses import dataclass


@dataclass(frozen=True)
class PackagingProperties:
    oxygen_barrier: float
    moisture_barrier: float
    light_barrier: float
    flexibility: float
    sustainability_score: float
    cost_score: float