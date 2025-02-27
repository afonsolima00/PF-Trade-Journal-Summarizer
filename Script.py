import os
import csv
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Directory containing your trade log files
DIR_PATH = r"C:\Users\neves\OneDrive\Ambiente de Trabalho\Projects\Task 14"
def parse_trade_log(file_path):
    """Parse a trade log file and extract its sections."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    sections = {"entry": [], "exit": [], "rationale": []}
    current_section = None
    for line in lines:
        line = line.strip()
        if line == "== Entry ==":
            current_section = "entry"
        elif line == "== Exit ==":
            current_section = "exit"
        elif line == "== Rationale ==":
            current_section = "rationale"
        elif current_section and line:  # Only append non-empty lines
            sections[current_section].append(line)
    # Join lines with newlines to preserve formatting for summarization
    for key in sections:
        sections[key] = "\n".join(sections[key])
    return sections

# Initialize tokenizer and summarizer once for efficiency
tokenizer = Tokenizer("english")
summarizer = TextRankSummarizer()

# Get all .txt files from the directory
files = [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]

# List to store trade summaries
summaries = []

for file in files:
    file_path = os.path.join(DIR_PATH, file)
    # Extract trade date from filename (e.g., "2023-10-01" from "trade_2023-10-01.txt")
    trade_id = file.split('_')[1].split('.')[0]
    
    # Parse the trade log file
    sections = parse_trade_log(file_path)
    rationale_text = sections["rationale"]
    
    # Skip if there's no rationale to summarize
    if not rationale_text:
        continue
    
    # Summarize the rationale into 2 sentences
    parser = PlaintextParser.from_string(rationale_text, tokenizer)
    summary_sentences = summarizer(parser.document, 2)  # 2 sentences for conciseness
    
    # Format summary as bullet points
    bullet_points = ["• " + str(sentence) for sentence in summary_sentences]
    summary_text = "\n".join(bullet_points)
    
    # Add to summaries list
    summaries.append({"trade_id": trade_id, "summary": summary_text})

# Write summaries to a CSV file
with open("trade_summaries.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["trade_id", "summary"])
    writer.writeheader()
    for summary in summaries:
        writer.writerow(summary)

print("Summaries have been saved to trade_summaries.csv")