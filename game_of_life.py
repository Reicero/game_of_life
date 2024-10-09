import pygame
import numpy as np
import random

# Initialisation de Pygame
pygame.init()

# Définition des dimensions initiales de la fenêtre et de la zone du compteur
GRID_WIDTH, GRID_HEIGHT = 600, 600
COUNTER_HEIGHT = 100
WINDOW_WIDTH, WINDOW_HEIGHT = GRID_WIDTH, GRID_HEIGHT + COUNTER_HEIGHT
CELL_SIZE = 5

# Définition des types de cellules
STATE_DEAD = 0
STATE_A = 1
STATE_B = 2

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Initialisation de la police
pygame.font.init()
font = pygame.font.Font(None, 36)

# Fonction pour initialiser la grille avec une certaine probabilité de cellules vivantes et de types de cellules
def init_grid_random(width, height, probability):
    grid = np.zeros((width, height))
    for y in range(height):
        for x in range(width):
            if random.random() < probability:
                grid[x, y] = random.choice([STATE_A, STATE_B])  # Choisissez aléatoirement entre les états A et B
    return grid

# Fonction pour dessiner la grille en bleu pour les cellules de type A et en rouge pour les cellules de type B
def draw_grid(screen, grid):
    surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))  # Créer une surface pour dessiner la grille
    surface.set_colorkey(WHITE)  # Définir le blanc comme couleur clé (transparente)

    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            if grid[x, y] == STATE_A:
                color = BLUE
            elif grid[x, y] == STATE_B:
                color = RED
            else:
                color = WHITE 
            pygame.draw.rect(surface, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    screen.blit(surface, (0, COUNTER_HEIGHT))  # Dessiner la surface en dessous de la zone du compteur

# Fonction pour afficher le texte à l'écran
def draw_text(screen, text, position, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Fonction pour compter le nombre de voisins vivants autour d'une cellule donnée
def next_generation(grid):
    new_grid = np.zeros_like(grid)  # Créer une nouvelle grille vide de la même taille

    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            # Compter le nombre de voisins vivants de type A, de type B et de cellules mortes
            count_a = 0
            count_b = 0
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue  # Ignorer la cellule elle-même
                    neighbor_x = (x + i) % grid.shape[0]  # Gérer les bords de la grille
                    neighbor_y = (y + j) % grid.shape[1]  # Gérer les bords de la grille
                    
                    if 0 <= x + i < grid.shape[0] and 0 <= y + j < grid.shape[1]:
                        count += grid[neighbor_x, neighbor_y]
                    
                    if grid[neighbor_x, neighbor_y] == STATE_A:
                        count_a += 1
                    elif grid[neighbor_x, neighbor_y] == STATE_B:
                        count_b += 1
            
            total_alive_neighbors = count_a + count_b

            # Appliquer les nouvelles règles en fonction des voisins
            if grid[x, y] in [STATE_A, STATE_B]:
                if total_alive_neighbors == 2 or total_alive_neighbors == 3:
                    new_grid[x, y] = grid[x, y]  # La cellule reste vivante
                else:
                    new_grid[x, y] = STATE_DEAD  # La cellule meurt
            else:
                # Les cellules mortes deviennent vivantes si elles ont exactement 3 voisins vivants
                if total_alive_neighbors == 3:
                    new_grid[x, y] = STATE_A if count_a > count_b else STATE_B

    return new_grid

# Création de la fenêtre d'affichage
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Jeu de la Vie")

# Initialisation de la grille avec une probabilité de 0.5 de cellules vivantes et de types de cellules
grid = init_grid_random(GRID_WIDTH // CELL_SIZE, GRID_HEIGHT // CELL_SIZE, 0.4)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:  # Détecter le redimensionnement de la fenêtre
            WINDOW_WIDTH, WINDOW_HEIGHT = event.size
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
            GRID_WIDTH, GRID_HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT - COUNTER_HEIGHT  # Adapter la taille de la grille
            grid = init_grid_random(GRID_WIDTH // CELL_SIZE, GRID_HEIGHT // CELL_SIZE, 0.4)  # Réinitialiser la grille
    
    # Calculer la prochaine génération de la grille
    grid = next_generation(grid)

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner la grille mise à jour
    draw_grid(screen, grid)

    # Compter le nombre de cellules de type A et de type B
    count_a = np.count_nonzero(grid == STATE_A)
    count_b = np.count_nonzero(grid == STATE_B)

    # Créer les textes pour les compteurs
    text_a = font.render(f"Type A: {count_a}", True, BLUE)
    text_b = font.render(f"Type B: {count_b}", True, RED)
    
    # Calculer la largeur totale des textes pour centrer le fond gris
    total_width = max(text_a.get_width(), text_b.get_width()) + 20  # Ajout d'un peu de padding
    rect_x = (WINDOW_WIDTH - total_width) // 2
    rect_y = 10
    rect_height = 80
    
    # Afficher le fond gris centré
    pygame.draw.rect(screen, GRAY, (rect_x, rect_y, total_width, rect_height))
    
    # Afficher les textes centrés sur le fond gris
    screen.blit(text_a, (rect_x + 10, rect_y + 10))
    screen.blit(text_b, (rect_x + 10, rect_y + 40))

    pygame.display.flip()  # Mettre à jour l'affichage

    pygame.time.delay(100)  # Ajouter un léger délai pour ralentir la simulation

# Fermeture de Pygame
pygame.quit()