import os
import sys

# Umożliwia uruchomienie skryptu bez instalacji pakietu (pip install -e .)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pybelief.core.belief_mass import BeliefMass
from pybelief.fusion import dempster, pcr


def main():
    # Trzy źródła zgodne w większości na hipotezę A
    sources = [
        BeliefMass({frozenset("A"): 0.7, frozenset("B"): 0.3}),
        BeliefMass({frozenset("A"): 1.0}),
        BeliefMass({frozenset("A"): 1.0}),
    ]

    dst_result = dempster.combine_multiple(sources)
    pcr_result = pcr.combine_multiple(sources)

    print("=== combine_multiple demo ===")
    print("Źródła:")
    for i, s in enumerate(sources, 1):
        print(f"  {i}: {s}")

    print("\nDempster (DST):")
    for h, v in dst_result.items():
        print(f"  {set(h)} -> {v:.4f}")

    print("\nPCR5 (DSmT):")
    for h, v in pcr_result.items():
        print(f"  {set(h)} -> {v:.4f}")


if __name__ == "__main__":
    main()
