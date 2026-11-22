"""Převod Notion-flavored Markdownu (`content_format: notion-md`) na Markdown pro Obsidian (13 kap. 10.12, zadání 0.17.2).

Cíl je co nejvěrnější podoba: struktura (pořadí bloků, vnoření, číslování, prázdné položky a odstavce) i text se přenesou
beze změny. Co Markdown neumí, zůstane v podobě, kterou Obsidian vykreslí, nebo jde položka do ruční kontroly; nic se
tiše nezjednodušuje.

- Markdownové řádky (CommonMark, GFM) zůstanou, jak jsou; převedou se v nich jen inline značky (`<b>`, `<span color>`,
  zmínky, data, citace `[^URL]`). Obsah bloků kódu a inline kódu se nepřevádí nikdy; `\\<tag>` je text.
- Bloková značka (i odsazená pod markdownovou odrážkou) se převede na svém odsazení. **Kontejner** (`<li>`, `<todo>`,
  `<quote>`, `<callout>`, `<toggle>`, `<column>`, `<p>`, `<h1>`–`<h4>`): titulek je text hned za otevírací značkou,
  potomci po prázdném řádku (nebo po blokové značce či markdownové odrážce) se převedou rekurzivně o úroveň hlouběji.
- Druhy ruční kontroly: `attachment`, `page`, `columns`, `ol_type`, `unsupported:<značka>`, `struktura`.
- Kontrola věrnosti: text bez značek (po sjednocení bílých znaků) a strom seznamů a kontejnerů (počet položek na každé
  úrovni) zdroje a výstupu se musí shodovat; jinak druh `struktura` (soubor se zapíše).

Upřesnění zadání 0.19.1: druh calloutu podle rodiny barvy (přípona `_bg` se odřízne): red → danger, orange a yellow
→ warning, green → success, blue → info, purple → example, pink → tip, ostatní a bez barvy → note. Potomci odrážky `- `
o dvě mezery, číslované položky o šířku značky včetně mezery (`1. ` → 3). Tabulka bez `header-row="true"` má prázdný
řádek záhlaví a všechny řádky v těle. Prázdný odstavec = prázdný řádek.
"""
from __future__ import annotations

import re
import textwrap
from collections import Counter

FENCE = "notion-md"

_TAG = re.compile(r"<(/?)([A-Za-z][\w-]*)((?:\s+[^<>\n]*?)?)\s*(/?)>")
_ATTR = re.compile(r"""([\w:-]+)(?:\s*=\s*("[^"]*"|'[^']*'|[^\s"'>/]+))?""")
_BULLET = re.compile(r"([-*+]|\d+[.)])(?=\s|$)")
_FENCE_OPEN = re.compile(r"(`{3,}|~{3,})")
_CITATION = re.compile(r"\[\^([A-Za-z][\w+.-]*://[^\]\s]+)\]")
_MD_IMAGE = re.compile(r"!\[[^\]\n]*\]\(")

_INLINE = {"b", "strong", "i", "em", "s", "del", "strike", "u", "span", "a", "br", "code", "date", "sub", "sup"}
_MARKS = {"b": "**", "strong": "**", "i": "*", "em": "*", "s": "~~", "del": "~~", "strike": "~~"}
_KEEP_INLINE = {"u", "br", "code", "sub", "sup"}
_VOID = {"empty-block", "hr", "col", "br"}
_CONTAINERS = {"quote", "callout", "toggle"}           # kontejnery počítané v kontrole věrnosti (vedle seznamů)
_ITEMS = {"li", "todo"}
_HEADINGS = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}
_MEDIA = {"image", "file", "pdf", "audio", "video"}
_CALLOUT_KIND = {"red": "danger", "orange": "warning", "yellow": "warning", "green": "success", "blue": "info",
                 "purple": "example", "pink": "tip"}
_SUPPORTED_BLOCKS = ({"ul", "ol", "p", "table", "columns", "column", "page", "database", "empty-block"}
                     | _ITEMS | _CONTAINERS | set(_HEADINGS) | _MEDIA)


def _is_inline(name: str) -> bool:
    return name in _INLINE or name.startswith("mention")


