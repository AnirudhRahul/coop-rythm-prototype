import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
NUM_LANES = 5
LANE_WIDTH = WIDTH // NUM_LANES
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Note constants
NOTE_WIDTH = 50
NOTE_HEIGHT = 20
NOTE_SPEED = 8

# Pointer Location
pointer = 1

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Lists to store notes
notes = []

# Function to generate a random note in one of the lanes
def generate_note():
    lane = random.randint(0, NUM_LANES-1)
    x = lane * LANE_WIDTH + (LANE_WIDTH - NOTE_WIDTH) // 2
    notes.append([x, 0])

# Main game loop
running = True
score = 0
hearts = 3
counter = 0
consec_notes = 0
combo = 0
freq = 40
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                pointer = max(pointer - 1, 0)

            if event.key == pygame.K_l:
                pointer = min(pointer + 1, NUM_LANES-1)

    # Generate notes at random intervals
    if counter == 0:
        generate_note()
    counter += 1
    counter %= int(freq)

    # Remove notes that go off the screen
    notes = [note for note in notes if note[1] < HEIGHT]

    # Clear the screen
    screen.fill(WHITE)

    # Draw the three lanes
    for x in range(LANE_WIDTH, WIDTH, LANE_WIDTH):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, HEIGHT))

    # Draw the pointer
    pygame.draw.rect(screen, GREEN, (pointer * LANE_WIDTH, HEIGHT - 10, LANE_WIDTH, 10))
    
    # Move and draw notes
    for note in notes:
        note[1] += int(NOTE_SPEED)
        pygame.draw.rect(screen, RED, (note[0], note[1], NOTE_WIDTH, NOTE_HEIGHT))

    # Check for user input to catch notes
    keys = pygame.key.get_pressed()

    notes_left = []
    for note in notes:
        if not note[1] + NOTE_HEIGHT >= HEIGHT - 10:
            notes_left.append(note)
            continue
        lane = note[0] // LANE_WIDTH
        hearts -= not pointer == lane
        consec_notes = consec_notes + 1 if pointer == lane else 0
        score += consec_notes
        combo = combo + 1 if pointer == lane else 0
        # if note[0] < LANE_WIDTH:
        #     hearts -= not pointer == 0
        #     consec_notes = consec_notes + 1 if pointer == 0 else 0
        #     combo = combo + 1 if pointer == 0 else 0
        # elif LANE_WIDTH <= note[0] < 2 * LANE_WIDTH:
        #     hearts -= not pointer == 1
        #     consec_notes = consec_notes + 1 if pointer == 1 else 0
        #     combo = combo + 1 if pointer == 1 else 0
        # elif 2 * LANE_WIDTH <= note[0] < 3 * LANE_WIDTH:
        #     hearts -= not pointer == 2
        #     consec_notes = consec_notes + 1 if pointer == 2 else 0
        #     combo = combo + 1 if pointer == 2 else 0
        # elif 3 * LANE_WIDTH <= note[0] < 4 * LANE_WIDTH:
        #     hearts -= not pointer == 3
        #     consec_notes = consec_notes + 1 if pointer == 3 else 0
        #     combo = combo + 1 if pointer == 3 else 0
        # elif 4 * LANE_WIDTH <= note[0]:
        #     hearts -= not pointer == 4
        #     consec_notes = consec_notes + 1 if pointer == 4 else 0
        #     combo = combo + 1 if pointer == 4 else 0
        
    notes = notes_left

    # Display the hearts
    font = pygame.font.Font(None, 36)
    hearts_text = font.render(f"Hearts: {hearts}", True, (0, 0, 0))
    screen.blit(hearts_text, (10, 10))

    combo_text = font.render(f"Combo: {combo}", True, (0, 0, 0))
    screen.blit(combo_text, (10, 35))


    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 60))

    if consec_notes == 10:
        hearts = min(hearts + 1, 3)
        consec_notes = 0

    if hearts == 0:
        break

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
    NOTE_SPEED += 0.001
    freq -= 0.001

# Quit Pygame
pygame.quit()
sys.exit()
