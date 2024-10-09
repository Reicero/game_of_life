
import pygame
import numpy as np

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonction pour initialiser la grille
def init_grid(width, height):
    return np.random.choice([0, 1], (width, height))

# Fonction pour dessiner la grille
def draw_grid(screen, grid):
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            color = WHITE if grid[x, y] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Fonction pour calculer la prochaine génération de la grille
def next_generation(grid):
    new_grid = np.zeros_like(grid)  # Crée une nouvelle grille de la même taille que la grille actuelle

    # Parcourir chaque cellule de la grille
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            # Compter le nombre de voisins vivants
            count = count_neighbors(grid, x, y)

            # Appliquer les règles du jeu de la vie
            if grid[x, y] == 1:  # Cellule vivante
                if count == 2 or count == 3:
                    new_grid[x, y] = 1  # La cellule reste vivante
                else:
                    new_grid[x, y] = 0  # La cellule meurt
            else:  # Cellule morte
                if count == 3:
                    new_grid[x, y] = 1  # Une nouvelle cellule naît

    return new_grid

# Fonction pour compter le nombre de voisins vivants d'une cellule donnée
def count_neighbors(grid, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Ignorer la cellule elle-même
            if 0 <= x + i < grid.shape[0] and 0 <= y + j < grid.shape[1]:
                count += grid[x + i, y + j]
    return count

# Création de la fenêtre d'affichage
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de la Vie")

# Initialisation de la grille
grid = init_grid(WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculer la prochaine génération de la grille
    grid = next_generation(grid)

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner la grille mise à jour à l'écran
    draw_grid(screen, grid)

    pygame.display.flip()  # Mettre à jour l'affichage

    pygame.time.delay(100)  # Attente de 100 millisecondes avant de mettre à jour la grille

pygame.quit()
