import sys
import termios
import tty
import select
import time
from tetris_game import TetrisGame, COLORS

def get_key() -> str:
    """Get a single keypress without blocking."""
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        # Set stdin to non-blocking
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            if key == '\x03':  # Handle Ctrl+C
                raise KeyboardInterrupt
            return key
        return ''
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def clear_screen():
    """Clear the console screen."""
    print("\033[H\033[J", end="")

def main():
    game = TetrisGame()
    fall_time = time.time()
    fall_speed = 0.5  # Time in seconds between automatic drops

    print("\nTetris Controls:")
    print("h/l: Move left/right")
    print("k: Rotate piece")
    print("j: Soft drop")
    print("q: Quit game\n")
    print("Press any key to start...")
    input()

    while True:
        clear_screen()
        
        # Display game board and score
        print(f"Score: {game.score}")
        print("+" + "-" * (game.width * 2) + "+    Next Piece:")
        display = game.get_display_board()
        next_piece = game.get_next_piece_display()
        
        for i, row in enumerate(display):
            print("|", end="")
            for cell in row:
                print(COLORS[cell], end="")
            print("|", end="")
            
            # Show next piece preview to the right
            if i < 4:
                print("    ", end="")
                for cell in next_piece[i]:
                    print(COLORS[cell], end="")
            print()
            
        print("+" + "-" * (game.width * 2) + "+")

        if game.game_over:
            print("\nGame Over!")
            break

        # Handle input
        key = get_key()
        if key:  # Only process if we actually got a key
            if key == 'q':
                break
            elif key == 'h':  # Left
                game.move_piece(-1, 0)
            elif key == 'l':  # Right
                game.move_piece(1, 0)
            elif key == 'k':  # Rotate
                game.rotate_piece()
            elif key == 'j':  # Down
                game.move_piece(0, 1)

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
