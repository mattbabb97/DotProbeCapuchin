#                                     (`-.              ('-.     
#                                   _(OO  )_           ( OO ).-. 
# .-'),-----.  ,--.      ,-.-') ,--(_/   ,. \ ,-.-')   / . --. / 
#( OO'  .-.  ' |  |.-')  |  |OO)\   \   /(__/ |  |OO)  | \-.  \  
#/   |  | |  | |  | OO ) |  |  \ \   \ /   /  |  |  \.-'-'  |  | 
#\_) |  |\|  | |  |`-' | |  |(_/  \   '   /,  |  |(_/ \| |_.'  | 
#  \ |  | |  |(|  '---.',|  |_.'   \     /__),|  |_.'  |  .-.  | 
#   `'  '-'  ' |      |(_|  |       \   /   (_|  |     |  | |  | 
#     `-----'  `------'  `--'        `-'      `--'     `--' `--' 
                                                                  
import sys                  # Import the 'system' library
import random               # Import the 'random' library which gives cool functions for randomizing numbers
import math                 # Import the 'math' library for more advanced math operations
import time                 # Import the 'time' library for functions of keeping track of time (ITIs, IBIs etc.)
import datetime
import os                   # Import the operating system (OS)
import glob                 # Import the glob function
import pygame               # Import Pygame to have access to all those cool functions
import Matts_Toolbox        # Import Matt's Toolbox with LRC specific functions

pygame.init()               # This initializes all pygame modules

# READ TECHNICAL FILES ------------------------------------------------------------------------------------------------


# Grab the monkey name from monkey.txt
with open("monkey.txt") as f:
    monkey = f.read()

# Set Current Date
today = time.strftime('%Y-%m-%d')

# ----------------------------------------------------------------------------------------------------------------------
# SET UP LOCAL VARIABLES -----------------------------------------------------------------------------------------------

white = (255, 255, 255)                                         # This sets up colors you might need
black = (0, 0, 0)                                               # Format is (Red, Green, Blue, Alpha)
green = (0, 200, 0)                                             # 0 is the minimum 260 is the maximum
red = (250, 0, 0)                                               # Alpha is the transparency of a color
transparent = (0, 0, 0, 0)

"""Put your sounds here"""
sound_chime = pygame.mixer.Sound("chime.wav")                   # This sets your trial initiation sound
sound_correct = pygame.mixer.Sound("correct.wav")               # This sets your correct pellet dispensing sound
sound_incorrect = pygame.mixer.Sound("incorrect.wav")           # This sets your incorrect sound

"""Put your Screen Parameters here"""
scrSize = (800, 600)                                            # Standard Resolution of Monkey Computers is 800 x 600
scrRect = pygame.Rect((0, 0), scrSize)                          # Sets the shape of the screen to be a rectangle
fps = 60                                                        # Frames Per Second


"""FILE MANIPULATION FUNCTIONS --------------------------------------------------------------------------------------"""

# Create an Output File
from Matts_Toolbox import writeLn

# Name the file of your Data Output
from Matts_Toolbox import makeFileName

# Get parameters from parameters.txt
from Matts_Toolbox import getParams

# Save parameters into their own file for safe keeping
from Matts_Toolbox import saveParams

"""SCREEN MANIPULATION FUNCTIONS ------------------------------------------------------------------------------------"""
from Matts_Toolbox import setScreen

from Matts_Toolbox import refresh

        # Argument to pass: Surface

"""HELPER FUNCTIONS -------------------------------------------------------------------------------------------------"""
# Quit Program Function
from Matts_Toolbox import quitEscQ

# Sound Playing Function
from Matts_Toolbox import sound

# Pellet Dispensing Function
from Matts_Toolbox import pellet

# Moving the Cursor
from Matts_Toolbox import joyCount
from Matts_Toolbox import moveCursor

from Matts_Toolbox import pseudorandomize
from Matts_Toolbox import shuffle_array

