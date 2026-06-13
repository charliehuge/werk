#!/usr/bin/env python3
"""Backfill wiki footers on exercise files + build the exercises index.

Idempotent: footer is delimited by a <!-- wiki-footer --> sentinel; re-running
truncates at the sentinel and regenerates. Frontmatter slugs are the source of
truth; this only renders human-navigable links from them.
"""
import sys, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
EX = ROOT / "exercises"
SENTINEL = "<!-- wiki-footer -->"

VOCAB = "../vocabulary.md"

def parse(path):
    text = path.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"{path.name}: no frontmatter")
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm), body, fm  # parsed, body, raw frontmatter text

def strip_footer(body):
    # drop footer (+ its leading '---' rule) and trim surrounding whitespace
    head = body.split(SENTINEL)[0]
    return head.rstrip().removesuffix("---").strip()

def vocab_link(term, section):
    return f"[{term}]({VOCAB}#{section})"

def main():
    files = sorted(EX.glob("*.md"))
    files = [f for f in files if f.name != "README.md"]
    # slug -> display name
    names = {}
    for f in files:
        fm, _, _ = parse(f)
        names[f.stem] = fm["name"]

    missing = []
    for f in files:
        fm, body, raw_fm = parse(f)
        body = strip_footer(body)

        lines = [SENTINEL, ""]
        # Trains
        focus = fm.get("focus") or []
        if focus:
            lines.append("**Trains:** " + " · ".join(vocab_link(t, "focus") for t in focus) + "  ")
        equip = fm.get("equipment") or []
        if equip:
            lines.append("**Equipment:** " + " · ".join(vocab_link(t, "equipment") for t in equip) + "  ")
        else:
            lines.append("**Equipment:** " + vocab_link("bodyweight", "equipment") + "  ")
        mp = fm.get("movement_pattern")
        lvl = fm.get("level")
        pl = []
        if mp:
            pl.append("**Pattern:** " + vocab_link(mp, "movement_pattern"))
        if lvl:
            pl.append("**Level:** " + vocab_link(lvl, "level"))
        if pl:
            lines.append(" · ".join(pl))

        # Progressions & regressions
        prog = fm.get("progression") or []
        reg = fm.get("regression") or []
        if prog or reg:
            lines += ["", "**Progressions & regressions**"]
            for s in prog:
                disp = names.get(s)
                if not disp:
                    missing.append((f.name, "progression", s)); disp = s
                lines.append(f"- Harder: [{disp}]({s}.md)")
            for s in reg:
                disp = names.get(s)
                if not disp:
                    missing.append((f.name, "regression", s)); disp = s
                lines.append(f"- Easier: [{disp}]({s}.md)")

        # References (sources + videos)
        sources = fm.get("sources") or []
        videos = fm.get("videos") or []
        if sources or videos:
            lines += ["", "**References**"]
            for u in sources:
                lines.append(f"- [{u}]({u})")
            for v in videos:
                if isinstance(v, dict):
                    lines.append(f"- 📹 [{v.get('title', v['url'])}]({v['url']})")
                else:
                    lines.append(f"- 📹 [{v}]({v})")

        footer = "\n".join(lines)
        new = body + "\n\n---\n\n" + footer + "\n"
        # preserve original frontmatter text verbatim
        f.write_text(f"---{raw_fm}---\n\n{new}")

    # Index grouped by focus
    by_focus = {}
    for f in files:
        fm, _, _ = parse(f)
        for foc in (fm.get("focus") or ["(uncategorized)"]):
            by_focus.setdefault(foc, []).append((fm["name"], f.name))
    idx = ["# Exercise Library", "",
           f"{len(files)} exercises. Each appears under every focus it trains. "
           "Tag values: [vocabulary.md](../vocabulary.md).", ""]
    for foc in sorted(by_focus):
        idx.append(f"## {foc}")
        idx.append("")
        for name, fn in sorted(by_focus[foc]):
            idx.append(f"- [{name}]({fn})")
        idx.append("")
    (EX / "README.md").write_text("\n".join(idx).rstrip() + "\n")

    if missing:
        print("UNRESOLVED REFS:")
        for m in missing:
            print(" ", m)
    print(f"Wrote {len(files)} exercises + index.")

if __name__ == "__main__":
    main()
