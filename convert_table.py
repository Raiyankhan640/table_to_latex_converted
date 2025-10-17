import sys
import base64
import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

def image_to_base64(image_path: str) -> str:
    """Converts an image file to a base64 encoded string."""
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)

def create_latex_standalone(image_path: str) -> str:
    """
    Generates a complete, standalone, and compilable LaTeX document for a table image.
    """
    # Use the configured Google generative model.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
    
    b64_image = image_to_base64(image_path)

    # --- PROMPT: describe the expected LaTeX output and include the image ---
    # Note: raw string used so backslashes in LaTeX are preserved and won't cause unicode escape errors.
    prompt_text = r"""
    You are a precision LaTeX document generator. Your mission is to convert the provided table image into a **complete, standalone, and directly compilable `.tex` file**. The final document must perfectly render the entire table, with all columns and borders visible.

    EXECUTION DIRECTIVES (NON-NEGOTIABLE):

    1.  Generate a Full Document: Your output MUST be a complete LaTeX document. It must start with `\documentclass{article}` and end with `\end{document}`.

    2.  Force Page Width: You MUST include the `geometry` package to create ample horizontal space. Use these exact settings in the preamble:
        `\usepackage[a4paper, margin=1cm, hmargin=1cm, vmargin=2cm]{geometry}`

    3.  Required Packages: Your preamble MUST include `\usepackage{tabularx}` and `\usepackage{booktabs}` for high-quality tables.

    4.  Table Environment:
        * Use the `tabularx` environment and set its width to `\linewidth` to fill the new, wider page space.
        * Your column specifier MUST replicate all vertical borders seen in the image (e.g., `{|l|X|c|c|}`).
        * To preserve the table's natural column widths, use the `X` type ONLY for the column(s) with long, wrapping text. Use `l`, `c`, or `r` for all other columns.

    5.  Border Fidelity: You MUST replicate ALL horizontal lines using `\hline`. This includes a `\hline` after the header, after every data row, and at the very end of the table to create a complete box.

    6.  No Extra Content: The document body should contain ONLY the table. Do not add any text before `\begin{tabularx}` or after `\end{tabularx}`.

    7.  Final Output: Your entire response must be the raw code for the `.tex` file and nothing else.

    Analyze the image and generate the complete, self-contained LaTeX file now.
    """

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}},
        ]
    )

    print("🤖 Generating a complete, standalone .tex file...")
    response = llm.invoke([message])
    
    # Extract text and trim whitespace
    cleaned_response = response.content.strip() if hasattr(response, "content") else str(response).strip()

    # Remove common markdown fences if present
    if cleaned_response.startswith("```latex"):
        cleaned_response = cleaned_response[7:]
    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[3:]
    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]

    # Remove any leading stray characters before the LaTeX documentclass.
    # This prevents stray characters like 'x' at the start of the file.
    import re
    m = re.search(r'\\documentclass', cleaned_response)
    if m:
        cleaned_response = cleaned_response[m.start():]
    else:
        # Fallback: remove any leading non-printable/garbage characters and whitespace
        cleaned_response = cleaned_response.lstrip()

    return cleaned_response.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_table.py <path_to_image>")
        sys.exit(1)

    # Get input image path
    image_file_path = sys.argv[1]
    
    # Generate LaTeX code
    latex_code = create_latex_standalone(image_file_path)
    
    # Create output filename based on input image name
    input_name = os.path.splitext(os.path.basename(image_file_path))[0]
    output_filename = f"{input_name}_table.tex"
    
    # Save to .tex file
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(latex_code)
        print(f"\nSuccessfully created: {output_filename}")
    except Exception as e:
        print(f"Error saving .tex file: {e}")
        sys.exit(1)