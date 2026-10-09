from dataclasses import dataclass


@dataclass(frozen=True)
class StorageConditions:
    temperature: float
    humidity: float
    storage_duration: int
    transportation_type: str