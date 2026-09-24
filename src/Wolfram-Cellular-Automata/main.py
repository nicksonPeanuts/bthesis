import sys
import pygame
import numpy as np
import colorsys

pygame.init()

# lsita de constante
WIDTH, HEIGHT = 1000, 600
UI_WIDTH = 230
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER_COLOR = (70, 200, 70)
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (30, 30, 30)
INPUT_BOX_COLOR = (200, 200, 200)
INPUT_BOX_ACTIVE_COLOR = (255, 255, 255)
CHECKMARK_COLOR = (200, 200, 200)
CHECKMARK_ACTIVE_COLOR = (50, 200, 50)

# fonturi
pygame.font.init()
FONT = pygame.font.SysFont(None, 36)

# Global variables
cell_size = 10
grid_width = (WIDTH - UI_WIDTH) // cell_size
generations = HEIGHT // cell_size
rule_number = 30
is_running = False
use_rainbow = False

def draw_button(screen, rect, text, is_hovered):
    if text == "Stop":
        color = (200, 50, 50) if is_hovered else (150, 0, 0)  # Roșu pentru butonul de stop
    else:
        color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_input_box(screen, rect, text, is_active):
    color = INPUT_BOX_ACTIVE_COLOR if is_active else INPUT_BOX_COLOR
    pygame.draw.rect(screen, color, rect, 2)
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(midleft=(rect.x + 5, rect.centery))
    screen.blit(text_surface, text_rect)

def draw_checkmark(screen, rect, is_checked):
    pygame.draw.rect(screen, CHECKMARK_COLOR, rect, 2)
    if is_checked:
        pygame.draw.line(screen, CHECKMARK_ACTIVE_COLOR, (rect.left + 5, rect.centery), (rect.centerx, rect.bottom - 5), 3)
        pygame.draw.line(screen, CHECKMARK_ACTIVE_COLOR, (rect.centerx, rect.bottom - 5), (rect.right - 5, rect.top + 5), 3)

def get_color(gen_nr):
    if use_rainbow:
        hue = (gen_nr * 0.03) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return int(r * 255), int(g * 255), int(b * 255)
    else:
        return 255, 255, 255

def new_generation(generation, rule_binary):
    nextgen = np.zeros_like(generation)
    for i in range(1, len(generation) - 1):
        ruleset = (generation[i - 1], generation[i], generation[i + 1])
        index = 7 - (ruleset[0] * 4 + ruleset[1] * 2 + ruleset[2] * 1)
        nextgen[i] = rule_binary[index]
    return nextgen

def display_generation(surface, gen_nr, generation, cell_size):
    for x, cell in enumerate(generation):
        color = get_color(gen_nr) if cell == 1 else (0, 0, 0)
        pygame.draw.rect(surface, color, (x * cell_size, gen_nr * cell_size, cell_size, cell_size))

def binary_of(number, bits=8):
    return [int(bit) for bit in f"{number:0{bits}b}"]

def main():
    global rule_number, cell_size, grid_width, generations, is_running, use_rainbow

    # Initialize pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wolfram's Game of Life")
    clock = pygame.time.Clock()

    # Create a separate surface for the automaton
    automaton_surface = pygame.Surface((WIDTH - UI_WIDTH, HEIGHT))
    automaton_surface.fill(BACKGROUND_COLOR)

    # Input boxes and buttons
    rule_input_box = pygame.Rect(WIDTH - UI_WIDTH + 20, 50, 200, 40)
    cell_size_input_box = pygame.Rect(WIDTH - UI_WIDTH + 20, 120, 200, 40)
    start_button = pygame.Rect(WIDTH - UI_WIDTH + 20, 190, 200, 50)
    checkmark_box = pygame.Rect(WIDTH - UI_WIDTH + 20, 260, 30, 30)

    rule_input = str(rule_number)
    cell_size_input = str(cell_size)

    rule_input_active = False
    cell_size_input_active = False

    # Simulation variables
    gen_nr = 0
    generation = np.zeros(grid_width, dtype=int)
    generation[grid_width // 2] = 1

    while True:
        screen.fill(BACKGROUND_COLOR)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rule_input_box.collidepoint(event.pos):
                    rule_input_active = True
                    cell_size_input_active = False
                elif cell_size_input_box.collidepoint(event.pos):
                    rule_input_active = False
                    cell_size_input_active = True
                elif start_button.collidepoint(event.pos):
                    is_running = not is_running
                    if is_running:
                        try:
                            rule_number = int(rule_input)
                            if not 0 <= rule_number <= 255:
                                raise ValueError
                        except ValueError:
                            rule_number = 82

                        try:
                            cell_size = int(cell_size_input)
                            if cell_size <= 0:
                                raise ValueError
                        except ValueError:
                            cell_size = 10

                        grid_width = (WIDTH - UI_WIDTH) // cell_size
                        generations = HEIGHT // cell_size

                        gen_nr = 0
                        generation = np.zeros(grid_width, dtype=int)
                        generation[grid_width // 2] = 1
                elif checkmark_box.collidepoint(event.pos):
                    use_rainbow = not use_rainbow
                else:
                    rule_input_active = False
                    cell_size_input_active = False

            if event.type == pygame.KEYDOWN:
                if rule_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        rule_input = rule_input[:-1]
                    else:
                        rule_input += event.unicode
                elif cell_size_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        cell_size_input = cell_size_input[:-1]
                    else:
                        cell_size_input += event.unicode

        # Draw UI elements
        draw_input_box(screen, rule_input_box, rule_input, rule_input_active)
        draw_input_box(screen, cell_size_input_box, cell_size_input, cell_size_input_active)
        draw_button(screen, start_button, "Start" if not is_running else "Stop", start_button.collidepoint(pygame.mouse.get_pos()))
        draw_checkmark(screen, checkmark_box, use_rainbow)

        checkmark_text = FONT.render("Rainbow", True, TEXT_COLOR)
        screen.blit(checkmark_text, (checkmark_box.right + 10, checkmark_box.top))

        # Functia prin care se simuleaa automaata
        if is_running:
            if gen_nr < generations:
                display_generation(automaton_surface, gen_nr, generation, cell_size)
                gen_nr += 1
                generation = new_generation(generation, binary_of(rule_number))

        # Blit the automaton surface onto the main screen
        screen.blit(automaton_surface, (0, 0))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main() 
