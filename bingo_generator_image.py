import csv
import random
import os
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas  # Import reportlab here
from reportlab.lib.pagesizes import letter, landscape

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

draw = None  # Declare draw globally
font = None #Declare font globally

def wrap_text(text, width, font):
    """Wraps text to fit within a specified width."""
    words = text.split()
    lines = []
    current_line = ""
    dummy_img = Image.new('RGB', (1, 1))  # Dummy image
    draw = ImageDraw.Draw(dummy_img)  # Create a dummy draw object
    
    for word in words:
        text_width = draw.textlength(current_line + word, font=font)
        if text_width < width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    lines.append(current_line.strip())
    return "\n".join(lines)


def csv_to_image(csv_file, image_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    cell_width = 150
    cell_height = 50
    font_size = 12
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Or full path
    except OSError:
        print("Arial font not found. Using a default font.")
        font = ImageFont.load_default()

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

            draw.rectangle([(x1, y1), (x2, y2)], outline='black')

            wrapped_text = wrap_text(cell, cell_width - 10, font)
            lines = wrapped_text.split('\n')

            # Calculate text height correctly
            text_height = font.getbbox("A")[3] - font.getbbox("A")[1]  
            y_offset = (cell_height - len(lines) * text_height) / 2  # Vertical centering

            for i, line in enumerate(lines):
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = x1 + (cell_width - text_width) / 2  # Center horizontally
                text_y = y1 + y_offset + i * text_height  # Place each line correctly
                draw.text((text_x, text_y), line, fill='black', font=font)

    img.save(image_file)


def display_bingo_boards(folder, output_pdf="bingo_boards.pdf"):
    files = [f for f in os.listdir(folder) if f.endswith('.csv')]  
    pdf_file = os.path.join(folder, output_pdf)  

    # Create a single PDF in landscape mode
    c = canvas.Canvas(pdf_file, pagesize=landscape(letter))  
    page_width, page_height = landscape(letter)  # Get landscape dimensions

    for file in files:
        csv_file = os.path.join(folder, file)
        image_file = os.path.join(folder, file.replace(".csv", ".png"))

        csv_to_image(csv_file, image_file)  # Generate the image from CSV

        # Read CSV to determine image size
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)  

        cell_width = 150  
        cell_height = 50  

        num_cols = len(data[0])
        num_rows = len(data)
        image_width = num_cols * cell_width
        image_height = num_rows * cell_height

        # Scale the board to fit within the page while maintaining aspect ratio
        max_width = page_width - 50  # 25pt margin on each side
        max_height = page_height - 50  # 25pt margin on top/bottom

        scale_factor = min(max_width / image_width, max_height / image_height)

        scaled_width = image_width * scale_factor
        scaled_height = image_height * scale_factor

        x_offset = (page_width - scaled_width) / 2
        y_offset = (page_height - scaled_height) / 2

        c.drawImage(image_file, x_offset, y_offset, scaled_width, scaled_height)
        c.showPage()  # Add a new page for the next board

        print(f"Added {file} to {output_pdf}")

    c.save()  # Save the final PDF
    print(f"Generated {pdf_file}")

# Example usage (no changes needed here)
generate_bingo_boards('template.csv', 'commercial_brands.txt', 'hollywood_celebs.txt', 'football_related_activities.txt', 12)
display_bingo_boards('bingo_csv')
