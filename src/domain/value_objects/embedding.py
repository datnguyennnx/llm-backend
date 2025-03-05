from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Embedding:
    vector: np.ndarray
    model: str
    
    def __post_init__(self):
        if not isinstance(self.vector, np.ndarray):
            object.__setattr__(self, 'vector', np.array(self.vector))
            
    def to_list(self) -> list:
        return self.vector.tolist()