"""
Modulo di protezione e blindatura file ("Data Sealing").
Controlla il flag frontmatter 'locked: true' e registra/verifica gli hash SHA-256.
"""
import sys, os, hashlib, json
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding='utf-8')

LOCKS_DIR = Path("locks")
LOCKS_FILE = LOCKS_DIR / "locked_entities.json"

def calculate_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def is_locked(path: Path) -> bool:
    try:
        txt = path.read_text(encoding="utf-8")
        if txt.startswith("---"):
            parts = txt.split("---", 2)
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1]) or {}
                return fm.get("locked") is True
    except Exception:
        pass
    return False

def register_lock(path: Path, reason: str = "certificato_transfermarkt_dataset"):
    LOCKS_DIR.mkdir(parents=True, exist_ok=True)
    registry = {}
    if LOCKS_FILE.exists():
        try:
            registry = json.loads(LOCKS_FILE.read_text(encoding="utf-8"))
        except Exception:
            registry = {}
            
    rel = str(path.as_posix())
    registry[rel] = {
        "sha256": calculate_sha256(path),
        "reason": reason
    }
    LOCKS_FILE.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

def verify_locks() -> list:
    if not LOCKS_FILE.exists():
        return []
    registry = json.loads(LOCKS_FILE.read_text(encoding="utf-8"))
    violations = []
    for rel_path, data in registry.items():
        p = Path(rel_path)
        if not p.exists():
            violations.append({"file": rel_path, "error": "FILE_DELETED"})
            continue
        current_hash = calculate_sha256(p)
        if current_hash != data["sha256"]:
            violations.append({"file": rel_path, "error": "UNAUTHORIZED_MODIFICATION"})
    return violations
