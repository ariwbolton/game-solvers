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

    def __repr__(self) -> str:
        return f"Page(id={self.id}, name={self.name}, links={len(self.links) if self.links else None}, backlinks={len(self.backlinks) if self.backlinks else None})"
