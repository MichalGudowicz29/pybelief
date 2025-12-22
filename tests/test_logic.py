import os
import sys

import pytest

# Upewniamy się, że katalog projektu jest na sys.path przy uruchamianiu bez instalacji editable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pybelief.core.belief_mass import BeliefMass
from pybelief.fusion import dempster, pcr

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


def test_dempster_combine_multiple_three_sources():
    """Łączenie więcej niż dwóch źródeł przy użyciu combine_multiple."""
    m1 = BeliefMass({frozenset("A"): 0.8, frozenset("B"): 0.2})
    m2 = BeliefMass({frozenset("A"): 1.0})
    m3 = BeliefMass({frozenset("A"): 1.0})

    chained = dempster.combine_multiple([m1, m2, m3])

    # Cała masa powinna skończyć na A po kolejnych normalizacjach
    assert chained.get_mass("A") == pytest.approx(1.0)
    assert chained.get_mass("B") == pytest.approx(0.0)

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


def test_pcr5_combine_multiple_three_sources():
    """PCR5 również powinien poprawnie łączyć więcej niż dwa źródła."""
    m1 = BeliefMass({frozenset("A"): 0.6, frozenset("B"): 0.4})
    m2 = BeliefMass({frozenset("A"): 1.0})
    m3 = BeliefMass({frozenset("A"): 1.0})

    chained = pcr.combine_multiple([m1, m2, m3])

    # Po redystrybucji konfliktu masa A powinna dominować, B minimalne
    assert chained.get_mass("A") > 0.98
    assert chained.get_mass("B") < 0.02