"""Migrace MAJOR verzí core (zadání 13 kap. 10.6, 11 kap. 5–6).

Soubor `<verze>.py` (např. `1.0.0.py`) s funkcí `migrate(vault, apply: bool) -> str`: bez `apply` jen vypíše,
co by změnil (dry-run), s `apply` změny provede. `update_core` spustí migrace verzí mezi starou a novou verzí,
když se mění MAJOR. Ve fázi 3 je tu jen kostra, žádná migrace zatím neexistuje.
"""
