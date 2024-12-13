import sys
import termios
import tty
import select
import time
from tetris_game import TetrisGame, COLORS

def get_key() -> str:
    """Get a single keypress without blocking."""
    def is_data():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        if is_data():
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return ''

def clear_screen():
    """Clear the console screen."""
    print("\033[H\033[J", end="")

def main():
    game = TetrisGame()
    fall_time = time.time()
    fall_speed = 0.5  # Time in seconds between automatic drops

    print("\nTetris Controls:")
    print("←/→: Move left/right")
    print("↑: Rotate piece")
    print("↓: Soft drop")
    print("q: Quit game\n")
    print("Press any key to start...")
    input()

    while True:
        clear_screen()
        
        # Display game board and score
        print(f"Score: {game.score}")
        print("┌" + "──" * game.width + "┐")
        display = game.get_display_board()
        for row in display:
            print("│", end="")
            for cell in row:
                print(COLORS[cell], end="")
            print("│")
        print("└" + "──" * game.width + "┘")

        if game.game_over:
            print("\nGame Over!")
            break

        # Handle input
        key = get_key()
        if key == 'q':
            break
        elif key == '\x1b':
            # Handle arrow keys
            try:
                next_char = sys.stdin.read(1)
                if next_char == '[':
                    next_char = sys.stdin.read(1)
                    if next_char == 'A':  # Up arrow
                        game.rotate_piece()
                    elif next_char == 'B':  # Down arrow
                        game.move_piece(0, 1)
                    elif next_char == 'C':  # Right arrow
                        game.move_piece(1, 0)
                    elif next_char == 'D':  # Left arrow
                        game.move_piece(-1, 0)
            except:
                pass

        # Automatic falling
        current_time = time.time()
        if current_time - fall_time > fall_speed:
            game.step()
            fall_time = current_time

        time.sleep(0.05)  # Prevent CPU overuse

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user")
