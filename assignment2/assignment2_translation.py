import sys
import pandas as pd


def load_source(path: str, n: int, seed: int = 42) -> pd.DataFrame:
    df = pd.read_excel(path)
    col_map = {c.lower().strip(): c for c in df.columns}
    en_col = col_map.get("english sentences") or col_map.get("english")
    hi_col = col_map.get("hindi sentences") or col_map.get("hindi")
    if not en_col or not hi_col:
        raise ValueError(f"Could not find English/Hindi columns. Found: {list(df.columns)}")

    df = df[[en_col, hi_col]].rename(columns={en_col: "english", hi_col: "hindi_reference"})
    df = df.dropna().drop_duplicates(subset="english").reset_index(drop=True)

    if len(df) < n:
        print(f"WARNING: only {len(df)} rows available, using all of them instead of {n}.")
        n = len(df)
    return df.sample(n=n, random_state=seed).reset_index(drop=True)


def translate_batch(sentences, model_name="Helsinki-NLP/opus-mt-en-hi", batch_size=8):
    from transformers import pipeline
    print(f"Loading model '{model_name}' (first run downloads ~300MB, then cached) ...")
    translator = pipeline("translation", model=model_name)

    outputs = []
    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i + batch_size]
        results = translator(batch, max_length=256)
        outputs.extend([r["translation_text"] for r in results])
        print(f"  translated {min(i + batch_size, len(sentences))}/{len(sentences)}")
    return outputs


def compute_scores(hypotheses, references):
    from sacrebleu.metrics import BLEU, CHRF, TER
    refs = [references]  # sacrebleu expects list-of-lists (one list per reference set)

    bleu = BLEU().corpus_score(hypotheses, refs)
    chrf = CHRF().corpus_score(hypotheses, refs)
    ter = TER().corpus_score(hypotheses, refs)
    return bleu, chrf, ter


def main():
    src_path = sys.argv[1] if len(sys.argv) > 1 else "final_dataset.xlsx"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    df = load_source(src_path, n)
    print(f"Selected {len(df)} English sentences for translation.")

    df["hindi_generated"] = translate_batch(df["english"].tolist())

    bleu, chrf, ter = compute_scores(df["hindi_generated"].tolist(), df["hindi_reference"].tolist())

    with open("scores.txt", "w", encoding="utf-8") as f:
        f.write("Translation Evaluation Scores\n")
        f.write("==============================\n")
        f.write(f"Model: Helsinki-NLP/opus-mt-en-hi\n")
        f.write(f"Number of sentences: {len(df)}\n\n")
        f.write(f"BLEU:  {bleu.score:.4f}\n")
        f.write(f"CHRF:  {chrf.score:.4f}\n")
        f.write(f"TER:   {ter.score:.4f}\n")
    print("Saved scores.txt")
    print(f"BLEU: {bleu.score:.2f}  CHRF: {chrf.score:.2f}  TER: {ter.score:.2f}")

    output = df.rename(columns={
        "english": "Original English Sentence",
        "hindi_generated": "Model-Generated Hindi Translation",
    })[["Original English Sentence", "Model-Generated Hindi Translation"]]
    output.to_excel("translation_output.xlsx", index=False, engine="openpyxl")
    print("Saved translation_output.xlsx")


if __name__ == "__main__":
    main()
