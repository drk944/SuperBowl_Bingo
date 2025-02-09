import csv
import random
import os
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas  # Import reportlab here

def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def generate_bingo_boards(template_file, company_file, hollywood_file, football_file, n):
    # Load template
    with open(template_file, 'r') as file:
        reader = csv.reader(file)
        template = [row for row in reader]
    
    # Load category words
    company_words = load_words(company_file)
    hollywood_words = load_words(hollywood_file)
    football_words = load_words(football_file)
    
    os.makedirs('bingo_csv', exist_ok=True)
    
    for i in range(n):
        # Shuffle words for each new board
        random.shuffle(company_words)
        random.shuffle(hollywood_words)
        random.shuffle(football_words)
        
        # Create iterators for each category
        company_iter = iter(company_words)
        hollywood_iter = iter(hollywood_words)
        football_iter = iter(football_words)
        
        # Generate board based on template
        board = []
        for row in template:
            new_row = []
            for cell in row:
                if cell == 'c':
                    new_row.append(next(company_iter, ''))
                elif cell == 'h':
                    new_row.append(next(hollywood_iter, ''))
                elif cell == 'f':
                    new_row.append(next(football_iter, ''))
                else:
                    new_row.append(cell)
            board.append(new_row)
        
        # Write board to CSV
        output_filename = os.path.join('bingo_csv', f'bingo_board_{i+1}.csv')
        with open(output_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(board)
        print(f'Generated {output_filename}')


def wrap_text(text, width, pdf):  # Add pdf as an argument
    """Wraps text to fit within a specified width."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if pdf.get_string_width(current_line + word) < width:  # Use the passed pdf
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return "\n".join(lines)

def csv_to_image(csv_file, image_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)  # Read all data

    cell_width = 150  # Adjust as needed
    cell_height = 50  # Adjust as needed
    font_size = 12
    # font = ImageFont.truetype("arial.ttf", font_size)
    
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Example path - REPLACE THIS!
    font = ImageFont.truetype(font_path, font_size)
    
    num_cols = len(data[0])
    num_rows = len(data)
    image_width = num_cols * cell_width
    image_height = num_rows * cell_height

    img = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(img)

    for row_index, row in enumerate(data):
        for col_index, cell in enumerate(row):
            x1 = col_index * cell_width
            y1 = row_index * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            draw.rectangle([(x1, y1), (x2, y2)], outline='black')  # Cell borders

            # Center the text (more or less)
            text_width, text_height = draw.textsize(cell, font=font)
            text_x = x1 + (cell_width - text_width) / 2
            text_y = y1 + (cell_height - text_height) / 2
            draw.text((text_x, text_y), cell, fill='black', font=font)

    img.save(image_file)


def display_bingo_boards(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.csv')]  # <--- Define files here
    for file in files:
        csv_file = os.path.join(folder, file)
        image_file = os.path.join(folder, file.replace(".csv", ".png"))
        pdf_file = os.path.join(folder, file.replace(".csv", ".pdf"))

        csv_to_image(csv_file, image_file)

        # Use reportlab for PDF conversion (more reliable and cross-platform)
        with open(csv_file, 'r') as f: #Needed to get image width and height
            reader = csv.reader(f)
            data = list(reader)  # Read all data

        cell_width = 150  # Adjust as needed
        cell_height = 50  # Adjust as needed

        num_cols = len(data[0])
        num_rows = len(data)
        image_width = num_cols * cell_width
        image_height = num_rows * cell_height

        c = canvas.Canvas(pdf_file)
        c.drawImage(image_file, 0, 0, image_width, image_height)
        c.save()

        print(f"Generated {pdf_file}")

# Example usage (no changes needed here)
generate_bingo_boards('template.csv', 'commercial_brands.txt', 'hollywood_celebs.txt', 'football_related_activities.txt', 5)
display_bingo_boards('bingo_csv')
