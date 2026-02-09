
import os
import re

TERM_PATTERNS = [
    (r"Khaloree", "Khalorēē"),
    (r"khaloree", "Khalorēē"),
    (r"Khalorée", "Khalorēē"),
    (r"\bnoesis\b", "NOESIS"),
    (r"\bwitnessOS\b", "WitnessOS"),
    (r"\btryambakam\b", "Tryambakam"),
    (r"Prana", "Prana (Check capitalization)"),
    (r"\bprana\b", "Prana"),
    (r"Somanaut", "Somanaut"),
    (r"\bsomanaut\b", "Somanaut"),
    (r"Lethe", "Lethe"),
    (r"\blethe\b", "Lethe"),
    (r"Aletheia", "Aletheia"),
    (r"\baletheia\b", "Aletheia")
]

BOOKS = [
    "02_MANUSCRIPTS/COMPILED/Book_1_Anamnesis_Engine.md",
    "02_MANUSCRIPTS/COMPILED/Book_2_The_Myocardial_Chorus.md",
    "02_MANUSCRIPTS/COMPILED/Book_3_The_Ripening.md"
]

BASE_PATH = "/Volumes/madara/2026/twc-vault/01-Projects/Somatic-Canticles"

report = ["# MANUSCRIPT CONSISTENCY REPORT\n"]

for book_rel_path in BOOKS:
    path = os.path.join(BASE_PATH, book_rel_path)
    if not os.path.exists(path):
        report.append(f"## {book_rel_path}\n**FILE NOT FOUND**\n")
        continue

    report.append(f"## {os.path.basename(path)}\n")
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    issues_found = 0
    
    # Check Chapter Sequence
    # Assuming chapters start with "# Chapter XX" or "## Chapter XX"
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Check Terms
        for pattern, correction in TERM_PATTERNS:
            if re.search(pattern, line) and correction not in line: # Simple check, false positives possible if correct term is also on line
                 # Strict check: if the MATCH itself is not the valid term.
                 # Actually regex match is better.
                 matches = re.finditer(pattern, line)
                 for match in matches:
                     found_text = match.group(0)
                     if found_text != correction and found_text != correction.lower(): # Allow exact match if it was meant to be lowercase, but we suspect it shouldn't
                         # Wait, logic:
                         # If found "Khaloree", it's wrong.
                         # If found "noesis", it's likely wrong (should be NOESIS).
                         if found_text != correction:
                             report.append(f"- Line {line_num}: Found `{found_text}`, likely should be `{correction}`.")
                             issues_found += 1

    if issues_found == 0:
        report.append("No terminology issues found.\n")
    else:
        report.append(f"\nTotal potential issues: {issues_found}\n")

output_path = os.path.join(BASE_PATH, "03_EDITORIAL/consistency_report.md")
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(report)

print(f"Report generated at {output_path}")
