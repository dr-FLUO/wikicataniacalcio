from pathlib import Path

p_ross = Path("content/01-societa/presidenti/ross-pelligra.md")
t_ross = p_ross.read_text(encoding="utf-8")
if "- societa/presidenti/ross-pelligra" not in t_ross:
    t_ross = t_ross.replace("aliases:\n- societa/presidenti/rosario-pelligra", "aliases:\n- societa/presidenti/rosario-pelligra\n- societa/presidenti/ross-pelligra")
    p_ross.write_text(t_ross, encoding="utf-8")
    print("Added alias to ross-pelligra.md")

p_tdg = Path("content/04-strutture/stadio-massimino/torre-del-grifo.md")
t_tdg = p_tdg.read_text(encoding="utf-8")
if "aliases:" not in t_tdg:
    t_tdg = t_tdg.replace("status: verified", "status: verified\naliases:\n- stadio/torre-del-grifo\n- 04-strutture/centri-sportivi/torre-del-grifo")
    p_tdg.write_text(t_tdg, encoding="utf-8")
    print("Added aliases to torre-del-grifo.md")
