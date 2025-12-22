# DST & DSmT Fusion Library

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-beta-orange)]()

Lekka biblioteka Pythona do fuzji danych (wnioskowania w warunkach niepewności). Implementuje klasyczną **Teorię Dempstera-Shafera (DST)** oraz nowoczesną **Teorię Dezerta-Smarandache'a (DSmT)** przy użyciu reguły PCR5.

Zaprojektowana z myślą o skalowalności, czytelności i łatwej integracji.

---

## Możliwości


* **Architektura:** Oparta na `dataclasses` - łatwa w rozbudowie o nowe metadane bez psucia logiki fuzji.
* **Zaimplementowane algorytmy:**
    * **Reguła Dempstera:** Klasyczna fuzja z normalizacją konfliktu.
    * **PCR5 (Proportional Conflict Redistribution):** Zaawansowana obsługa konfliktów (DSmT), rozwiązująca paradoksy klasycznej teorii.

---

## Instalacja i Uruchomienie

### 1. Pobranie repozytorium
```bash
git clone https://github.com/itaprac/Inzynierski-projekt-zespolowy.git

cd Inzynierski-projekt-zespolowy/src/library

```

### 2. Instalacja pakietu:
Zalecamy instalację w trybie edytowalnym (`-e`), co pozwala na wprowadzanie zmian w kodzie bez konieczności reinstalacji.

```bash
# Utworzenie wirtualnego środowiska (opcjonalnie, ale zalecane)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub: .\venv\Scripts\activate  # Windows

# Instalacja biblioteki
pip install -e .

# Instalacja narzędzi deweloperskich (do testów)
# (Brak zdefiniowanego extras "dev" w pyproject.toml. Zainstaluj narzędzia testowe ręcznie:)
pip install pytest

```

### 3. Uruchomienie testów i przykładu 

```bash 
python example/zadeh_paradox.py

pytest -v
```
---

## Jak używać (Szybki Start)
Biblioteka udostępnia prosty interfejs oparty na klasie `BeliefMass` i funkcjach `combine`.

```python
from dst_dsmt import BeliefMass
from dst_dsmt.fusion import dempster, pcr

# 1. Zdefiniuj hipotezy (używając frozenset dla niemutowalności)
# Sensor A twierdzi na 90%, że to Samolot (S)
m1 = BeliefMass({
    frozenset(['S']): 0.9,
    frozenset(['R']): 0.1  # Rakieta
})

# Sensor B twierdzi na 80%, że to Samolot (S)
m2 = BeliefMass({
    frozenset(['S']): 0.8,
    frozenset(['R']): 0.2
})

# 2. Połącz wiedzę (Fuzja)
wynik = pcr.combine(m1, m2)

print(wynik.get_mass(['S'])) 
# Wynik będzie bliski 0.98 (wzmocniona pewność)

```

---

## Przykłady (Paradoks Zadeha)
W folderze `examples/` znajduje się demonstracja **Paradoksu Zadeha**, który pokazuje, dlaczego klasyczna teoria Dempstera (DST) zawodzi przy wysokim konflikcie i dlaczego warto stosować PCR5 (DSmT).

Aby uruchomić przykład:

```bash
python examples/zadeh_paradox.py

```

**Oczekiwany wynik:**

* **DST:** Pokaże mylący wynik (pewność co do mało prawdopodobnej hipotezy).
* **PCR5:** Pokaże logiczny wynik (konflikt wraca do źródeł).

---

## Uruchamianie Testów
Biblioteka posiada zestaw testów jednostkowych sprawdzających poprawność obliczeń matematycznych.

```bash

# Uruchomienie z dokładnym opisem (verbose)
pytest -v

```

---

## Struktura Projektu

```text
library/
├── pybelief/
│   ├── core/           # Podstawowe struktury danych (BeliefMass)
│   └── fusion/         # Algorytmy (Dempster, PCR5)
├── examples/           # Skrypty demonstracyjne
├── tests/              # Testy jednostkowe
├── pyproject.toml      # Konfiguracja pakietu
└── README.md           # Ten plik

```

## Licencja
Projekt jest objęty licencją MIT. Szczegóły w pliku `LICENSE`.
