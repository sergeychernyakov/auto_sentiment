# Sentiment Analysis on Car Dealership Comments

This project analyzes customer comments about car dealership experiences and provides sentiment scores for various activities related to the car buying process.

## Project Structure

```
project/
│
├── .env
├── inputs/
│   ├── input_1.xlsx
│   ├── input_2.xlsx
│
├── outputs/
│
├── venv/
│
├── requirements.txt
└── analyze_comments.py
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sergeychernyakov/auto_sentiment.git
cd yourproject
```

### 2. Create and Activate a Virtual Environment

- On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

- On macOS and Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project directory with the following content:

```
OPENAI_API_KEY=your-openai-api-key
```

### 5. Place Input Files

Place your input Excel files (e.g., `input_1.xlsx`, `input_2.xlsx`) in the `inputs` directory.

## Running the Script

### 1. Run the Script

```bash
python analyze_comments.py
```

### 2. View Output

The processed comments and sentiment scores will be saved in the `outputs` directory as CSV files.

## Dependencies

- pandas
- openai
- nltk
- python-dotenv

These dependencies are listed in the `requirements.txt` file and can be installed using `pip`.

## Logging

The script logs detailed information about the process, which is helpful for debugging and monitoring.

## Configuration

- `line_limit`: Number of lines to process from each Excel file (default is 3).
- `temperature`: Sampling temperature for the OpenAI API (default is 0.7).
- `max_tokens`: Maximum number of tokens for the OpenAI API response (default is 150).

These parameters can be adjusted by modifying the `SentimentAnalysis` class instantiation in `analyze_comments.py`.

## Example Output

An example output file will contain the original comments along with the sentiment scores for each activity.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```

### How to Run the Script

1. **Activate the Virtual Environment**:

   - On Windows:

   ```bash
   venv\Scripts\activate
   ```

   - On macOS and Linux:

   ```bash
   source venv/bin/activate
   ```

2. **Ensure the Input Files are in the Correct Folder**:

   Place your input Excel files in the `inputs` folder.

3. **Run the Script**:

   ```bash
   python analyze_comments.py
   ```
