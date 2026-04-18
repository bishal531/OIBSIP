# Data Directory

## Contents

This directory stores all data files used in the project.

### Files

- **preprocessed_data.csv**: Cleaned and processed text data
  - Columns: original, cleaned, tokens, token_count
  - Used by autocomplete and autocorrect notebooks

- **vocabulary.txt**: List of unique words/tokens
  - One word per line
  - Generated from preprocessed data
  - Used for training and evaluation

### Data Preparation

Raw text data is processed through:
1. Cleaning (lowercase, remove special characters)
2. Tokenization (word splitting)
3. Normalization (whitespace handling)

### Adding New Data

To add new data sources:
1. Place raw text files in this directory
2. Run the data exploration notebook to process
3. Update vocabulary.txt if new tokens are found
