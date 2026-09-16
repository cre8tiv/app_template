#!/usr/bin/env python3
import re
from collections import Counter
from pathlib import Path

URL_REGEX = re.compile(r"https?://[^\s)]+")
FENCE_OPEN_REGEX = re.compile(r"^(\s{0,3})(`{3,}|~{3,})(.*)$")
INDENTED_BLOCK_REGEX = re.compile(r"^( {4}|\t)")
HEADING_REGEX = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)
BULLET_REGEX = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
ORDERED_LIST_REGEX = re.compile(r"^(\s*)(\d+)\.\s+", re.MULTILINE)
DATE_REGEX = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?(?:[+-]\d{2}:?\d{2}|Z)?)?\b")
VERSION_REGEX = re.compile(r"\bv?(?:\d+\.\d+(?:\.\d+)?(?:-[a-zA-Z0-9.]+)?)\b")
NUMERIC_REGEX = re.compile(r"\b\d+(?:\.\d+)?\b")
COMMAND_REGEX = re.compile(
    r"\b(?:npm|git|docker|pip|pip3|cargo|npx|yarn|brew|apt|apt-get|dotnet|node|python|python3|claude|supabase|psql|kubectl|helm|terraform|az|aws|gcloud|curl|wget|ssh|gh|jq|make|cmake|go|rustc|deno|bun|pnpm|ng|prisma|vercel|firebase|netlify|systemctl|journalctl|sudo|docker-compose)\s+\S",
    re.IGNORECASE
)
FRONTMATTER_REGEX = re.compile(r"\A(---\r?\n.*?\r?\n---\r?\n)", re.DOTALL)

# crude but effective path detection
# Requires either a path prefix (./ ../ / or drive letter) or a slash/backslash within the match
PATH_REGEX = re.compile(r"(?:\./|\.\./|/|[A-Za-z]:\\)[\w\-/\\\.]+|[\w\-\.]+[/\\][\w\-/\\\.]+")


class ValidationResult:
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []

    def add_error(self, msg):
        self.is_valid = False
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------- Extractors ----------


def extract_headings(text):
    return [(level, title.strip()) for level, title in HEADING_REGEX.findall(text)]


def extract_code_blocks(text):
    """Line-based fenced and indented code block extractor.

    Handles ``` and ~~~ fences with variable length (CommonMark: closing
    fence must use same char and be at least as long as opening). Supports
    nested fences (e.g. an outer 4-backtick block wrapping inner 3-backtick
    content). Also detects four-space/tab-indented CommonMark code blocks.
    """
    blocks = []
    lines = text.split("\n")
    i = 0
    n = len(lines)
    while i < n:
        m = FENCE_OPEN_REGEX.match(lines[i])
        if m:
            fence_char = m.group(2)[0]
            fence_len = len(m.group(2))
            open_line = lines[i]
            block_lines = [open_line]
            i += 1
            closed = False
            while i < n:
                close_m = FENCE_OPEN_REGEX.match(lines[i])
                if (
                    close_m
                    and close_m.group(2)[0] == fence_char
                    and len(close_m.group(2)) >= fence_len
                    and close_m.group(3).strip() == ""
                ):
                    block_lines.append(lines[i])
                    closed = True
                    i += 1
                    break
                block_lines.append(lines[i])
                i += 1
            if closed:
                blocks.append("\n".join(block_lines))
            elif len(block_lines) > 1:
                # Unclosed fence that reached EOF — still append its contents
                # so validation catches any corruption inside the block.
                blocks.append("\n".join(block_lines))
            continue

        # Four-space/tab-indented CommonMark code block (fences take priority).
        if INDENTED_BLOCK_REGEX.match(lines[i]):
            block_lines = [lines[i]]
            i += 1
            while i < n:
                if INDENTED_BLOCK_REGEX.match(lines[i]) or lines[i].strip() == "":
                    block_lines.append(lines[i])
                    i += 1
                else:
                    break
            if any(line.strip() for line in block_lines):
                blocks.append("\n".join(block_lines))
            continue

        i += 1
    return blocks


def extract_urls(text):
    return Counter(URL_REGEX.findall(text))


def extract_paths(text):
    return Counter(PATH_REGEX.findall(text))


def extract_dates(text):
    return set(DATE_REGEX.findall(text))


def extract_versions(text):
    return set(VERSION_REGEX.findall(text))


def extract_numeric(text):
    return set(NUMERIC_REGEX.findall(text))


def extract_commands(text):
    return set(COMMAND_REGEX.findall(text))


def extract_frontmatter(text):
    m = FRONTMATTER_REGEX.match(text)
    return m.group(1) if m else ""


def count_bullets(text):
    return len(BULLET_REGEX.findall(text))


def extract_list_items(text):
    """Extract (indent_level, marker, content) for every list line.

    Handles unordered (-, *, +) and ordered (1., 2., etc.) list markers.
    Indent level is measured in characters (spaces/tabs) before the marker.
    """
    items = []
    for line in text.split("\n"):
        m = BULLET_REGEX.match(line)
        if m:
            indent = len(line) - len(line.lstrip())
            marker = m.group(0).strip()
            content = line[m.end():]
            items.append((indent, marker, content))
            continue
        m = ORDERED_LIST_REGEX.match(line)
        if m:
            indent = len(m.group(1))
            marker = m.group(2) + "."
            content = line[m.end():]
            items.append((indent, marker, content))
    return items


def extract_inline_codes(text):
    """Backtick-delimited inline spans, with fenced code blocks stripped first.

    Previously used a column-0-anchored regex to strip fences, which misses
    fences indented 1-3 spaces (valid CommonMark). Reuse extract_code_blocks
    (FENCE_OPEN_REGEX-based, indentation-aware) instead so an indented fence's
    body backticks don't leak into inline-code pairing.
    """
    text_without_fences = text
    for block in extract_code_blocks(text):
        text_without_fences = text_without_fences.replace(block, "", 1)
    return re.findall(r"`([^`]+)`", text_without_fences)


