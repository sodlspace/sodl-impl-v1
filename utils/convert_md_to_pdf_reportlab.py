import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import markdown

def convert_markdown_to_pdf_reportlab(md_file_path, pdf_file_path):
    """
    Convert a markdown file to PDF using ReportLab.
    This function reads the markdown file and converts it to a PDF document.
    """
    # Read the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Parse markdown content into elements
    # For simplicity, we'll split by lines and handle basic formatting
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    story = []
    
    # Get basic styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        spaceAfter=12,
        borderWidth=0,
        borderPadding=0,
        leading=16
    )
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        spaceAfter=10,
        borderWidth=0,
        borderPadding=0,
        leading=14
    )
    heading3_style = ParagraphStyle(
        'Heading3',
        parent=styles['Heading3'],
        spaceAfter=8,
        borderWidth=0,
        borderPadding=0,
        leading=12
    )
    normal_style = styles['Normal']
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=10,
        leftIndent=20,
        spaceBefore=6,
        spaceAfter=6
    )
    
    # Split content into lines for processing
    lines = markdown_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('# '):
            # Heading 1
            story.append(Paragraph(line[2:], heading1_style))
            story.append(Spacer(1, 0.2 * inch))
        elif line.startswith('## '):
            # Heading 2
            story.append(Paragraph(line[3:], heading2_style))
            story.append(Spacer(1, 0.15 * inch))
        elif line.startswith('### '):
            # Heading 3
            story.append(Paragraph(line[4:], heading3_style))
            story.append(Spacer(1, 0.1 * inch))
        elif line.startswith('```'):
            # Code block
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].startswith('```'):
                if i < len(lines):
                    code_lines.append(lines[i])
                i += 1
            code_block = '\n'.join(code_lines)
            story.append(Preformatted(code_block, code_style))
            story.append(Spacer(1, 0.1 * inch))
        elif line.startswith('- ') or line.startswith('* '):
            # List item
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 0.05 * inch))
        elif line != '':
            # Regular paragraph
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 0.1 * inch))
        else:
            # Empty line - add more space
            story.append(Spacer(1, 0.1 * inch))
        
        i += 1
    
    # Build the PDF
    doc.build(story)
    print(f"Successfully converted {md_file_path} to {pdf_file_path}")

# Define file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
md_file_path = os.path.join(current_dir, ".sodl", "SODL_DOCUMENTATION.md")
pdf_file_path = os.path.join(current_dir, ".sodl", "SODL Language Specification_v0.3.pdf")

# Convert the markdown file to PDF
convert_markdown_to_pdf_reportlab(md_file_path, pdf_file_path)