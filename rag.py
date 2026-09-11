from pathlib import Path

file_path = Path("knowledge_base/ml_interview_questions.txt")

data = file_path.read_text()

print(data[:500])