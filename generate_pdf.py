import os
from fpdf import FPDF
import glob

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Courier", size=8)

target_files = []
for ext in ["*.py", "Dockerfile", "requirements.txt", "*.md"]:
    if ext == "*.md": continue # Skip markdown, just focusing on code for now as requested
    target_files.extend(glob.glob(f"**/{ext}", recursive=True))

target_files = [f for f in target_files if "__pycache__" not in f and "venv" not in f]

for filepath in sorted(target_files):
    pdf.set_font("Courier", style="B", size=10)
    pdf.cell(0, 10, txt=f"File: {filepath}", ln=1)
    pdf.set_font("Courier", size=8)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            # Replace unsupported characters with standard equivalents or omit them
            line = line.encode('latin-1', 'replace').decode('latin-1')
            line = line.replace('\n', '')
            pdf.cell(0, 4, txt=f"{i+1:4d}: {line}", ln=1)
        pdf.cell(0, 10, txt="", ln=1) # Spacer
    except Exception as e:
        pdf.cell(0, 4, txt=f"Error reading file: {e}", ln=1)
        pdf.cell(0, 10, txt="", ln=1)

output_path = r"C:\Users\Nick\.gemini\antigravity\brain\014cb234-6e69-444a-b355-c2981b1137f8\AETHERIUS_FULL_CODEBASE.pdf"
pdf.output(output_path)
print(f"PDF generated successfully at {output_path}")
