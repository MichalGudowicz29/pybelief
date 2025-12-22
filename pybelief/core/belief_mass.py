from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Union, List

# Alias typu
Hypothesis = FrozenSet[str]

@dataclass
class BeliefMass:
    """
    Lekki kontener na masy przekonań.
    
    Przechowuje podstawowy przekonanie (basic belief assignment) w postaci
    słownika: hipoteza -> masa. Automatycznie czyści bardzo małe wartości
    (< 1e-10) z błędów numerycznych.
    
    Attributes:
        masses: Słownik mapujący frozenset hipotez na masy [0, 1].
    
    Examples:
        >>> m = BeliefMass({frozenset("A"): 0.6, frozenset("B"): 0.4})
        >>> m.get_mass("A")
        0.6
        >>> normalized = m.normalize()
    """
    masses: Dict[Hypothesis, float] = field(default_factory=dict)
    
    def __post_init__(self):
        """Automatyczne czyszczenie zerowych mas przy tworzeniu."""
        # Filtrujemy bardzo małe wartości (błędy numeryczne)
        self.masses = {k: v for k, v in self.masses.items() if v > 1e-10}

    def normalize(self) -> 'BeliefMass':
        """Zwraca nową, znormalizowaną instancję.
        
        Normalizuje masy tak, aby sumowały się do 1.0. Jeśli suma mas wynosi 0,
        zwraca pustą instancję.
        
        Returns:
            Nowa instancja BeliefMass ze znormalizowanymi masami.
        
        Examples:
            >>> m = BeliefMass({frozenset("A"): 0.4, frozenset("B"): 0.1})
            >>> normalized = m.normalize()
            >>> sum(normalized.masses.values())
            1.0
        """
        total = sum(self.masses.values())
        if total == 0: return BeliefMass()
        return BeliefMass({k: v / total for k, v in self.masses.items()})

    def get_mass(self, hypothesis: Union[Hypothesis, list, set, str]) -> float:
        """Bezpieczny dostęp do masy dla hipotezy.
        
        Automatycznie konwertuje różne formaty hipotez (str, list, set, frozenset)
        na frozenset i zwraca masę. Jeśli hipoteza nie istnieje, zwraca 0.0.
        
        Args:
            hypothesis: Hipoteza jako string ("A"), lista ["A", "B"], 
                set, frozenset lub Hypothesis.
        
        Returns:
            Masa dla hipotezy w przedziale [0, 1]. 0.0 jeśli hipoteza nie istnieje.
        
        Examples:
            >>> m = BeliefMass({frozenset("A"): 0.8})
            >>> m.get_mass("A")
            0.8
            >>> m.get_mass(["A"])
            0.8
            >>> m.get_mass("C")
            0.0
        """
        if isinstance(hypothesis, str):
            hypothesis = frozenset([hypothesis])
        elif not isinstance(hypothesis, frozenset):
            hypothesis = frozenset(hypothesis)
        return self.masses.get(hypothesis, 0.0)

    def items(self):
        """Zwraca widok par (hipoteza, masa) z wewnętrznego słownika.
        
        Returns:
            dict_items z mapą mas (Hypothesis -> float).
        """
        return self.masses.items()

    def __repr__(self):
        return f"BeliefMass({dict(self.masses)})"