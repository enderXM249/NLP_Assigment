import os
import re
import sys
import getpass
import pandas as pd


def get_token():
    token = os.environ.get("HF_TOKEN")
    if not token:
        token = getpass.getpass("Paste your HF token (input hidden, not stored): ").strip()
    return token


def word_count(text) -> int:
    if not isinstance(text, str):
        return 0
    return len(re.findall(r"\S+", text.strip()))


def load_hf_dataset():
    from huggingface_hub import login, hf_hub_download

    login(token=get_token())
    print("Downloading eng.txt and hin.txt from ainlpml/english-hindi ...")
    eng_path = hf_hub_download(repo_id="ainlpml/english-hindi", repo_type="dataset", filename="eng.txt")
    hin_path = hf_hub_download(repo_id="ainlpml/english-hindi", repo_type="dataset", filename="hin.txt")

    with open(eng_path, encoding="utf-8") as f:
        eng_lines = f.read().splitlines()
    with open(hin_path, encoding="utf-8") as f:
        hin_lines = f.read().splitlines()

    n = min(len(eng_lines), len(hin_lines))
    if len(eng_lines) != len(hin_lines):
        print(f"WARNING: eng.txt has {len(eng_lines)} lines, hin.txt has {len(hin_lines)} lines. "
              f"Truncating both to {n} aligned lines.")

    df = pd.DataFrame({"english": eng_lines[:n], "hindi": hin_lines[:n]})
    print(f"Loaded {len(df)} line-aligned sentence pairs.")
    return df


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Already normalized to english/hindi columns by load_hf_dataset(); pass through.
    return df[["english", "hindi"]]


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "final_dataset.xlsx"

    df = load_hf_dataset()
    df = normalize_columns(df)
    df = df.dropna(subset=["english", "hindi"]).reset_index(drop=True)
    print(f"Rows with both languages present: {len(df)}")

    df["word_count_english"] = df["english"].apply(word_count)
    df["word_count_hindi"] = df["hindi"].apply(word_count)

    mask_len = df["word_count_english"].between(5, 50) & df["word_count_hindi"].between(5, 50)
    df = df[mask_len].copy()
    print(f"After 5-50 word-count filter: {len(df)} pairs.")

    df["difference"] = df["word_count_english"] - df["word_count_hindi"]
    df = df[df["difference"].between(-10, 10)].copy()
    print(f"After difference filter (-10 to +10): {len(df)} pairs.")

    if len(df) < 10000:
        print(f"WARNING: only {len(df)} rows remain; assessment asked for >= 10,000.")

    final = df.rename(columns={
        "english": "English Sentences",
        "hindi": "Hindi Sentences",
        "word_count_english": "Word Count (English)",
        "word_count_hindi": "Word Count (Hindi)",
        "difference": "Difference (Eng - Hindi)",
    })[["English Sentences", "Hindi Sentences", "Word Count (English)",
        "Word Count (Hindi)", "Difference (Eng - Hindi)"]]

    final.to_excel(out_path, index=False, engine="openpyxl")
    print(f"Saved {len(final)} rows to {out_path}")


if __name__ == "__main__":
    main()