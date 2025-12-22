from collections import defaultdict
from typing import List
from ..core.belief_mass import BeliefMass

def combine(bma1: BeliefMass, bma2: BeliefMass) -> BeliefMass:
    """Reguła PCR5: Proporcjonalna redystrybucja konfliktu."""
    result_map = defaultdict(float)

    for h1, m1 in bma1.items():
        for h2, m2 in bma2.items():
            intersection = h1 & h2
            prod = m1 * m2
            
            if intersection:
                # 1. Klasyczne przecięcie
                result_map[intersection] += prod
            elif prod > 0:
                # 2. Redystrybucja konfliktu (Logic PCR5)
                # Formuła: m1^2 * m2 / (m1 + m2) wraca do h1
                sum_m = m1 + m2
                if sum_m > 0:
                    result_map[h1] += (m1 * prod) / sum_m
                    result_map[h2] += (m2 * prod) / sum_m

    # Wynik PCR5 normalizujemy dla pewności numerycznej
    return BeliefMass(result_map).normalize()

def combine_multiple(sources: List[BeliefMass]) -> BeliefMass:
    """Łączy wiele źródeł (BeliefMass) za pomocą reguły PCR5.
    
    Args:
        sources: Lista źródeł BeliefMass do połączenia (minimum 2).
        
    Returns:
        Połączony BeliefMass ze wszystkich źródeł.
        
    Raises:
        ValueError: Jeśli podano mniej niż 2 źródła.
    """
    if len(sources) < 2:
        raise ValueError("Wymagane są co najmniej 2 źródła do fuzji.")
    
    result = sources[0]
    for source in sources[1:]:
        result = combine(result, source)
    
    return result