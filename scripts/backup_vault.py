#!/usr/bin/env python3
"""
scripts/backup_vault.py - Sistema di Backup e Snapshot Automatico per Wiki Calcio Catania.

Conforme a:
- DIRETTIVA OPERATIVA GENERALE UNIFICATA: PUNTO 1
- Gestione automatica snapshot timestampati in backups/
- Rotazione programmata (mantiene gli ultimi 5 backup)
- Ripristino d'emergenza: --restore <file_o_ultimo> [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tarfile
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = WORKSPACE_ROOT / "backups"
MAX_BACKUPS = 5

ITEMS_TO_BACKUP = [
    Path("content"),
    Path("data"),
    Path("SCHEMA.md"),
    Path("quartz.config.ts"),
    Path("quartz.layout.ts"),
]


def ensure_backup_dir() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    # Ensure backups/ is in .gitignore
    gitignore = WORKSPACE_ROOT / ".gitignore"
    if gitignore.exists():
        text = gitignore.read_text(encoding="utf-8")
        if "backups/" not in text:
            with open(gitignore, "a", encoding="utf-8") as f:
                f.write("\n# Snapshot di backup automatici\nbackups/\n")
    return BACKUP_DIR


def rotate_backups() -> list[Path]:
    """Mantiene solo i 5 backup più recenti, eliminando i più datati."""
    backups = sorted(BACKUP_DIR.glob("backup_*.tar.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
    removed = []
    if len(backups) > MAX_BACKUPS:
        for old in backups[MAX_BACKUPS:]:
            old.unlink()
            removed.append(old)
            print(f"[ROTATION] Rimosso backup datato: {old.name}")
    return removed


def create_backup(label: str = "") -> Path:
    """Crea un archivio compresso tar.gz timestampato."""
    ensure_backup_dir()
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"_{label}" if label else ""
    backup_filename = f"backup_{now_str}{suffix}.tar.gz"
    backup_path = BACKUP_DIR / backup_filename

    print(f"[BACKUP] Inizio snapshot: {backup_filename}")
    total_files = 0
    with tarfile.open(backup_path, "w:gz") as tar:
        for rel_item in ITEMS_TO_BACKUP:
            abs_item = WORKSPACE_ROOT / rel_item
            if abs_item.exists():
                print(f"  -> Archiviazione {rel_item}...")
                tar.add(abs_item, arcname=str(rel_item))
                if abs_item.is_dir():
                    total_files += sum(1 for _ in abs_item.rglob("*") if _.is_file())
                else:
                    total_files += 1

    size_mb = backup_path.stat().st_size / (1024 * 1024)
    print(f"[BACKUP] Snapshot completato con successo: {backup_path.name}")
    print(f"         File archiviati: {total_files} | Dimensione archivio: {size_mb:.2f} MB")

    rotate_backups()
    return backup_path


def restore_backup(backup_target: str, dry_run: bool = False) -> bool:
    """Ripristina i file da un backup."""
    target_path = Path(backup_target)
    if not target_path.is_absolute():
        if (BACKUP_DIR / backup_target).exists():
            target_path = BACKUP_DIR / backup_target
        elif (WORKSPACE_ROOT / backup_target).exists():
            target_path = WORKSPACE_ROOT / backup_target

    if not target_path.exists():
        if backup_target.lower() == "latest":
            backups = sorted(BACKUP_DIR.glob("backup_*.tar.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
            if not backups:
                print("[ERROR] Nessun backup trovato in backups/")
                return False
            target_path = backups[0]
        else:
            print(f"[ERROR] Archivio di backup non trovato: {target_path}")
            return False

    print(f"[RESTORE] Ripristino da: {target_path.name}")
    if dry_run:
        print("[RESTORE DRY-RUN] Simulazione attiva. I seguenti elementi verrebbero estratti:")
        with tarfile.open(target_path, "r:gz") as tar:
            for member in tar.getmembers()[:25]:
                print(f"  -> {member.name} ({member.size} bytes)")
            total = len(tar.getmembers())
            if total > 25:
                print(f"  ... e altri {total - 25} elementi.")
        return True

    with tarfile.open(target_path, "r:gz") as tar:
        tar.extractall(path=WORKSPACE_ROOT)
    print(f"[RESTORE] Ripristino completato con successo da {target_path.name} in {WORKSPACE_ROOT}")
    return True


def list_backups():
    ensure_backup_dir()
    backups = sorted(BACKUP_DIR.glob("backup_*.tar.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
    print(f"=== BACKUP DISPONIBILI IN {BACKUP_DIR} ({len(backups)}) ===")
    for idx, b in enumerate(backups, 1):
        mtime = datetime.fromtimestamp(b.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        size_mb = b.stat().st_size / (1024 * 1024)
        print(f" {idx}. {b.name} ({size_mb:.2f} MB, creato: {mtime})")


def main():
    parser = argparse.ArgumentParser(description="Gestione backup e snapshot per Wiki Calcio Catania")
    parser.add_argument("--create", "-c", action="store_true", help="Crea un nuovo backup")
    parser.add_argument("--label", type=str, default="", help="Etichetta opzionale per il backup (es. pre-ingestion)")
    parser.add_argument("--restore", "-r", type=str, help="Ripristina da un file di backup (o 'latest')")
    parser.add_argument("--dry-run", action="store_true", help="Simula il ripristino senza scrivere sul disco")
    parser.add_argument("--list", "-l", action="store_true", help="Elenca i backup presenti")

    args = parser.parse_args()

    if args.restore:
        success = restore_backup(args.restore, dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    elif args.list:
        list_backups()
    else:
        # Default action: create backup
        create_backup(label=args.label)


if __name__ == "__main__":
    main()
