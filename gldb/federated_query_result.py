from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class FederatedQueryResult:
    data: Any
    metadata: Dict
