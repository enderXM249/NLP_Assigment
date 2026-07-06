Assessment 1: English–Hindi Dataset Processing and Analysis
Task Instructions
Clone the Dataset
Clone the provided Hugging Face dataset repository into your local system using the terminal.
Load the Data into Google Sheets
Extract the dataset into two columns:
Column A: English sentences
Column B: Hindi sentences
Ensure that the dataset contains at least 10,000 rows (lines).
Word Count Analysis
For each sentence in both English and Hindi, compute the word counts.
Keep only those words count whose sentences fall within the range of 5 to 50 in both languages.
Word Count Difference Calculation
For each word pair (English–Hindi), calculate the difference in word count between English and Hindi.
Retain only those word pairs where the word count difference lies within the range of -10 to +10.
Final Output
Prepare a cleaned dataset with the above conditions applied.
Submit the results in Excel format, with clear columns for:
English Sentences
Hindi Sentences
Word Count (English)
Word Count (Hindi)
Difference between Word Count (English) and Word Count (Hindi)

Assessment No. 2 – Translation with LLM
Task Instructions
Select Sentences
From the dataset prepared in Assignment No. 1, take 100 English sentences.
Run Inference with an LLM
Use a Large Language Model (LLM) of your choice (e.g., Hugging Face model, OpenAI API, or any other translation model).
Input the selected English sentences into the model.
Translate into Hindi
Generate the corresponding Hindi translations using the LLM.
Calculate BLEU, CHRF, TER Score on the translated sentences and save it in
.txt file

Submission Format

Prepare your output in Excel format with the following columns:
Column A: Original English sentence
Column B: Model-generated Hindi translation
