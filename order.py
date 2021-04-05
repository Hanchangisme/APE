from dataclasses import dataclass


@dataclass
class Order():
    size: int
    price: float
    isopen: bool
    islong: bool
    iscurrent: bool = False
    isrevoke: bool = False