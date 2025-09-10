from __future__ import annotations
import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys

ROOT = Path(__file__).parent
DB_PATH = ROOT / "ideas.json"

@dataclass
class Idea:
    id: int
    text: str
    tags: List[str]
    created_at: str  # ISO timestamp

def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_db() -> Dict[str, Any]:
    if not DB_PATH.exists():
        return {"last_id": 0, "items": []}
    try:
        return json.loads(DB_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"last_id": 0, "items": []}

def save_db(db: Dict[str, Any]) -> None:
    DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding="utf-8")

def normalize_tags(tag_list: List[str]) -> List[str]:
    # split by comma or spaces, strip, lowercase, dedupe
    raw = " ".join(tag_list)
    parts = []
    for piece in raw.replace(",", " ").split():
        p = piece.strip().lower()
        if p:
            parts.append(p)
    return sorted(list(dict.fromkeys(parts)))  # dedupe while preserving order-ish

def cmd_add(args) -> int:
    db = load_db()
   tags = normalize_tags([args.tags]) if isinstance(args.tags, str) else normalize_tags(args.tags)
    text = " ".join(args.text).strip()
    if not text:
        print('Nothing to add. Usage: add "your idea" --tags ai,tools')
        return 1
    idea_id = db["last_id"] + 1
    db["last_id"] = idea_id
    idea = Idea(id=idea_id, text=text, tags=tags, created_at=now_iso())
    db["items"].append(asdict(idea))
    save_db(db)
    print(f"✅ Saved idea #{idea_id} with tags: {', '.join(tags) if tags else '(none)'}")
    return 0

def cmd_list(_args) -> int:
    db = load_db()
    items = db["items"]
    if not items:
        print("No ideas yet. Add one with: add \"idea\" --tags tag1,tag2")
        return 0
    for it in items:
        tags = ", ".join(it.get("tags", [])) or "(none)"
        print(f"{it['id']:>3}. [{it['created_at']}] {it['text']}  ::  tags: {tags}")
    return 0

def cmd_search(args) -> int:
    q = " ".join(args.query).strip().lower()
    if not q:
        print("Provide a search term. Example: search prototype")
        return 1
    db = load_db()
    matches = []
    for it in db["items"]:
        hay = (it["text"] + " " + " ".join(it.get("tags", []))).lower()
        if q in hay:
            matches.append(it)
    if not matches:
        print("No matches.")
        return 0
    for it in matches:
        tags = ", ".join(it.get("tags", [])) or "(none)"
        print(f"{it['id']:>3}. [{it['created_at']}] {it['text']}  ::  tags: {tags}")
    return 0

def cmd_tag(args) -> int:
    db = load_db()
    tag = args.tag.strip().lower()
    if not tag:
        print("Provide a tag. Example: tag ai")
        return 1
    items = [it for it in db["items"] if tag in [t.lower() for t in it.get("tags", [])]]
    if not items:
        print(f"No ideas with tag: {tag}")
        return 0
    for it in items:
        tags = ", ".join(it.get("tags", [])) or "(none)"
        print(f"{it['id']:>3}. [{it['created_at']}] {it['text']}  ::  tags: {tags}")
    return 0

def cmd_addtag(args) -> int:
    db = load_db()
    try:
        idea_id = int(args.id)
    except Exception:
        print("Provide a valid numeric id. Example: addtag 3 --tags marketing,landing")
        return 1
    extra = normalize_tags([",".join(args.tags)]) if isinstance(args.tags, list) else normalize_tags([args.tags])

    modified = False
    for it in db["items"]:
        if it["id"] == idea_id:
            existing = [t.lower() for t in it.get("tags", [])]
            for t in extra:
                if t not in existing:
                    existing.append(t)
            it["tags"] = existing
            modified = True
            break
    if not modified:
        print(f"No idea with id: {idea_id}")
        return 1
    save_db(db)
    print(f"✅ Updated tags for idea #{idea_id}")
    return 0

def cmd_remove(args) -> int:
    db = load_db()
    try:
        idea_id = int(args.id)
    except Exception:
        print("Provide a valid numeric id. Example: remove 2")
        return 1
    before = len(db["items"])
    db["items"] = [it for it in db["items"] if it["id"] != idea_id]
    after = len(db["items"])
    if before == after:
        print(f"No idea with id: {idea_id}")
        return 1
    save_db(db)
    print(f"🗑️ Removed idea #{idea_id}")
    return 0

def cmd_export(args) -> int:
    out = Path(args.path or "ideas_export.json")
    db = load_db()
    out.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"📦 Exported to {out.resolve()}")
    return 0

def cmd_stats(_args) -> int:
    db = load_db()
    items = db["items"]
    print(f"Total ideas: {len(items)}")
    by_tag: Dict[str, int] = {}
    for it in items:
        for t in it.get("tags", []):
            k = t.lower()
            by_tag[k] = by_tag.get(k, 0) + 1
    if by_tag:
        print("By tag:")
        for t in sorted(by_tag.keys()):
            print(f"  {t}: {by_tag[t]}")
    return 0

def build_parser():
    p = argparse.ArgumentParser(
        prog="idea-box",
        description="Capture ideas with tags. List, search, tag filter, export JSON."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help='Add an idea. Example: add "Ship MVP" --tags ai,tools')
    add.add_argument("text", nargs=argparse.REMAINDER)
    add.add_argument("--tags", "-t", type=str, default="")
    add.set_defaults(func=cmd_add)

    ls = sub.add_parser("list", help="List all ideas")
    ls.set_defaults(func=cmd_list)

    sr = sub.add_parser("search", help="Search in text and tags")
    sr.add_argument("query", nargs=argparse.REMAINDER)
    sr.set_defaults(func=cmd_search)

    tg = sub.add_parser("tag", help="List ideas by tag")
    tg.add_argument("tag")
    tg.set_defaults(func=cmd_tag)

    at = sub.add_parser("addtag", help="Add tags to an idea by id")
    at.add_argument("id")
    at.add_argument("--tags", "-t", nargs=argparse.REMAINDER, default=[])
    at.set_defaults(func=cmd_addtag)

    rm = sub.add_parser("remove", help="Remove idea by id")
    rm.add_argument("id")
    rm.set_defaults(func=cmd_remove)

    ex = sub.add_parser("export", help="Export full DB to JSON")
    ex.add_argument("--path", "-o", default="ideas_export.json")
    ex.set_defaults(func=cmd_export)

    st = sub.add_parser("stats", help="Count totals and per-tag")
    st.set_defaults(func=cmd_stats)

    return p

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
