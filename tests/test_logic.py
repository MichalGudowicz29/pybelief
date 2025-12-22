import pytest
from dst_dsmt.core.belief_mass import BeliefMass
from dst_dsmt.fusion import dempster, pcr

# --- Testy Podstawowe (Core) ---

def test_belief_mass_creation():
    """Sprawdza tworzenie i normalizację mas."""
    # Masy nie sumują się do 1.0 -> powinna nastąpić normalizacja
    raw_masses = {
        frozenset("A"): 0.4,
        frozenset("B"): 0.1
    }
    bm = BeliefMass(raw_masses).normalize()
    
    # Suma 0.5, więc wagi powinny się podwoić
    assert bm.get_mass("A") == 0.8
    assert bm.get_mass("B") == 0.2
    assert sum(bm.masses.values()) == pytest.approx(1.0)

def test_zero_mass_removal():
    """Sprawdza czy zerowe masy są usuwane."""
    bm = BeliefMass({
        frozenset("A"): 0.5,
        frozenset("B"): 0.0
    })
    assert len(bm.masses) == 1
    assert bm.get_mass("B") == 0.0

# --- Testy Reguły Dempstera (DST) ---

def test_dempster_consensus():
    """Dwa źródła zgodne w 100%."""
    m1 = BeliefMass({frozenset("A"): 1.0})
    m2 = BeliefMass({frozenset("A"): 1.0})
    
    result = dempster.combine(m1, m2)
    assert result.get_mass("A") == 1.0

def test_dempster_paradox_behavior():
    """
    Sprawdza, czy Dempster wpada w 'Paradoks Zadeha'.
    Ekspert 1: 99% A, 1% C
    Ekspert 2: 99% B, 1% C
    Oczekiwany wynik DST: 100% na C (nielogiczne, ale poprawne matematycznie dla tej reguły).
    """
    m1 = BeliefMass({frozenset("A"): 0.99, frozenset("C"): 0.01})
    m2 = BeliefMass({frozenset("B"): 0.99, frozenset("C"): 0.01})
    
    result = dempster.combine(m1, m2)
    
    # Konflikt (A vs B) zjada większość masy, zostaje tylko przecięcie C-C
    assert result.get_mass("C") > 0.99

# --- Testy Reguły PCR5 (DSmT) ---

def test_pcr5_paradox_resolution():
    """
    Sprawdza, czy PCR5 poprawnie rozwiązuje paradoks.
    Konflikt powinien wrócić do źródeł (A i B), a C powinno zostać małe.
    """
    m1 = BeliefMass({frozenset("A"): 0.99, frozenset("C"): 0.01})
    m2 = BeliefMass({frozenset("B"): 0.99, frozenset("C"): 0.01})
    
    result = pcr.combine(m1, m2)
    
    # C powinno być bardzo małe (iloczyn 0.01 * 0.01 + drobna redystrybucja)
    assert result.get_mass("C") < 0.01
    
    # A i B powinny mieć wysokie poparcie (odzyskana masa z konfliktu)
    assert result.get_mass("A") > 0.4
    assert result.get_mass("B") > 0.4