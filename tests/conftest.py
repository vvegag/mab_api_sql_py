from __future__ import annotations

import os
import tempfile
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Garante que os testes usem SQLite local e não dependam do .env da máquina.
diretorio_teste = Path(tempfile.mkdtemp(prefix="mabandit_teste_"))
database_teste = diretorio_teste / "teste_mabandit.db"
os.environ.setdefault("DATABASE_URL", f"sqlite:///{database_teste.as_posix()}")