"""LIST OF TODOS ----------------------------------------------------------------------------------------------------"""
# TODO: run more than 2 blocks (need 40 blocks of 5 trials per block using the 10 available stimuli)
# TODO: remove option that results in "wrong" answer if cursor moves to opposite side of screen from target
# TODO:
# TODO:

"""ICON CLASS -------------------------------------------------------------------------------------------------------"""

from Matts_Toolbox import Box

# Draws the Icons
class Icon(Box):
    def __init__(self, PNG, position, scale):                                  # Pass the image and position (x,y)
        super(Icon, self).__init__()
        image = pygame.image.load(PNG).convert_alpha()                          # image = image you passed in arguments
        self.size = image.get_size()                                            # Get the size of the image
        self.image = pygame.transform.smoothscale(image, scale)                 # Scale the image = scale inputted
        self.rect = self.image.get_rect()                                       # Get rectangle around the image
        self.rect.center = self.position = position                             # Set rectangle and center at position
        self.mask = pygame.mask.from_surface(self.image)                        # Creates a mask object

    def mv2pos(self, position):                                           # Move the Image obj to position (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position = position


"""TRIAL CLASS -----------------------------------------------------------------------------------------------------"""

class Trial(object):
    def __init__(self):
        super(Trial, self).__init__()
        self.session_type = session_type               # Type of Session (1: Regular 2: Extended)
        self.trial_number = 0                          # Trial Number
        self.trial_within_block = -1                   # Trial Within the current block {1-5}
        self.block = 1                                 # Block number
        self.block_length = 5                         # Number of trials per block = 5
        self.blocks_per_session = 25                    # Number of blocks per session = 25
        self.LorR = (0, 0)
        self.startphase = True                          #start button
        self.phase1 = False                             #flash images
        self.phase2 = False                             #select target
        self.trainID = 0
        self.train1_array = [0, 1, 2, 3, 4]
        shuffle_array(self.train1_array)
        self.train2_array = [0, 1, 2, 3, 4]
        shuffle_array(self.train2_array)

        self.stimuli = []                              # Create a blank list for stimuli input
        self.stimuliPosition = []                      # Create a blank list for Left/Right Positions

    def new(self):
        global start_time
        global subselection
        global SELECT
        SELECT = -1
        self.trial_number += 1                                                # Increment trial number by 1
        self.trial_within_block += 1                                          # Increment trial within block by 1
        sound_chime.play()
        print("Trial: " + str(self.trial_number))
        print("Trial_within_block: " + str(self.trial_within_block))
        print("Block: " + str(self.block))

        if self.trial_within_block == self.block_length:                      # If this is the last trial in the block
            self.trial_within_block = 0                                       # Reset this to 0
            self.newBlock()                                                   # Run .newBlock()
            print("Block Complete!")

        self.startphase = True
        self.phase1 = False
        self.phase2 = False

        pseudorandomize(icon_positions)                                 # Randomise the Left/Right Positions
        self.create_stimuli()                                           # Run .create_stimuli()
        cursor.mv2pos((400, 550))                                       # Move the cursor to the start position
        start_time = pygame.time.get_ticks()


    def newBlock(self):
        """Moves program to the next block and randomizes the trial types"""
        global trial_type
        shuffle_array(self.train1_array)
        print(self.train1_array)
        shuffle_array(self.train2_array)
        print(self.train2_array)
        self.trainID = 0
        self.block += 1                                                 # Increment block by 1
        #pseudorandomize(trial_type)                                     # Randomise the trials within a block
        if self.block > blocks_per_session:                             # Check if this is the last block in the session
            print("Session Complete!")                                  # If it is, then quit!
            pygame.quit()
            sys.exit()

    def create_stimuli(self):
        """Create the stimuli based on the trial type"""

        Icons = [Icon("start.png", (150, 500), (140, 140)),                 # Start Button
                Icon("imageA.png", (0, 0), (140, 140)),                        # Target
                Icon(train1[self.train1_array[self.trainID]], (0, 0), (140, 140)),
                Icon(train2[self.train2_array[self.trainID]], (0, 0), (140, 140))]
        self.trainID += 1

        if trial_type[self.trial_within_block] == 1:                        # Threat-Neutral Congruent
            self.stimuli = [Icons[0], Icons[1], Icons[2], Icons[3]]
        elif trial_type[self.trial_within_block] == 2:                      # Threat-Neutral Incongruent
            self.stimuli = [Icons[0], Icons[1], Icons[2], Icons[3]]
        elif trial_type[self.trial_within_block] == 3:                      # Neutral-Neutral
            self.stimuli = [Icons[0], Icons[1], Icons[2], Icons[3]]


    def draw_start(self):
        """Draw the target sample at center of the screen"""
        self.stimuli[0].mv2pos((400, 300))
        self.stimuli[0].draw(screen)

    def draw_target(self):
        """Draw the samples at their positions after target sample is selected"""
        global icon_positions
        n = self.get_trial_type()
        if n == 1: 
            self.stimuli[1].mv2pos(icon_positions[0])
            self.stimuli[1].draw(screen)
        elif n == 2:
            self.stimuli[1].mv2pos(icon_positions[1])
            self.stimuli[1].draw(screen)
        elif n == 3:
            self.stimuli[1].mv2pos(icon_positions[1])
            self.stimuli[1].draw(screen)

    def draw_stimuli(self):
        """Draw the samples at their positions after target sample is selected"""
        global icon_positions
        self.stimuli[2].mv2pos(icon_positions[0])
        self.stimuli[3].mv2pos(icon_positions[1])
        self.stimuli[2].draw(screen)
        self.stimuli[3].draw(screen)

    def get_trial_type(self):
        return trial_type[self.trial_within_block]
        print("Trial Type: " + str(trial_type[self.trial_within_block]))

    def trial_duration(self):
        global duration
        global timer
        global start_time
        global SELECT

        seconds = 0
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() - start_time) / 1000)
        if seconds > duration and SELECT != -1:
            seconds = seconds
        elif seconds > duration and SELECT == -1:
            start_time = pygame.time.get_ticks()
            self.trial_number -= 1
            self.trial_within_block -= 1
            self.trainID -= 1
            seconds = 0
            selection = 0
            self.startphase = True
            self.new()

        return seconds


    def response_time(self):
        seconds = 0
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() - start_time) / 1000)
            print(seconds)

        return seconds

    def flash_stimuli(self):
        #print("Running flash_stimuli")
        self.draw_stimuli()
        pygame.time.delay(1000)
        self.phase1 = False
        self.phase2 = True
        
    
