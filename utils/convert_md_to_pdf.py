import weasyprint
import markdown
import os

def convert_markdown_to_pdf(md_file_path, pdf_file_path):
    """
    Convert a markdown file to PDF using WeasyPrint.
    This function reads the markdown file, converts it to HTML,
    and then converts the HTML to PDF.
    """
    # Read the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML using the markdown library
    html_body = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
    
    # Wrap the HTML body in a complete HTML document
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SODL Language Specification</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            background-color: white;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #333;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 16px;
            margin-left: 0;
            color: #666;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""

    # Convert HTML to PDF
    html_doc = weasyprint.HTML(string=html_content)
    html_doc.write_pdf(pdf_file_path)
    
    print(f"Successfully converted {md_file_path} to {pdf_file_path}")

# Define file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
md_file_path = os.path.join(current_dir, ".sodl", "SODL_DOCUMENTATION.md")
pdf_file_path = os.path.join(current_dir, ".sodl", "SODL Language Specification_v0.3.pdf")

# Convert the markdown file to PDF
convert_markdown_to_pdf(md_file_path, pdf_file_path)