# ---------- Validators ----------


def validate_headings(orig, comp, result):
    h1 = extract_headings(orig)
    h2 = extract_headings(comp)

    if len(h1) != len(h2):
        result.add_error(f"Heading count mismatch: {len(h1)} vs {len(h2)}")

    if h1 != h2:
        result.add_error("Heading text/order changed")


def validate_code_blocks(orig, comp, result):
    c1 = extract_code_blocks(orig)
    c2 = extract_code_blocks(comp)

    if c1 != c2:
        result.add_error("Code blocks not preserved exactly")


def validate_urls(orig, comp, result):
    u1 = extract_urls(orig)
    u2 = extract_urls(comp)

    if u1 != u2:
        lost = {k for k, v in u1.items() if u2.get(k, 0) < v}
        added = {k for k, v in u2.items() if u1.get(k, 0) < v}
        parts = []
        if lost:
            parts.append(f"lost={lost}")
        if added:
            parts.append(f"added={added}")
        result.add_error(f"URL mismatch: {', '.join(parts)}")


def validate_paths(orig, comp, result):
    p1 = extract_paths(orig)
    p2 = extract_paths(comp)

    if p1 != p2:
        lost = {k for k, v in p1.items() if p2.get(k, 0) < v}
        added = {k for k, v in p2.items() if p1.get(k, 0) < v}
        parts = []
        if lost:
            parts.append(f"lost={lost}")
        if added:
            parts.append(f"added={added}")
        result.add_error(f"Path mismatch: {', '.join(parts)}")


def validate_dates(orig, comp, result):
    d1 = extract_dates(orig)
    d2 = extract_dates(comp)
    if d1 != d2:
        result.add_error(f"Date mismatch: lost={d1 - d2}, added={d2 - d1}")


def validate_versions(orig, comp, result):
    v1 = extract_versions(orig)
    v2 = extract_versions(comp)
    if v1 != v2:
        result.add_error(f"Version mismatch: lost={v1 - v2}, added={v2 - v1}")


def validate_numeric(orig, comp, result):
    n1 = extract_numeric(orig)
    n2 = extract_numeric(comp)
    if n1 != n2:
        result.add_error(f"Numeric value mismatch: lost={n1 - n2}, added={n2 - n1}")


def validate_commands(orig, comp, result):
    c1 = extract_commands(orig)
    c2 = extract_commands(comp)
    if c1 != c2:
        result.add_error(f"Command mismatch: lost={c1 - c2}, added={c2 - c1}")


def validate_frontmatter(orig, comp, result):
    f1 = extract_frontmatter(orig)
    f2 = extract_frontmatter(comp)
    if f1 != f2:
        result.add_error("YAML frontmatter changed")


def validate_bullets(orig, comp, result):
    b1 = count_bullets(orig)
    b2 = count_bullets(comp)

    if b1 == 0:
        return

    diff = abs(b1 - b2) / b1

    if diff > 0.15:
        result.add_error(f"Bullet count changed too much: {b1} -> {b2}")
        return

    # Compare list structure: markers, nesting, and ordered values.
    orig_items = extract_list_items(orig)
    comp_items = extract_list_items(comp)

    if len(orig_items) != len(comp_items):
        result.add_error(f"List item count mismatch: {len(orig_items)} vs {len(comp_items)}")
        return

    for idx, (oi, ci) in enumerate(zip(orig_items, comp_items)):
        o_indent, o_marker, o_content = oi
        c_indent, c_marker, c_content = ci
        if o_indent != c_indent:
            result.add_error(f"List item {idx}: indent changed ({o_indent} -> {c_indent})")
            return
        if o_marker != c_marker:
            result.add_error(f"List item {idx}: marker changed ('{o_marker}' -> '{c_marker}')")
            return


def validate_inline_codes(orig, comp, result):
    c1 = Counter(extract_inline_codes(orig))
    c2 = Counter(extract_inline_codes(comp))

    if c1 != c2:
        lost = set(c1.keys()) - set(c2.keys())
        added = set(c2.keys()) - set(c1.keys())
        for code, count in c1.items():
            if code in c2 and c2[code] < count:
                lost.add(f"{code} (lost {count - c2[code]} of {count} occurrences)")
        if lost:
            result.add_error(f"Inline code lost: {lost}")
        if added:
            result.add_warning(f"Inline code added: {added}")


# ---------- Main ----------


def validate(original_path: Path, compressed_path: Path) -> ValidationResult:
    result = ValidationResult()

    orig = read_file(original_path)
    comp = read_file(compressed_path)

    validate_headings(orig, comp, result)
    validate_code_blocks(orig, comp, result)
    validate_urls(orig, comp, result)
    validate_paths(orig, comp, result)
    validate_dates(orig, comp, result)
    validate_versions(orig, comp, result)
    validate_numeric(orig, comp, result)
    validate_commands(orig, comp, result)
    validate_frontmatter(orig, comp, result)
    validate_bullets(orig, comp, result)
    validate_inline_codes(orig, comp, result)

    return result


# ---------- CLI ----------

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python validate.py <original> <compressed>")
        sys.exit(1)

    orig = Path(sys.argv[1]).resolve()
    comp = Path(sys.argv[2]).resolve()

    res = validate(orig, comp)

    print(f"\nValid: {res.is_valid}")

    if res.errors:
        print("\nErrors:")
        for e in res.errors:
            print(f"  - {e}")

    if res.warnings:
        print("\nWarnings:")
        for w in res.warnings:
            print(f"  - {w}")
