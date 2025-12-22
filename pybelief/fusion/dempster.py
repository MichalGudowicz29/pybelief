from collections import defaultdict
from ..core.belief_mass import BeliefMass

def combine(bma1: BeliefMass, bma2: BeliefMass) -> BeliefMass:
    """Reguła Dempstera: przecięcia z normalizacją (1 / 1-K)."""
    result_map = defaultdict(float)
    conflict = 0.0

    for h1, m1 in bma1.items():
        for h2, m2 in bma2.items():
            intersection = h1 & h2
            prod = m1 * m2
            
            if intersection:
                result_map[intersection] += prod
            else:
                conflict += prod

    if conflict >= 1.0 - 1e-10:
        raise ValueError("Całkowity konflikt - fuzja DST niemożliwa.")

    # Normalizacja
    normalization_factor = 1.0 / (1.0 - conflict)
    normalized_map = {k: v * normalization_factor for k, v in result_map.items()}
    
    return BeliefMass(normalized_map)