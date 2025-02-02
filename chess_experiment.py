import pygame
import chess
from stockfish import Stockfish

# Initialize Stockfish (update the path to the Stockfish binary)
stockfish = Stockfish(path="/usr/games/stockfish")

# Pygame Initialization
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 700, 700
SQUARE_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load chess piece images
PIECE_IMAGES = {}
PIECES = ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']
for piece in PIECES:
    PIECE_IMAGES[piece] = pygame.image.load(f"assets/{piece}.jpg")

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Create a chess board
board = chess.Board()

# Game Mode
game_mode = None  # 'human' or 'ai'


def draw_board():
    """Draw the chessboard and pieces."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_image = PIECE_IMAGES[piece.symbol()]
                screen.blit(pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE)),
                            (col * SQUARE_SIZE, row * SQUARE_SIZE))


def get_stockfish_move():
    """Get the best move from Stockfish."""
    stockfish.set_fen_position(board.fen())
    return stockfish.get_best_move()


def get_square_under_mouse(pos):
    """Return the chess square under the mouse."""
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)


def highlight_square(square):
    """Highlight a square on the board."""
    row = 7 - chess.square_rank(square)
    col = chess.square_file(square)
    pygame.draw.rect(screen, GREEN, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)


def show_main_menu():
    """Display a menu for the user to select game mode."""
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Chess Game", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    font = pygame.font.Font(None, 50)
    ai_text = font.render("1. Play vs AI", True, WHITE)
    human_text = font.render("2. Play vs Human", True, WHITE)
    screen.blit(ai_text, (WIDTH // 2 - ai_text.get_width() // 2, HEIGHT // 2))
    screen.blit(human_text, (WIDTH // 2 - human_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.flip()


def main():
    global game_mode

    # Show the main menu
    show_main_menu()

    # Wait for user input to select the game mode
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = 'ai'
                    selecting = False
                elif event.key == pygame.K_2:
                    game_mode = 'human'
                    selecting = False

    # Game Loop
    running = True
    selected_square = None
    player_turn = True

    while running:
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                square = get_square_under_mouse(mouse_pos)

                if selected_square is None:
                    # Select a square with a piece
                    if board.piece_at(square):
                        selected_square = square
                        highlight_square(square)
                else:
                    # Make a move
                    move = chess.Move(from_square=selected_square, to_square=square)
                    if move in board.legal_moves:
                        board.push(move)
                        player_turn = False if game_mode == 'ai' else not player_turn
                    selected_square = None

        if game_mode == 'ai' and not player_turn and not board.is_game_over():
            # Stockfish's turn
            ai_move = get_stockfish_move()
            board.push(chess.Move.from_uci(ai_move))
            player_turn = True

        # Check for game over
        if board.is_game_over():
            print("Game over!")
            print("Result:", board.result())
            running = False

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()