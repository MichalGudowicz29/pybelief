# WAŻNE: Aby to działało, musisz być w katalogu głównym projektu
# i mieć zainstalowany pakiet (pip install -e .)

from pybelief.core.belief_mass import BeliefMass
from pybelief.fusion import dempster, pcr

def run_zadeh_demo():
    print("=== DEMONSTRACJA PARADOKSU ZADEHA ===")
    
    # Scenariusz:
    # Ekspert 1: 99% A (Meningitis), 1% T (Tumor)
    m1 = BeliefMass({
        frozenset(['A']): 0.99, 
        frozenset(['T']): 0.01
    })
    
    # Ekspert 2: 99% B (Concussion), 1% T (Tumor)
    m2 = BeliefMass({
        frozenset(['B']): 0.99, 
        frozenset(['T']): 0.01
    })

    print(f"Ekspert 1: {m1}")
    print(f"Ekspert 2: {m2}")
    print("\n--- WYNIKI FUZJI ---\n")

    # 1. Reguła Dempstera (DST)
    try:
        dst_result = dempster.combine(m1, m2)
        print("DST (Dempster):")
        for h, v in dst_result.items():
            print(f"  {set(h)}: {v:.5f}")
        print("-> WNIOSEK: Paradoks! 100% pewności, że to Guz (T), mimo że oboje w to wątpili.")
    except Exception as e:
        print(f"Błąd DST: {e}")

    print("-" * 30)

    # 2. Reguła PCR5 (DSmT)
    pcr_result = pcr.combine(m1, m2)
    print("DSmT (PCR5):")
    for h, v in sorted(pcr_result.items(), key=lambda x: -x[1]):
        print(f"  {set(h)}: {v:.5f}")
    print("-> WNIOSEK: Konflikt rozdzielony. Nadal nie wiemy czy A czy B, ale T jest małe.")

if __name__ == "__main__":
    run_zadeh_demo()