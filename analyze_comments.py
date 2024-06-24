import os
import re
import json
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from openai import OpenAI
from dotenv import load_dotenv
import nltk
import logging

class SentimentAnalysis:
    def __init__(self, line_limit=3, temperature=0.2, max_tokens=150):
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.line_limit = line_limit
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Ensure necessary NLTK data is downloaded
        nltk.download('punkt')
        nltk.download('stopwords')

        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Define keywords for activities
        self.activities_keywords = {
            'Search on the brand’s website': ['website', 'online', 'internet'],
            'First visit to the dealership': ['visit', 'dealership', 'first time'],
            'Model comparison at the dealership': ['comparison', 'compare', 'models'],
            'The test drive': ['test drive', 'driving'],
            'Valuation of your used one in exchange': ['valuation', 'trade-in', 'exchange'],
            'Negotiating the value of the new car': ['negotiating', 'negotiation', 'price'],
            'Financing at the dealership': ['financing', 'finance', 'loan'],
            'Signing the purchase contract': ['contract', 'signing', 'agreement'],
            'Car delivery': ['delivery', 'delivered'],
            'First maintenance at the dealership': ['maintenance', 'service', 'first maintenance']
        }

    def preprocess_text(self, text):
        text = text.lower()  # Convert to lowercase
        text = re.sub(r'\W', ' ', text)  # Remove punctuation and special characters
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        tokens = word_tokenize(text)  # Tokenize the text
        tokens = [word for word in tokens if word not in stopwords.words('english')]  # Remove stopwords
        return ' '.join(tokens)

    def analyze_comment(self, comment):
        prompt = f"Analyze the following comment and provide a sentiment score from 0 to 10 for each activity: {comment}\n"
        prompt += "Activities: Search on the brand’s website, First visit to the dealership, Model comparison at the dealership, The test drive, Valuation of your used one in exchange, Negotiating the value of the new car, Financing at the dealership, Signing the purchase contract, Car delivery, First maintenance at the dealership.\n"
        prompt += "Provide the score for each activity in a JSON format."
        
        logging.info(f"Sending prompt to OpenAI API: {prompt}")
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        logging.info(f"Received response from OpenAI API: {response}")
        return response.choices[0].message.content.strip()

    def extract_json(self, text):
        # Use regular expressions to extract JSON part from the response
        json_str = re.search(r'\{.*\}', text, re.DOTALL)
        if json_str:
            return json_str.group(0)
        return None

    def parse_analysis(self, analysis):
        json_text = self.extract_json(analysis)
        if json_text:
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                logging.error(f"JSONDecodeError for analysis: {json_text}")
        else:
            logging.error(f"No JSON found in analysis: {analysis}")
        return {activity: "N/A" for activity in self.activities_keywords}

    def process_file(self, file_path, output_path):
        logging.info(f"Processing file: {file_path}")
        # Load the dataset with a limit on the number of lines
        data = pd.read_excel(file_path, nrows=self.line_limit)
        
        # Inspect column names
        logging.info(f"Column names: {data.columns.tolist()}")

        # Use the correct column name for comments
        comment_col = 'Comments'  # Updated to match the actual column name in the dataset

        # Preprocess comments
        data['cleaned_comment'] = data[comment_col].apply(self.preprocess_text)

        # Analyze comments using ChatGPT
        data['analysis'] = data['cleaned_comment'].apply(self.analyze_comment)

        # Parse the analysis to extract scores
        data['scores'] = data['analysis'].apply(self.parse_analysis)

        # Convert scores to DataFrame and concatenate with original comments
        output_data = pd.concat([data[comment_col], data['scores'].apply(pd.Series)], axis=1)

        # Save the output to a CSV file
        output_data.to_csv(output_path, index=False)
        logging.info(f"Processing complete. The results are saved in '{output_path}'.")

if __name__ == '__main__':
    # Set up the directories
    input_folder = 'inputs'
    output_folder = 'outputs'
    os.makedirs(output_folder, exist_ok=True)

    # Initialize the SentimentAnalysis class with a line limit (default is 3)
    line_limit = 3
    sentiment_analysis = SentimentAnalysis(line_limit)

    # Get all .xlsx files in the input folder
    files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]

    # Process each file
    for file in files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f'output_{file.split(".")[0]}.csv')
        sentiment_analysis.process_file(input_path, output_path)
