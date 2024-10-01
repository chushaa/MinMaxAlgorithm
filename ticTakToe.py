import random
import argparse
import time

# Display the Tic-Tac-Toe board
def display_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

# Check if a player has won
def check_win(board, mark):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]

    return any(board[i] == board[j] == board[k] == mark for i, j, k in win_conditions)

# Check if the board is full
def check_full(board):
    return ' ' not in board

# Human player move
def player_move(board, mark):
    while True:
        move = input(f"Player {mark}, enter your move (1-9): ")
        try:
            move = int(move) - 1  # Adjust to zero-based index
            if board[move] == ' ':
                board[move] = mark
                break
            else:
                print("This spot is already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid move. Enter a number between 1 and 9.")

# Basic Minimax algorithm for optimal move
def minimax(board, depth, is_maximizing):
    if check_win(board, 'O'):
        return 1  # Computer win
    if check_win(board, 'X'):
        return -1  # Human win
    if check_full(board):
        return 0  # Tie

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Minimax with Alpha-Beta Pruning
def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing):
    if check_win(board, 'O'):
        return 1  # Computer win
    if check_win(board, 'X'):
        return -1  # Human win
    if check_full(board):
        return 0  # Tie

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax_alpha_beta(board, depth + 1, alpha, beta, False)
                board[i] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                board[i] = ' '
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
        return best_score

# Computer player move with selected algorithm (Minimax or Minimax with Pruning)
def computer_move(board, mark, use_pruning, is_first_move=False):
    best_score = -float('inf')
    best_moves = []  # List of equally good moves

    for i in range(9):
        if board[i] == ' ':
            board[i] = mark
            if use_pruning:
                score = minimax_alpha_beta(board, 0, -float('inf'), float('inf'), mark == 'O')
            else:
                score = minimax(board, 0, mark == 'O')
            board[i] = ' '

            if score > best_score:
                best_score = score
                best_moves = [i]  # Reset best moves list
            elif score == best_score:
                best_moves.append(i)  # Add equally good move

    # If it's the first move and there are multiple equally good moves, pick randomly
    if is_first_move and len(best_moves) > 1:
        move = random.choice(best_moves)
    else:
        move = best_moves[0]

    board[move] = mark
    print(f"Computer ({mark}) chose position {move + 1}")

# Main game function
def play_game(player1_is_human, use_pruning):
    board = [' '] * 9  # Initialize the board
    current_player = 'X'
    first_move = True  # Track if it's the first move

    # Start the stopwatch
    start_time = time.time()

    while True:
        display_board(board)

        if current_player == 'X':
            if player1_is_human:
                player_move(board, 'X')
            else:
                computer_move(board, 'X', use_pruning, is_first_move=first_move)
        else:
            computer_move(board, 'O', use_pruning)

        first_move = False  # Set first move to false after the first turn

        # Check for win
        if check_win(board, current_player):
            display_board(board)
            if current_player == 'X' and player1_is_human:
                print("Player 1 (X) wins!")
            elif current_player == 'X' and not player1_is_human:
                print("Computer (X) wins!")
            else:
                print("Computer (O) wins!")
            break

        # Check for tie
        if check_full(board):
            display_board(board)
            print("It's a tie!")
            break

        # Switch player
        current_player = 'O' if current_player == 'X' else 'X'

    # Stop the stopwatch and print the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Game over! Total time: {elapsed_time:.2f} seconds.")

# Argument parser to select game mode and algorithm
def main():
    parser = argparse.ArgumentParser(description="Tic Tac Toe game mode and algorithm selector.")
    parser.add_argument('mode', choices=['1', '2'],
                        help="Choose '1' for Human vs Computer or '2' for Computer vs Computer")
    parser.add_argument('algorithm', choices=['x', 'o'],
                        help="Choose 'x' for Minimax or 'o' for Minimax with Alpha-Beta Pruning")
    args = parser.parse_args()

    # Determine if Player 1 is human-controlled based on the mode
    player1_is_human = (args.mode == '1')

    # Determine whether to use Alpha-Beta Pruning based on the second argument
    use_pruning = (args.algorithm == 'o')

    if player1_is_human:
        print(f"You chose Human vs Computer mode with {'Alpha-Beta Pruning' if use_pruning else 'Minimax'} algorithm.")
    else:
        print(f"You chose Computer vs Computer mode with {'Alpha-Beta Pruning' if use_pruning else 'Minimax'} algorithm.")

    play_game(player1_is_human, use_pruning)

if __name__ == "__main__":
    main()
