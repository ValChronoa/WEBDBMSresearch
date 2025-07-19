"""JSON → CSS theme engine."""
from __future__ import annotations
import json, os
from pathlib import Path
from typing import Dict, Any

THEME_CSS_TEMPLATE = """
:root {{
  --color-primary: {primary};
  --color-secondary: {secondary};
  --color-danger: {danger};
  --color-warning: {warning};
}}
"""

def compile_themes(theme_dir: str, static_dir: str) -> None:
    Path(static_dir).mkdir(parents=True, exist_ok=True)
    for path in Path(theme_dir).glob("*.json"):
        with open(path, encoding="utf-8") as fp:
            cfg: Dict[str, Any] = json.load(fp)["palette"]
        css = THEME_CSS_TEMPLATE.format(**cfg)
        (Path(static_dir) / f"{path.stem}.css").write_text(css, encoding="utf-8")