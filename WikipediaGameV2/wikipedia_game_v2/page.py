import dataclasses
from dataclasses import dataclass


@dataclass
class Page:
    id: int
    name: str
    links: list[int] | None
    backlinks: list[int] | None

    loaded: bool  # A page node can be created in a "partially complete" state, before it's officially loaded

    @staticmethod
    def from_dict(data: dict) -> "Page":
        return Page(**data)

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)
