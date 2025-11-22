from scoring import compute_overall
from utils import save_json

def main():
    print("Paste your transcript below. Enter an empty line when done:")
    lines = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        except EOFError:
            break
    text = " ".join(lines)
    result = compute_overall(text)
    save_json(result)
    print("Analysis saved to reports/output.json")
    print(result)

if __name__ == "__main__":
    main()
