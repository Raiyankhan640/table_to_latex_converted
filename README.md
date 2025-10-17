# Table to LaTeX Converter

A Python tool that converts images of tables into compilable LaTeX code using Google's Gemini Pro API and LangChain.

## Features

- Converts table images to complete, standalone LaTeX documents
- Preserves table structure, borders, and formatting
- Automatically handles column widths using `tabularx`
- Generates directly compilable `.tex` files

## Prerequisites

- Python 3.8+
- Google Cloud API key for Gemini Pro
- LaTeX distribution (for compiling output files)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Table-to-Latex-using-Langchain
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

Run the script with an image file as input:
```bash
python convert_table.py path/to/your/table_image.jpg
```

The script will:
1. Process the input image
2. Generate LaTeX code using Gemini Pro
3. Save the output as a `.tex` file named after your input image

## Technologies Used

- Python 3.x
- LangChain
- Google Gemini Pro API
- PIL (Python Imaging Library)
- LaTeX with tabularx

## Project Structure

```
Table-to-Latex-using-Langchain/
├── convert_table.py      # Main conversion script
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (not in repo)
└── README.md           # Project documentation
```

## License

N/A

## Author

Khan Raiyan Ibne Reza
