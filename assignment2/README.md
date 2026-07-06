# NLP_task — English–Hindi Dataset Processing & LLM Translation

Two-part NLP assessment:
- **Assignment 1**: clean and filter the [`ainlpml/english-hindi`](https://huggingface.co/datasets/ainlpml/english-hindi) parallel corpus by word count.
- **Assignment 2**: translate 100 sentences from that cleaned dataset using an LLM, and score the translations with BLEU, CHRF, and TER.

## Repository contents

| File | Assignment | Purpose |
|---|---|---|
| `full_pipeline.py` | 1 | Downloads the HF dataset, filters by word count (5–50 words) and word-count difference (±10), exports `final_dataset.xlsx`. |
| `assignment2_translation.py` | 2 | Samples 100 sentences from `final_dataset.xlsx`, translates English→Hindi with an LLM, scores against reference Hindi with BLEU/CHRF/TER, exports `translation_output.xlsx` and `scores.txt`. |
| `requirements.txt` | both | All Python dependencies for both scripts. |
| `final_dataset.xlsx` | 1 (output) | Cleaned dataset: English Sentences, Hindi Sentences, Word Count (English), Word Count (Hindi), Difference. |
| `translation_output.xlsx` | 2 (output) | 100 sentence pairs: Original English Sentence, Model-Generated Hindi Translation. |
| `scores.txt` | 2 (output) | BLEU, CHRF, TER scores for the translation run. |

## Setup

```bash
pip install -r requirements.txt
```

You'll need:
- A Hugging Face account with **approved access** to the gated `ainlpml/english-hindi` dataset (request access on the [dataset page](https://huggingface.co/datasets/ainlpml/english-hindi)), plus a personal access token (use a **Read**-type token, not fine-grained, to avoid gated-repo permission issues).
- No API key needed for Assignment 2 — it uses the free, ungated `Helsinki-NLP/opus-mt-en-hi` model from Hugging Face, downloaded automatically on first run (~300MB, cached after).

## Usage

### Assignment 1 — Dataset processing
```bash
python full_pipeline.py
```
Prompts for your Hugging Face token (input hidden, never saved to disk). Produces `final_dataset.xlsx`.

**Results:**

| Stage | Row count |
|---|---|
| Raw dataset loaded | 10,000 |
| After 5–50 word-count filter (both languages) | 8,788 |
| After ±10 word-count difference filter | 8,214 |

**Sample output:**

| English Sentences | Hindi Sentences | Word Count (English) | Word Count (Hindi) | Difference (Eng - Hindi) |
|---|---|---|---|---|
| Mithali To Anchor Indian Team Against Australia in ODIs | आस्ट्रेलिया के खिलाफ वनडे टीम की कमान मिताली को | 9 | 9 | 0 |
| Jharkhand chief minister Hemant Soren | झारखंड के मुख्यमंत्री हेमंत सोरेन (फोटोः पीटीआई) | 5 | 7 | -2 |
| Senior leaders of all major parties held electioneering in favour of their candidates. | सभी मुख्य पार्टियों के वरिष्ठ नेताओं ने अपने-अपने उम्मीदवारों के पक्ष में चुनाव प्रचार किया। | 13 | 15 | -2 |

### Assignment 2 — LLM translation + scoring
```bash
python assignment2_translation.py
# or specify a different source file / sample size:
python assignment2_translation.py final_dataset.xlsx 100
```
Requires `final_dataset.xlsx` (from Assignment 1) to be present in the same folder. Produces `translation_output.xlsx` and `scores.txt`.

## Notes

- The dataset in Assignment 1 is **gated**; access must be requested and approved before the script will run.
- Never commit your Hugging Face token, `.env` files, or any API keys to this repository.
- Word counts use whitespace tokenization (`\S+` regex) for both English and Hindi (Devanagari) text.
- Translation quality depends on the chosen model; `Helsinki-NLP/opus-mt-en-hi` is used here as a free, no-signup baseline. Swap in a different model name in `assignment2_translation.py` (e.g. an OpenAI or IndicTrans2 model) if you want to compare quality.
