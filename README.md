Simple Super Bowl Bingo generator
=================================

When watching the game just isn't enough! Super Bowl Bingo is actually a really fun way to get everyone involved in the game, even if they don't know much about football.

<img src="helpers/Super Bowl 59 Example Board.png" alt="Super Bowl 59 Example Board" width="400"/><br>

# How to Play
Simply download the appropriate pdf file and print out as many pages as you need. Each player should get their own unique bingo card.

The board is a 7x7 and there are three categories of events:
1. Commerical Brands
  a. Mtn Dew, Doritos, Jeep, etc
3. Celebrity appearance (either at game or in commercial)
  a. Taylor Swift, Matt Damon, Paul Rudd
5. Actual things that happen in the game
  a. Missed Field Goal, Interception, pass interference, etc

The "FREE SPACE" in the center of the board is the halftime show, which is guaranteed to happen but won't trigger until halfway through the game.

The board is setup such that to get 7 in a row in any direction, a bingo will consist of 2 commericals brands, 2 celebrity appearances, and 3 football related events.

This specific format can be edited, as well as all the different bingo squares, see "Making your own game" below for more information, although the size of the board is untested beyond 7x7.

# Making Your Own Cards
To create your own bingo game you will need to have Python installed on your computer along with the Pillow library. You can install Pillow using pip:

```
pip install pillow
```

## Customizing the Cards
To customize square names or layout, you can edit the files inside of the "squares" folder.
### Template.csv
This file contains the template for the bingo board layout. Each cell corresponds to a square on the bingo board. You can modify the layout by changing the values in this file.

This repository is set up to generate a 7x7 bingo board with or without a Free Space in the center. You can adjust the size of the board by changing the number of rows and columns in this file, but this is untested and will likely require changes to the code itself.

The values inside of template.csv correspond to the following categories:
- c: Commerical Brand
- h: Celebrity Appearance (Hollywood)
- f: Football Related Event
- e: Free Space (Halftime Show)

**Constraints:**
- I only provide a template for 7x7 boards, so if you change the size you'll need to create your own template.
- Free space only works for the center of the board unless you provide your own custom template.
  - Free space shows up as a blank space because the template has a logo in the center square.

### Other .txt files
Simply add your own events or people to the corresponding text files. Each line in the text file represents a different square that can be randomly selected for the bingo board. Be careful to not make them too big, as they may not fit on the board properly.

### Template Image
I created the template using Google Drawings and exported it as a PNG. You can copy mine here: https://docs.google.com/drawings/d/1oijXkY2x03rTtMsZzRx8FljCl141CdhuPSBY3VRjIbs/edit?usp=sharing

## Running the Code
```
usage: bingo_generator.py [-h] [-n NUM] [-t TEMPLATE] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -n NUM, --num NUM     Number of boards to generate (default: 1)
  -t TEMPLATE, --template TEMPLATE
                        Path to the PNG template (default: helpers/Bingo_Template.png)
  -o OUTPUT, --output OUTPUT
                        Name of the output PDF file (default: SuperBowl_Bingo_Cards.pdf)
```

 
Running `python bingo_generator.py -n 10` will generate a PDF containing 10 unique bingo cards.

# TODO:
This was a great first run, for next year though there's some obvious issues and knowing myself, I won't fix until next Feburary.
1. (Yearly) Update each of the bingo items to be game specific (Done by searching the web for expected commercials and celebrities)
2. Ensure no duplicate boards are created
3. Test with different board sizes
4. Server approach so people can create their own boards without needing to run python code
5. Updating commercials to be logos would be really cool

# History
I wrote this the morning of the Super Bowl 59 (Feb 2025)to create a fun bingo game so that the non-sports family members could still participate and have something fun to do. The game ended up being really fun and no one got a bingo until the 4th quarter, in which within 5 minutes of gametime 2 more people also got a bingo! About 10 people in total played.

I learned a lot from the first year and have since improved the code, formatting, and playability. The first year had some tiles that were too specific to the game, so I eased up on that for this current version.
