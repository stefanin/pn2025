
from pathlib import Path

directory = Path("db")
# Crea la directory solo se non esiste
directory.mkdir(parents=True, exist_ok=True)
directory = Path("log")
# Crea la directory solo se non esiste
directory.mkdir(parents=True, exist_ok=True)
