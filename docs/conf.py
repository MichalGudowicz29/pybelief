import os
import sys
from importlib.metadata import PackageNotFoundError, version

# Dodaj katalog główny projektu, aby importy pybelief działały przy budowie dokumentacji
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)


# -- Informacje o projekcie -------------------------------------------------

project = "pybelief"
author = "Grupa Dezert"

try:
	release = version("pybelief")
except PackageNotFoundError:
	release = "0.0.0"


# -- Konfiguracja ogólna ----------------------------------------------------

extensions = [
	"sphinx.ext.autodoc",
	"sphinx.ext.autosummary",
	"sphinx.ext.napoleon",
	"sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autosummary_generate = True
autodoc_default_options = {
	"members": True,
	"undoc-members": False,
	"show-inheritance": True,
}


# -- Wygląd HTML ------------------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]
