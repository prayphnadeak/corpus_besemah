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

## Contributors

- **Project Leader**: Pray Putra Hasianro Nadeak, S.ST. (BPS-Statistics of Pagar Alam Municipality)
- **Co-Project Leader** : M. Rifky Naratama, S.Tr.Stat (BPS-Statistics of Pagar Alam Municipality)
- **Data Engineer 1**: Rahmat Hidayat (Undergraduate Student of UNSRI-Sriwijaya Uninversity)
- **Data Engineer 2**: Deka (Undergraduate Student of UNSRI-Sriwijaya Uninversity)

## Format

The `.jsonl` files follow the Alpaca instruction format:

```json
{
    "instruction": "...",
    "input": "...",
    "output": "..."
}
```

