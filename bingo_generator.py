import csv
import random
import os
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

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

def display_bingo_boards(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for file in files:
        pdf.add_page()
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(200, 10, file.replace(".csv", ""), ln=True, align='C')
        pdf.ln(5)

        with open(os.path.join(folder, file), 'r') as f:
            reader = csv.reader(f)
            board = [row for row in reader]

        num_cols = len(board[0])
        cell_width = 190 / num_cols
        cell_height = 20  # Adjusted cell height

        for row in board:
            pdf.set_x(10)  # Reset x position for new row
            max_cell_height = 0  # To store max height of cells in the row

            for cell in row[:num_cols]:
                wrapped_text = wrap_text(cell, cell_width - 6, pdf)  # Smaller width for padding
                
                # Calculate required cell height based on content
                lines = wrapped_text.split('\n')
                required_height = len(lines) * 8 # Adjust 8 to fine tune line spacing. Lower number = less spacing
                
                # Store the max height of cells in the row
                max_cell_height = max(max_cell_height, required_height)

            pdf.set_font("Arial", size=9)
            pdf.set_y(pdf.get_y() + (max_cell_height - cell_height)/2)

            for cell in row[:num_cols]:
                wrapped_text = wrap_text(cell, cell_width - 6, pdf)  # Smaller width for padding
                pdf.multi_cell(cell_width, 8, wrapped_text, border=1, align='C') # 8 is line height
                pdf.set_x(pdf.get_x() + cell_width)

            pdf.ln(max_cell_height - 8) # Move down to start next row
    pdf.output(os.path.join(folder, "bingo_boards.pdf"))  # <--- This line was missing!
    print(f'Saved bingo boards as {os.path.join(folder, "bingo_boards.pdf")}')


# Example usage
generate_bingo_boards('template.csv', 'commercial_brands.txt', 'hollywood_celebs.txt', 'football_related_activities.txt', 5)
display_bingo_boards('bingo_csv')
