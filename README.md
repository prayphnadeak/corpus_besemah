# Besemah Language Corpus

This dataset is curated for training and tuning AI models on the Besemah language (South Sumatra, Indonesia).

## Structure

- **besemah_dictionary.json**: The raw dictionary data cleaned of comments.
- **train.jsonl**: Instruction tuning dataset (90% split).
- **validation.jsonl**: Instruction tuning dataset (10% split).

## Statistics

- **Total Entries**: 6876
- **Total Instruction Pairs**: 31424
- **Training Examples**: 28281
- **Validation Examples**: 3143

## Format

The `.jsonl` files follow the Alpaca instruction format:

```json
{
    "instruction": "...",
    "input": "...",
    "output": "..."
}
```
