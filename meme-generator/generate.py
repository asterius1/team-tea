#!/usr/bin/env python3
"""
Void Council Meme Generator
Downloads pre-composed memes from memegen.link and saves them to assets/memes/.
Run from repo root: python meme-generator/generate.py
"""

import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "assets" / "memes"
API_BASE   = "https://api.memegen.link/images"
WIDTH      = 600

# ─── Meme definitions ────────────────────────────────────────────────────────
# texts: list of panel texts (order matches template panels top-to-bottom)
# caption: shown under the image on the gallery page

MEMES = [
    {
        "filename": "01-drake.png",
        "template": "drake",
        "texts":    ["Quarantine coffee", "Void Council tea"],
        "caption":  "Every recruit, eventually.",
        "exhibit":  "A",
    },
    {
        "filename": "02-gru.png",
        "template": "gru",
        "texts":    [
            "Join April Fools on the fun team",
            "Realise they serve coffee",
            "Realise they serve coffee",
            "Realise they serve coffee",
        ],
        "caption":  "A cautionary tale in four panels.",
        "exhibit":  "B",
    },
    {
        "filename": "03-woman-cat.png",
        "template": "woman-cat",
        "texts":    [
            "COFFEE IS OBJECTIVELY BETTER CHANGE MY MIND",
            "Void Council sipping tea unbothered",
        ],
        "caption":  "Quarantine vs Void Council. Every day.",
        "exhibit":  "C",
    },
    {
        "filename": "04-fine.png",
        "template": "fine",
        "texts":    ["Quarantine HQ after discovering the other team has tea"],
        "caption":  "Source: someone who was there.",
        "exhibit":  "D",
    },
    {
        "filename": "05-mordor.png",
        "template": "mordor",
        "texts":    ["One does not simply", "beat the tea drinkers"],
        "caption":  "Boromir understood the assignment.",
        "exhibit":  "E",
    },
    {
        "filename": "06-pigeon.png",
        "template": "pigeon",
        "texts":    ["Tea", "Quarantine", "Is this coffee?"],
        "caption":  "A genuine cry for help.",
        "exhibit":  "F",
    },
    {
        "filename": "07-cmm.png",
        "template": "cmm",
        "texts":    ["Tea is objectively superior to coffee"],
        "caption":  "Nobody could. Nobody tried very hard.",
        "exhibit":  "G",
    },
    {
        "filename": "08-panik-kalm-panik.png",
        "template": "panik-kalm-panik",
        "texts":    [
            "I have to pick an April Fools team",
            "I joined Void Council",
            "We have been playing for six hours",
        ],
        "caption":  "An accurate timeline of events.",
        "exhibit":  "H",
    },
    {
        "filename": "09-fry.png",
        "template": "fry",
        "texts":    [
            "Not sure if winning because we are good",
            "or because tea gives us actual superpowers",
        ],
        "caption":  "The scientists are looking into it.",
        "exhibit":  "I",
    },
    {
        "filename": "10-rollsafe.png",
        "template": "rollsafe",
        "texts":    [
            "Can not lose to Quarantine",
            "if you are already on Void Council",
        ],
        "caption":  "Flawless strategic logic.",
        "exhibit":  "J",
    },
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def encode_text(text: str) -> str:
    """Encode text for memegen.link URL segments."""
    return (
        text
        .replace("%",  "~p")
        .replace("?",  "~q")
        .replace("&",  "~a")
        .replace("#",  "~h")
        .replace("/",  "~s")
        .replace("\\", "~b")
        .replace("<",  "~l")
        .replace(">",  "~g")
        .replace('"',  "''")
        .replace(" ",  "_")
        .replace("\n", "~n")
    )

def build_url(template: str, texts: list[str]) -> str:
    segments = "/".join(encode_text(t) for t in texts)
    return f"{API_BASE}/{template}/{segments}.png?width={WIDTH}"

def download(url: str, dest: Path, retries: int = 3) -> bool:
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "VoidCouncilMemeGen/1.0"},
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                dest.write_bytes(resp.read())
            return True
        except Exception as exc:
            print(f"    attempt {attempt}/{retries} failed: {exc}")
            if attempt < retries:
                time.sleep(2)
    return False

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ok  = []
    bad = []

    for meme in MEMES:
        dest = OUTPUT_DIR / meme["filename"]
        url  = build_url(meme["template"], meme["texts"])
        label = f"[{meme['exhibit']}] {meme['filename']}"

        if dest.exists():
            print(f"  skip  {label}  (already exists, delete to re-download)")
            ok.append(meme)
            continue

        print(f"  fetch {label}")
        print(f"        {url}")
        if download(url, dest):
            size = dest.stat().st_size // 1024
            print(f"        ✓  {size} KB")
            ok.append(meme)
        else:
            print(f"        ✗  FAILED")
            bad.append(meme)

        time.sleep(0.5)   # be polite to the free API

    print(f"\n{'='*50}")
    print(f"  Done: {len(ok)} downloaded, {len(bad)} failed")
    if bad:
        print("  Failed memes:")
        for m in bad:
            print(f"    - {m['filename']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
