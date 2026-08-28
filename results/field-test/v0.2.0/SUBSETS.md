# v0.2.0 Subsets

Canonical pair roles:

- **Primary / positive pair:** `pair3_gpt_mistral`
- **Validation pair:** `pair5_deepseek_mistral`
- **Negative control:** `pair1_gpt_gemini`
- **Homogeneous control:** `homogeneous_gpt`

Subset files:

- `validation_subset.csv`
  - purpose: run the validation pair `pair5_deepseek_mistral`
  - models: `deepseek/deepseek-chat` and `mistralai/mistral-small-3.2-24b-instruct`

- `negative_control_subset.csv`
  - purpose: run the negative control `pair1_gpt_gemini`
  - models: `openai/gpt-4o-mini` and `google/gemini-2.5-flash`

The full corpus lives in `corpus.csv` and is used for the primary / positive pair.