def _attrs(s: str) -> dict[str, str]:
    out = {}
    for m in _ATTR.finditer(s or ""):
        v = m.group(2) or ""
        if v[:1] in "\"'":
            v = v[1:-1]
        out[m.group(1).lower()] = v
    return out


def _mask(text: str) -> str:
    """Kopie textu stejné délky, v níž jsou bloky kódu, inline kód a escapované `\\<` nahrazeny znakem \\x00.
    Hledání značek a odrážek běží nad maskou, výřezy se berou z originálu."""
    chars = list(text)
    pos = 0
    fence = ""
    for line in text.split("\n"):
        s = line.lstrip(" \t")
        if fence:
            if s.startswith(fence[0] * len(fence)) and not s.strip().strip(fence[0]):
                fence = ""
            chars[pos:pos + len(line)] = "\x00" * len(line)
        else:
            m = _FENCE_OPEN.match(s)
            if m:
                fence = m.group(1)
                chars[pos:pos + len(line)] = "\x00" * len(line)
        pos += len(line) + 1
    masked = "".join(chars)
    runs = list(re.finditer(r"`+", masked))
    i = 0
    while i < len(runs):
        n = len(runs[i].group())
        j = next((k for k in range(i + 1, len(runs)) if len(runs[k].group()) == n), None)
        if j is None:
            i += 1
            continue
        for k in range(runs[i].start(), runs[j].end()):
            if chars[k] != "\n":
                chars[k] = "\x00"
        i = j + 1
    masked = "".join(chars)
    for m in re.finditer(r"\\<", masked):
        chars[m.start() + 1] = "\x00"
    return "".join(chars)


def _is_list_line(line: str) -> bool:
    return bool(_BULLET.match(line.lstrip(" \t")))


def _is_quote_line(line: str) -> bool:
    return line.lstrip(" \t").startswith(">")


def _join(blocks: list[list[str]]) -> list[str]:
    """Spojí bloky; mezi dva neprázdné vloží prázdný řádek, aby Markdown bloky neslil (odstavec, citace). Bez něj jen
    tehdy, když další blok začíná odrážkou a předchozí nekončí citací."""
    out: list[str] = []
    for b in blocks:
        if not b:
            continue
        if out and out[-1].strip() and b[0].strip():
            if not _is_list_line(b[0]) or _is_quote_line(out[-1]):
                out.append("")
        out.extend(b)
    return out


