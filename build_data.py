"""
Build data/results.js from the HoC Library GE2024 CSV.

Usage:
    python3 build_data.py --input "HoC-GE2024-results-by-constituency.csv"

Output:
    data/results.js  (overwritten each run)
"""

import csv, json, sys, os, argparse

# Map CSV column names -> our internal party codes
PARTY_COLS = [
    ("Con",   "CON"),
    ("Lab",   "LAB"),
    ("LD",    "LD"),
    ("RUK",   "REF"),   # Reform UK
    ("Green", "GRN"),
    ("SNP",   "SNP"),
    ("PC",    "PC"),
    ("DUP",   "DUP"),
    ("SF",    "SF"),
    ("SDLP",  "SDLP"),
    ("UUP",   "UUP"),
    ("APNI",  "APNI"),
    ("All other candidates", "OTHER"),
]

# Map the CSV "First party" / "Second party" values -> our codes
PARTY_NAME_MAP = {
    "Con":   "CON",
    "Lab":   "LAB",
    "LD":    "LD",
    "RUK":   "REF",
    "Green": "GRN",
    "SNP":   "SNP",
    "PC":    "PC",
    "DUP":   "DUP",
    "SF":    "SF",
    "SDLP":  "SDLP",
    "UUP":   "UUP",
    "APNI":  "APNI",
    "Ind":   "OTHER",
    "Spk":   "OTHER",
}

def parse_int(s):
    s = s.strip().replace(",", "")
    return int(s) if s else 0

def build(input_path):
    output = {}

    with open(input_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ons_id   = row["ONS ID"].strip()
            name     = row["Constituency name"].strip()
            valid    = parse_int(row["Valid votes"])

            if not ons_id or valid == 0:
                continue

            # Build results list — only include parties with >0 votes
            results = []
            for col, code in PARTY_COLS:
                votes = parse_int(row.get(col, "0"))
                if votes > 0:
                    share = round(votes / valid * 100, 1)
                    results.append({"party": code, "votes": votes, "share": share})

            # Sort by votes descending
            results.sort(key=lambda r: r["votes"], reverse=True)

            # Winner = First party column (more reliable than deriving from votes)
            winner_raw = row.get("First party", "").strip()
            winner = PARTY_NAME_MAP.get(winner_raw, "OTHER")

            output[ons_id] = {
                "ons_id":  ons_id,
                "name":    name,
                "winner":  winner,
                "results": results,
            }

    return output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to HoC GE2024 CSV")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: file not found: {args.input}")
        sys.exit(1)

    print(f"Reading {args.input} ...")
    data = build(args.input)
    print(f"Parsed {len(data)} constituencies.")

    os.makedirs("data", exist_ok=True)
    js = "const CONSTITUENCY_DATA = " + json.dumps(data, separators=(",", ":")) + ";"
    with open("data/results.js", "w", encoding="utf-8") as f:
        f.write(js)

    size_kb = os.path.getsize("data/results.js") // 1024
    print(f"Written data/results.js ({size_kb} KB)")

    # Quick sanity check
    winners = {}
    for s in data.values():
        w = s["winner"]
        winners[w] = winners.get(w, 0) + 1
    print("Winners breakdown:")
    for party, count in sorted(winners.items(), key=lambda x: -x[1]):
        print(f"  {party:6s} {count}")

if __name__ == "__main__":
    main()