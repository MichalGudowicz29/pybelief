from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Union, List

# Alias typu
Hypothesis = FrozenSet[str]

@dataclass
class BeliefMass:
    """
    Lekki kontener na masy przekonań.
    """
    masses: Dict[Hypothesis, float] = field(default_factory=dict)
    
    def __post_init__(self):
        """Automatyczne czyszczenie zerowych mas przy tworzeniu."""
        # Filtrujemy bardzo małe wartości (błędy numeryczne)
        self.masses = {k: v for k, v in self.masses.items() if v > 1e-10}

    def normalize(self) -> 'BeliefMass':
        """Zwraca nową, znormalizowaną instancję."""
        total = sum(self.masses.values())
        if total == 0: return BeliefMass()
        return BeliefMass({k: v / total for k, v in self.masses.items()})

    def get_mass(self, hypothesis: Union[Hypothesis, list, set, str]) -> float:
        """Bezpieczny dostęp do masy."""
        if isinstance(hypothesis, str):
            hypothesis = frozenset([hypothesis])
        elif not isinstance(hypothesis, frozenset):
            hypothesis = frozenset(hypothesis)
        return self.masses.get(hypothesis, 0.0)

    def items(self):
        return self.masses.items()

    def __repr__(self):
        return f"BeliefMass({dict(self.masses)})"