def _trim(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


def _color_style(color: str) -> str:
    color = (color or "").strip()
    if color.endswith("_bg"):
        return f"background-color: {color[:-3]}"
    return f"color: {color}"


def _wrap_color(text: str, attrs: dict) -> str:
    color = attrs.get("color")
    if not color or color == "default" or not text:
        return text
    return f'<span style="{_color_style(color)}">{text}</span>'


def date_text(attrs: dict) -> str | None:
    """Datum zmínky textem `RRRR-MM-DD[ HH:mm][ – …]`."""
    start = attrs.get("start") or attrs.get("date")
    if not start:
        return None
    text = start + (f" {t}" if (t := attrs.get("starttime") or attrs.get("start-time") or attrs.get("time")) else "")
    end, end_time = attrs.get("end"), attrs.get("endtime") or attrs.get("end-time")
    if end or end_time:
        text += " – " + " ".join(x for x in (end, end_time) if x)
    return text


def callout_icon(attrs: dict) -> str:
    icon = (attrs.get("icon") or "").strip()
    return "" if "://" in icon or icon.startswith("/") else icon


class _Converter:
    def __init__(self) -> None:
        self.kinds: list[str] = []

    def flag(self, kind: str) -> None:
        if kind not in self.kinds:
            self.kinds.append(kind)

    # ------------------------------------------------------------ inline
    def inline(self, text: str) -> str:
        masked = _mask(text)
        if _MD_IMAGE.search(masked):
            self.flag("attachment")
        parts: list = []
        pos = 0
        stack: list[tuple] = []
        for m in _TAG.finditer(masked):
            parts.append(text[pos:m.start()])
            pos = m.end()
            closing, name, attr_s, selfclose = m.groups()
            name = name.lower()
            raw = text[m.start():m.end()]
            a = _attrs(attr_s)
            if name in _MARKS:
                parts.append(("close" if closing else "open", _MARKS[name]))
            elif name in _KEEP_INLINE:
                parts.append(raw)
            elif name == "span":
                if closing:
                    parts.append(stack.pop()[1] if stack and stack[-1][0] == "span" else raw)
                    continue
                opening, close = "", ""
                if a.get("color"):
                    opening, close = f'<span style="{_color_style(a["color"])}">', "</span>"
                if a.get("underline") == "true":
                    opening, close = opening + "<u>", "</u>" + close
                if not a.get("color") and a.get("underline") != "true":
                    opening, close = raw, "</span>"
                parts.append(opening)
                stack.append(("span", close))
            elif name == "a":
                if closing:
                    if stack and stack[-1][0] == "a":
                        parts.append(f"]({stack.pop()[1]})")
                    else:
                        parts.append(raw)
                elif a.get("href"):
                    parts.append("[")
                    stack.append(("a", a["href"]))
                else:
                    parts.append(raw)
                    stack.append(("a-raw", ""))
            elif name in ("date", "mention-date"):
                if closing:
                    if stack and stack[-1][0] == "date":
                        _, dtext, at = stack.pop()
                        if not "".join(p for p in parts[at:] if isinstance(p, str)).strip():
                            parts.append(dtext)
                    continue
                dtext = date_text(a)
                if dtext is None:
                    parts.append(raw)
                    self.flag(f"unsupported:{name}")
                elif selfclose:
                    parts.append(dtext)
                else:
                    stack.append(("date", dtext, len(parts)))
            elif name.startswith("mention"):
                url = a.get("url") or a.get("href") or ""
                if closing:
                    if stack and stack[-1][0] == "mention":
                        _, url, at = stack.pop()
                        label = "".join(p if isinstance(p, str) else p[1] for p in parts[at:])
                        if not url:
                            continue
                        del parts[at:]
                        parts.append(f"[{label.strip()}]({url})" if label.strip() else f"<{url}>")
                    continue
                if selfclose:
                    if url:
                        parts.append(f"<{url}>")
                    continue
                stack.append(("mention", url, len(parts)))
            else:                                   # bloková značka uprostřed textu (titulek): beze změny
                parts.append(raw)
                if not closing:
                    self.flag(f"unsupported:{name}")
        parts.append(text[pos:])
        out = self._marks(parts)
        cm = _mask(out)
        return "".join(self._citations(out, cm))

    @staticmethod
    def _citations(text: str, masked: str) -> list[str]:
        res, pos = [], 0
        for m in _CITATION.finditer(masked):
            res += [text[pos:m.start()], f"[{text[m.start(1):m.end(1)]}]({text[m.start(1):m.end(1)]})"]
            pos = m.end()
        res.append(text[pos:])
        return res

    @staticmethod
    def _marks(parts: list) -> str:
        """Značky `**`, `*`, `~~` s mezerami vně (`<b>x </b>y` → `**x** y`); prázdný úsek beze značek."""
        out = ""
        i = 0
        while i < len(parts):
            p = parts[i]
            if isinstance(p, str):
                out += p
            elif p[0] == "open":
                j = i + 1
                if j < len(parts) and parts[j] == ("close", p[1]):
                    i += 2
                    continue
                nxt = parts[j] if j < len(parts) and isinstance(parts[j], str) else ""
                lead = nxt[:len(nxt) - len(nxt.lstrip(" \t"))]
                out += lead + p[1]
                if nxt:
                    parts[j] = nxt[len(lead):]
            else:
                body = out.rstrip(" \t")
                trail = out[len(body):]
                out = body + p[1] + trail
            i += 1
        return out

    # ------------------------------------------------------------ bloky
    def convert(self, text: str) -> list[str]:
        """Posloupnost bloků Notion Markdownu → řádky Markdownu (relativně k odsazení 0)."""
        lines = text.split("\n")
        mlines = _mask(text).split("\n")
        blocks: list[list[str]] = []
        md: list[str] = []

        def flush() -> None:
            if md:
                blocks.append(self.inline("\n".join(md)).split("\n"))
                md.clear()

        i = 0
        while i < len(lines):
            if not self._block_tags(mlines[i]):
                md.append(lines[i])
                i += 1
                continue
            flush()
            depth, j = 0, i
            while j < len(lines):
                depth += self._depth_delta(mlines[j])
                j += 1
                if depth <= 0:
                    break
            indent = lines[i][:len(lines[i]) - len(lines[i].lstrip(" \t"))]
            region = [ln[len(indent):] if ln.startswith(indent) else ln.lstrip(" \t") for ln in lines[i:j]]
            out = self.region("\n".join(region))
            blocks.append([indent + ln if ln.strip() else "" for ln in out])
            i = j
        flush()
        return _join(blocks)

    @staticmethod
    def _block_tags(mline: str) -> list:
        return [m for m in _TAG.finditer(mline) if not _is_inline(m.group(2).lower())]

    def _depth_delta(self, mline: str) -> int:
        d = 0
        for m in self._block_tags(mline):
            closing, name, _a, selfclose = m.groups()
            if selfclose or name.lower() in _VOID:
                continue
            d += -1 if closing else 1
        return d

    def _elements(self, text: str) -> list[tuple]:
        """Prvky nejvyšší úrovně: ("text", s) | ("el", jméno, atributy, vnitřek, surový, uzavřený)."""
        masked = _mask(text)
        tags = [m for m in _TAG.finditer(masked) if not _is_inline(m.group(2).lower())]
        items: list[tuple] = []
        pos, i = 0, 0
        while i < len(tags):
            m = tags[i]
            closing, name, attr_s, selfclose = m.groups()
            name = name.lower()
            if m.start() > pos:
                items.append(("text", text[pos:m.start()]))
            if closing:                                         # osiřelá uzavírací značka
                self.flag("struktura")
                pos, i = m.end(), i + 1
                continue
            if selfclose or name in _VOID:
                items.append(("el", name, _attrs(attr_s), "", text[m.start():m.end()], True))
                pos, i = m.end(), i + 1
                continue
            depth, j = 1, i + 1
            while j < len(tags):
                c2, n2, _a2, sc2 = tags[j].groups()
                if n2.lower() == name and not sc2:
                    depth += -1 if c2 else 1
                    if depth == 0:
                        break
                j += 1
            if j >= len(tags):                                  # neuzavřená značka
                items.append(("el", name, _attrs(attr_s), text[m.end():], text[m.start():], False))
                pos = len(text)
                break
            items.append(("el", name, _attrs(attr_s), text[m.end():tags[j].start()],
                          text[m.start():tags[j].end()], True))
            pos, i = tags[j].end(), j + 1
        if pos < len(text):
            items.append(("text", text[pos:]))
        return items

    def region(self, text: str) -> list[str]:
        blocks = []
        for it in self._elements(text):
            if it[0] == "text":
                if it[1].strip():
                    blocks.append(self.convert(textwrap.dedent(it[1].strip("\n"))))
            else:
                blocks.append(self.element(*it[1:]))
        return _join(blocks)

    def _split(self, inner: str) -> tuple[str, str]:
        """Kontejner: titulek (text hned za značkou) a potomci (po prázdném řádku, blokové značce nebo odrážce)."""
        masked = _mask(inner)
        ends = [len(inner)]
        if (m := re.search(r"\n[ \t]*\n", masked)):
            ends.append(m.start())
        if (tags := self._block_tags(masked)):
            ends.append(tags[0].start())
        if (m := re.search(r"\n[ \t]*(?:[-*+]|\d+[.)]|>|#{1,6})(?:[ \t]|$)", masked, flags=re.M)):
            ends.append(m.start())
        if (m := re.search(r"\n[ \t]*(?:`{3,}|~{3,})", masked)):
            ends.append(m.start())
        end = min(ends)
        return inner[:end], inner[end:]

    def _title(self, title: str, attrs: dict) -> list[str]:
        lines = [ln.strip() for ln in self.inline(title.strip("\n")).split("\n") if ln.strip()]
        return [_wrap_color(ln, attrs) for ln in lines]

    def _children(self, children: str) -> list[str]:
        if not children.strip():
            return []
        return _trim(self.convert(textwrap.dedent(children.strip("\n"))))

    def element(self, name: str, attrs: dict, inner: str, raw: str, closed: bool) -> list[str]:
        if not closed:
            self.flag("struktura")
            return self._fenced(raw)
        if name in ("ul", "ol"):
            return self._list(name, attrs, inner)
        if name in _ITEMS:
            marker = "-" if name == "li" else ("- [x]" if attrs.get("checked") == "true" else "- [ ]")
            return self._item(marker, attrs, inner)
        if name in ("p", "empty-block"):
            return self._paragraph(attrs, inner)
        if name in _HEADINGS:
            title, children = self._split(inner)
            tl = self._title(title, attrs)
            head = _HEADINGS[name] + (" " + " ".join(tl) if tl else "")
            return _join([[head], self._children(children)])
        if name in _CONTAINERS:
            return self._quoted(name, attrs, inner)
        if name == "table":
            return self._table(attrs, inner, raw)
        if name in ("columns", "column"):
            self.flag("columns")
            if name == "column":
                return self._paragraph({}, inner)
            return _join([self._paragraph({}, it[3]) if it[0] == "el" and it[1] == "column"
                          else (self.region(it[1]) if it[0] == "text" and it[1].strip() else
                                (self.element(*it[1:]) if it[0] == "el" else []))
                          for it in self._elements(inner)])
        if name in ("page", "database"):
            self.flag("page")
            return [self._link(self.inline(inner.strip()), attrs.get("url") or attrs.get("href") or "")]
        if name in _MEDIA:
            self.flag("attachment")
            url = attrs.get("source") or attrs.get("src") or attrs.get("url") or ""
            cap = self.inline(inner.strip())
            if name == "image":
                return [f"![{cap}]({url})"]
            return [self._link(cap, url)]
        self.flag(f"unsupported:{name}")
        return self._fenced(raw)

    @staticmethod
    def _link(label: str, url: str) -> str:
        if not url:
            return label
        return f"[{label}]({url})" if label else f"<{url}>"

    @staticmethod
    def _fenced(raw: str) -> list[str]:
        longest = max((len(r) for r in re.findall(r"`+", raw)), default=0)
        fence = "`" * max(3, longest + 1)
        return [fence + FENCE, *raw.split("\n"), fence]

    def _paragraph(self, attrs: dict, inner: str) -> list[str]:
        title, children = self._split(inner)
        tl = self._title(title, attrs)
        return _join([tl or [""], self._children(children)]) if children.strip() else (tl or [""])

    def _item(self, marker: str, attrs: dict, inner: str) -> list[str]:
        title, children = self._split(inner)
        tl = self._title(title, attrs)
        # potomci odrážky `- ` o dvě mezery, číslované položky o šířku značky včetně mezery (`1. ` → 3; zadání 0.19.1)
        pad = " " * (len(marker) + 1 if marker[0].isdigit() else 2)
        out = [marker + (" " + tl[0] if tl else "")] + [pad + ln for ln in tl[1:]]
        ch = self._children(children)
        if ch:
            if not _is_list_line(ch[0]):
                out.append("")
            out += [pad + ln if ln.strip() else "" for ln in ch]
        return out

    def _list(self, name: str, attrs: dict, inner: str) -> list[str]:
        ordered = name == "ol"
        if ordered and attrs.get("type", "1") not in ("1", ""):
            self.flag("ol_type")
        n = int(attrs["start"]) if attrs.get("start", "").isdigit() else 1
        out: list[str] = []
        pad = "  "                                              # odsazení potomků poslední položky
        for it in self._elements(inner):
            if it[0] == "text":
                if it[1].strip():
                    out += self.convert(textwrap.dedent(it[1].strip("\n")))
                continue
            _, ename, eattrs, einner, eraw, eclosed = it
            if ename == "li" and eclosed:
                marker = f"{n}." if ordered else "-"
                out += self._item(marker, eattrs, einner)
                pad = " " * (len(marker) + 1)
                n += 1
            elif ename in ("ul", "ol") and out:                 # seznam přímo v seznamu: potomek předchozí položky
                out += [pad + ln if ln.strip() else "" for ln in self.element(*it[1:])]
            else:
                out += self.element(*it[1:])
        return out

    def _quoted(self, name: str, attrs: dict, inner: str) -> list[str]:
        title, children = self._split(inner)
        tl = self._title(title, attrs if name != "callout" else {})
        ch = self._children(children)
        if name == "quote":
            head = ["> " + ln for ln in tl] or [">"]
            if ch and tl and not _is_list_line(ch[0]):
                head.append(">")
        else:
            if name == "callout":
                kind = _CALLOUT_KIND.get((attrs.get("color") or "").removesuffix("_bg"), "note")
                icon = callout_icon(attrs)
                first = " ".join(x for x in (f"> [!{kind}]", icon, tl[0] if tl else "") if x)
            else:
                first = " ".join(x for x in ("> [!note]-", tl[0] if tl else "") if x)
            head = [first] + ["> " + ln for ln in tl[1:]]
        return head + ["> " + ln if ln.strip() else ">" for ln in ch]

    def _table(self, attrs: dict, inner: str, raw: str) -> list[str]:
        col_colors: list[str] = []
        rows: list[list[str]] = []
        for it in self._elements(inner):
            if it[0] != "el":
                continue
            _, ename, eattrs, einner, _eraw, _c = it
            if ename == "colgroup":
                col_colors = [c[2].get("color", "") for c in self._elements(einner) if c[0] == "el" and c[1] == "col"]
            elif ename == "tr":
                row = []
                for ci, c in enumerate(x for x in self._elements(einner) if x[0] == "el"):
                    _, cname, cattrs, cinner, _craw, _cc = c
                    if cname not in ("td", "th") or any(cattrs.get(k, "1") != "1" for k in ("colspan", "rowspan")) \
                            or self._block_tags(_mask(cinner)):
                        self.flag("unsupported:table")
                        return self._fenced(raw)
                    color = cattrs.get("color") or eattrs.get("color") or (col_colors[ci] if ci < len(col_colors)
                                                                            else "")
                    text = " ".join(ln.strip() for ln in self.inline(cinner).split("\n") if ln.strip())
                    text = re.sub(r"(?<!\\)\|", r"\\|", text)
                    row.append(_wrap_color(text, {"color": color}))
                rows.append(row)
        if not rows:
            self.flag("unsupported:table")
            return self._fenced(raw)
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        fmt = [("| " + " | ".join(r) + " |").replace("  |", " |") for r in rows]
        sep = "|" + " --- |" * width
        if attrs.get("header-row") == "true":
            return [fmt[0], sep, *fmt[1:]]
        # bez záhlaví: prázdný řádek záhlaví a všechny řádky v těle (zadání 0.19.1)
        return ["|" + " |" * width, sep, *fmt]


# ---------------------------------------------------------------- kontrola věrnosti

def _prefix(line: str) -> tuple[int, int, str]:
    """(odsazení bez značek citace, hloubka citace, zbytek řádku)."""
    ind, q, i = 0, 0, 0
    while True:
        while i < len(line) and line[i] in " \t":
            ind += 4 if line[i] == "\t" else 1
            i += 1
        if i < len(line) and line[i] == ">":
            q += 1
            i += 1
            if i < len(line) and line[i] == " ":
                i += 1
            continue
        return ind, q, line[i:]


def _blank_extents(masked: str) -> str:
    """Ve zdroji vyprázdní tabulky a nepodporované bloky (ve výstupu jsou v ohrazení nebo bez seznamů)."""
    chars = list(masked)
    tags = list(_TAG.finditer(masked))
    i = 0
    while i < len(tags):
        closing, name, _a, selfclose = tags[i].groups()
        name = name.lower()
        if closing or selfclose or _is_inline(name) or (name in _SUPPORTED_BLOCK_SET and name != "table"):
            i += 1
            continue
        depth, j = 1, i + 1
        while j < len(tags):
            c2, n2, _a2, sc2 = tags[j].groups()
            if n2.lower() == name and not sc2:
                depth += -1 if c2 else 1
                if depth == 0:
                    break
            j += 1
        end = tags[j].end() if j < len(tags) else len(masked)
        for k in range(tags[i].start(), end):
            if chars[k] != "\n":
                chars[k] = " "
        while i < len(tags) and tags[i].start() < end:
            i += 1
    return "".join(chars)


_SUPPORTED_BLOCK_SET = _SUPPORTED_BLOCKS | {"tr", "td", "th", "colgroup", "col"}


def structure(text: str, source: bool) -> tuple[dict, int]:
    """Strom seznamů (počet položek na každé úrovni) a počet kontejnerů (citace, callout, toggle)."""
    masked = _mask(text)
    if source:
        masked = _blank_extents(masked)
    masked = masked.replace("\x00", " ")
    frames: list[list[int]] = [[]]
    lists: Counter = Counter()
    containers, prev_q = 0, 0

    def depth() -> int:
        return sum(len(f) for f in frames) + len(frames) - 1

    for line in masked.split("\n"):
        ind, q, s = _prefix(line)
        if not s.strip() and not q:
            prev_q = 0
            continue
        containers += max(0, q - prev_q)
        prev_q = q
        md = frames[-1]
        if _BULLET.match(s):
            while md and md[-1] >= ind:
                md.pop()
            lists[depth()] += 1
            md.append(ind)
        elif s.strip() and not (source and s.startswith("<")):
            while md and md[-1] >= ind:
                md.pop()
        if not source:
            continue
        for m in _TAG.finditer(s):
            closing, name, _a, selfclose = m.groups()
            name = name.lower()
            if name in _ITEMS:
                if closing:
                    if len(frames) > 1:
                        frames.pop()
                else:
                    lists[depth()] += 1
                    if not selfclose:
                        frames.append([])
            elif name in ("ul", "ol") and not closing:
                md = frames[-1]
                while md and md[-1] >= ind:
                    md.pop()
            elif name in _CONTAINERS and not closing and not selfclose:
                containers += 1
    return dict(lists), containers


def _source_text(text: str) -> str:
    """Zdroj pro srovnání textu: data zmínek textem, citace adresou, ikona calloutu v titulku (jako ve výstupu)."""
    def date_sub(m):
        return date_text(_attrs(m.group(2))) or m.group(0)

    text = re.sub(r"<(mention-date|date)\b([^<>\n]*?)\s*/>", date_sub, text, flags=re.I)
    text = re.sub(r"<(mention-date|date)\b([^<>\n]*?)>\s*</\1>", date_sub, text, flags=re.I)
    text = _CITATION.sub(r"\1", text)
    return re.sub(r"<callout\b([^<>\n]*)>",
                  lambda m: "<callout> " + callout_icon(_attrs(m.group(1))) + " ", text, flags=re.I)


def plain(text: str) -> str:
    """Text bez značek Markdownu a HTML, bílé znaky sjednocené."""
    t = text.replace("\\|", "|")
    t = re.sub(r"!?\[([^\]\n]*)\]\(([^)\n]*)\)", r"\1", t)
    t = re.sub(r"<[A-Za-z][\w+.-]*:[^<>\s]*>", "", t)
    t = _TAG.sub(lambda m: "" if _is_inline(m.group(2).lower()) else " ", t)    # bloková značka odděluje slova
    t = re.sub(r"\[![\w-]+\][-+]?", "", t)
    out = []
    for line in t.split("\n"):
        s = line
        while True:
            s = s.lstrip(" \t")
            if s.startswith(">"):
                s = s[1:]
                continue
            m = (re.match(r"(?:[-*+]|\d+[.)])(?:[ \t]+|$)", s) or re.match(r"\[[ xX]\](?:[ \t]+|$)", s)
                 or re.match(r"#{1,6}(?:[ \t]+|$)", s))
            if m and m.end():
                s = s[m.end():]
                continue
            break
        if re.match(r"(`{3,}|~{3,})", s) or re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*", s):
            continue
        out.append(s.replace("**", "").replace("~~", "").replace("*", "").replace("|", ""))
    return " ".join(" ".join(out).split())


def faithful(source: str, output: str) -> bool:
    return plain(_source_text(source)) == plain(output) and structure(source, True) == structure(output, False)


def notion_md_to_markdown(content: str) -> tuple[str, list[str]]:
    """Převod `notion-md` → Markdown; vrací (text, druhy ruční kontroly)."""
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    conv = _Converter()
    lines = conv.convert(content)
    while lines and not lines[-1].strip():
        lines.pop()
    out = "\n".join(lines)
    if "struktura" not in conv.kinds and not faithful(content, out):
        conv.flag("struktura")
    return out, conv.kinds