#----------------------------------------------------------------

    def start(self):
        global SELECT
        global timer
        global start_time
        self.draw_start()
        cursor.draw(screen)
        moveCursor(cursor)

        if cursor.collides_with(self.stimuli[0]):
            screen.fill(white)
            self.flash_stimuli()
            start_time = pygame.time.get_ticks()
            self.startphase = False
            self.phase1 = True


    def run_trial(self):
        global SELECT
        global timer
        global start_time
        global trial_type

        if self.get_trial_type() == 1:
            idx = 0
        elif self.get_trial_type() == 2 or 3:
            idx = 1
        
        cursor.draw(screen)
        moveCursor(cursor, only= 'left, right')
        self.stimuli[0].mv2pos((-50, -50))
        self.stimuli[0].size = 0
        self.draw_target()
        self.trial_duration()
        self.response_time()

        if SELECT == 1:
            self.LorR = icon_positions[idx]
            self.write(data_file, self.left_or_right(), self.response_time())
            sound(True)
            pellet()
            screen.fill(white)
            refresh(screen)
            pygame.time.delay(ITI * 1000)
            self.new()

        #elif SELECT == 2:
        #    self.LorR = icon_positions[1]
        #    sound(False)
        #    screen.fill(white)
        #    refresh(screen)
        #    #self.write(data_file, ...)
        #    pygame.time.delay(ITI * 1000)
        #    self.new()
            

    def left_or_right(self):
        if self.LorR == (125, 300):
            return "left"
        elif self.LorR == (675, 300):
            return "right"

    def write(self, file, side, time_taken):
        now = time.strftime('%H:%M:%S')
        # Training
        data = [monkey, today, now, self.session_type, self.block, self.trial_number, "training", side, time_taken,
                self.train1_array[self.trainID - 1], self.train2_array[self.trainID - 1]]
        # Testing
        #data = [monkey, today, now, self.session_type, self.block, self.trial_number, trial_type[self.trial_within_block], side, time_taken]
        writeLn(file, data)




