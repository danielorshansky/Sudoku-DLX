# made specifically for 9x9 sudokus, but dlx.py can solve different sudokus

from dlx import DLX

def solve(board):
    dlx = DLX()
    dlx.create_links(board, 9)
    dlx.search()
    for node in dlx.solutions:
        board[node.data[0]][node.data[1]] = node.data[2]
    return board

def generate():
    return solve([[0] * 9] * 9)

def solve_from_string(board_str):
    board = [[]]
    if board_str == "":
        print("The sudoku is invalid. Enter a valid 9x9 sudoku in the format: '123000089 450709023 709...'")
        return
    for char in board_str:
        if char == " ":
            if len(board[-1]) != 9:
                print("The sudoku is invalid. Enter a valid 9x9 sudoku in the format: '123000089 450709023 709...'")
                return
            board.append([])
            continue
        if char.isdigit():
            board[-1].append(int(char))
        else:
            print("The sudoku is invalid. Enter a valid 9x9 sudoku in the format: '123000089 450709023 709...'")
            return
    return(solve(board))

if __name__ == "__main__":
    solution = solve_from_string(input("Enter a valid 9x9 sudoku in the format: '123000089 450709023 709...': "))
    print("Solution: " + " ".join(["".join(str(value) for value in row) for row in solution]))
