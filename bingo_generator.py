import csv
import random
import os
import argparse
from PIL import Image, ImageDraw, ImageFont

def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def generate_bingo_boards(template, company_words, hollywood_words, football_words, n):
        
    game_boards = []

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
                if cell == 'c': # Commercials
                    new_row.append(next(company_iter, ''))
                elif cell == 'h': # Hollywood celebrities
                    new_row.append(next(hollywood_iter, ''))
                elif cell == 'f': # Football related activities
                    new_row.append(next(football_iter, ''))
                elif cell == 'e': # Empty cell that will correspond to free on the template
                    new_row.append(' ') 
                else:
                    new_row.append(cell)
            board.append(new_row)

        game_boards.append(board)
    return game_boards

def get_dynamic_font(draw, text, max_width, max_height, font_path, initial_size):
    """Shrinks font and forces breaks based on pixel width, not character count."""
    current_size = initial_size
    padding = 20 # Space inside the cell
    
    while current_size > 10:
        font = ImageFont.truetype(font_path, current_size)
        
        # --- SMART WRAP LOGIC ---
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Check if adding this word exceeds pixel width
            test_line = " ".join(current_line + [word])
            # getlength() is the most accurate way to measure a single line
            if draw.textlength(test_line, font=font) <= (max_width - padding):
                current_line.append(word)
            else:
                # If we have words in the current line, finish it
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    # If a single word is wider than the box, we force it anyway
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(" ".join(current_line))
            
        wrapped_text = "\n".join(lines)
        
        # --- SIZE CHECK ---
        # Get the bounding box of the multi-line block
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        if w <= (max_width - padding) and h <= (max_height - padding):
            return font, wrapped_text
            
        current_size -= 1 # Shrink incrementally for better fit
        
    return ImageFont.truetype(font_path, 10), text

def process_csv_to_template(game_boards, template_path, output_path):
    generated_images = []
    FONT_PATH = "helpers/arialbd.ttf" 

    for board in game_boards:
        img = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        
        DPI = img.width / 8 
        GRID_TOP = 1.75 * DPI
        CELL_SIZE = (8.0 * DPI) / 7

        if DPI < 200:
            print("Warning: DPI is low, text rendering may be poor.")

        for r in range(7):
            for c in range(7):
                text = str(board[r][c])
                
                # 1. Get center of the cell
                center_x = (c * CELL_SIZE) + (CELL_SIZE / 2)
                center_y = GRID_TOP + (r * CELL_SIZE) + (CELL_SIZE / 2)
                
                # 2. Get dynamic font and wrapped text
                # We pass CELL_SIZE as the constraints
                font, wrapped_text = get_dynamic_font(
                    draw, text, CELL_SIZE, CELL_SIZE, FONT_PATH, int(DPI * 0.25)
                )
                
                # 3. Draw with centering
                # anchor="mm" centers the block on the point
                # align="center" centers the lines relative to each other
                draw.multiline_text(
                    (center_x, center_y), 
                    wrapped_text, 
                    fill=(0,0,0), 
                    font=font, 
                    anchor="mm", 
                    align="center", 
                    spacing=4
                )
        generated_images.append(img.convert("RGB"))
        img.save(f"bingo_board.png") # Used for making banner image only
    
    # Save all images to one PDF
    if generated_images:
        generated_images[0].save(
            output_path, 
            save_all=True, 
            append_images=generated_images[1:],
            resolution=300.0,
            quality=95
        )
        print(f"Created {len(generated_images)} pages in {output_path}")

def main():
    # 1. Setup the Argument Parser
    parser = argparse.ArgumentParser(description="Generate Super Bowl Bingo Cards.")
    
    # 2. Define the Parameters
    parser.add_argument(
        "-n", "--num", 
        type=int, 
        default=1, 
        help="Number of boards to generate (default: 1)"
    )
    parser.add_argument(
        "-t", "--template", 
        type=str, 
        default="helpers/Bingo_Template.png", 
        help="Path to the PNG template (default: helpers/Bingo_Template.png)"
    )
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default="SuperBowl_Bingo_Cards.pdf", 
        help="Name of the output PDF file (default: SuperBowl_Bingo_Cards.pdf)"
    )

    args = parser.parse_args()

    # 3. Validation
    if not os.path.exists(args.template):
        print(f"❌ Error: Could not find template at {args.template}")
        return

    # Load template
    with open('squares/template.csv', 'r') as file:
        reader = csv.reader(file)
        template = [row for row in reader]

    print(f"🚀 Starting generation for {args.num} boards...")
    print(f"📍 Using template: {args.template}")

    game_boards = generate_bingo_boards(template, load_words('squares/commercial_brands.txt'), load_words('squares/hollywood_celebs.txt'), load_words('squares/football_related_activities.txt'), args.num)
    process_csv_to_template(game_boards, args.template, args.output)


if __name__ == "__main__":
    main()