# ---------------------------------------------------------------------------------------------------------------------


# UPLOAD TASK PARAMETERS ----------------------------------------------------------------------------------------------
varNames = ['full_screen', 'session_type', 'trials_per_block', 'blocks_per_session', 'ITI',
            'duration', 'IBI', 'run_time']
params = getParams(varNames)
globals().update(params)

full_screen = params['full_screen']                         # Since your parameters are stored in a dictionary
session_type = params['session_type']                       # You pull them out with dictionary[key]
#icon_condition = params['icon_condition']
trials_per_block = params['trials_per_block']
blocks_per_session = params['blocks_per_session']
ITI = params['ITI']
duration = params['duration']
IBI = params['IBI']
run_time = params['run_time']


trial_type = [1, 1, 2, 2, 3, 3]



# START THE CLOCK
clock = pygame.time.Clock()
start_time = (pygame.time.get_ticks() / 1000)
stop_after = run_time * 60 * 1000

# CREATE THE TASK WINDOW
screen = setScreen(full_screen)
pygame.display.set_caption("Dot_Probe")
display_icon = pygame.image.load("Monkey Icon.png")
pygame.display.set_icon(display_icon)
screen.fill(white)

# DEFINE THE CURSOR
cursor = Box(color = red, speed = 8, circle = True)


"""MAKE ICONS FROM PNGs-------------------------------------------------------------------------------------------"""

icon_positions = [(125, 300), (675, 300)]                               # Set the LEFT/RIGHT positions

train1 = glob.glob('stimuli/training1/*.png')
train2 = glob.glob('stimuli/training2/*.png')

#idx = random.sample(range(len(train1)), 1)






"""CREATE THE DATA FILE-------------------------------------------------------------------------------------------"""
data_file = makeFileName('Dot_Probe')
writeLn(data_file, ['monkey', 'date', 'time', 'session_type', 'block', 'trial_number', 'trial_type', 'response_side', 'rxn_time', 'stimuli_1', 'stimuli_2'])



"""SET UP IS COMPLETE - EVERYTHING BELOW THIS IS RUNNING THE MAIN PROGRAM"""


# MAIN GAME LOOP ------------------------------------------------------------------------------------------------------

trial = Trial()             # Initialize a new Trial
#pseudorandomize(trial_type) # Randomise the original trials list so block 1 is randomised
trial.new()                 # Begin ;)

running = True
while running:
    quitEscQ()
    timer = (pygame.time.get_ticks() / 1000)
    if timer > run_time:
        pygame.quit()
        sys.exit()
    screen.fill(white)
    cursor.draw(screen)

    SELECT = cursor.collides_with_list(trial.stimuli)
    clock.tick(fps)
    if trial.startphase == True:
        trial.start()
    elif trial.startphase == False:
        if trial.phase1 == True:
            trial.flash_stimuli()
        elif trial.phase2 == True:
            trial.run_trial()



    refresh(screen)

# --------------------------------------------------------------------------------------------------------------------
