import heapq

easy_board = [[6, 0, 8, 7, 0, 2, 1, 0, 0],
              [4, 0, 0, 0, 1, 0, 0, 0, 2],
              [0, 2, 5, 4, 0, 0, 0, 0, 0],
              [7, 0, 1, 0, 8, 0, 4, 0, 5],
              [0, 8, 0, 0, 0, 0, 0, 7, 0],
              [5, 0, 9, 0, 6, 0, 3, 0, 1],
              [0, 0, 0, 0, 0, 6, 7, 5, 0],
              [2, 0, 0, 0, 9, 0, 0, 0, 8],
              [0, 0, 6, 8, 0, 5, 2, 0, 3]]

hard_board = [[0, 7, 0, 0, 4, 2, 0, 0, 0],
              [0, 0, 0, 0, 0, 8, 6, 1, 0],
              [3, 9, 0, 0, 0, 0, 0, 0, 7],
              [0, 0, 0, 0, 0, 4, 0, 0, 9],
              [0, 0, 3, 0, 0, 0, 7, 0, 0],
              [5, 0, 0, 1, 0, 0, 0, 0, 0],
              [8, 0, 0, 0, 0, 0, 0, 7, 6],
              [0, 5, 4, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 6, 1, 0, 0, 5, 0]]

''' 
Function for beautifying board. From stack overflow
https://stackoverflow.com/questions/61433589/variable-scope-is-incorrectly-global
'''


def print_board(board):
    print("-" * 37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |" * 3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-" * 37)
        elif i % 3 == 2:
            print("|" + "---+" * 8 + "---|")
        else:
            print("|" + "   +" * 8 + "   |")


'''
Function for checking if goal state is reached
'''


def check_completion_status(board):
    # Iterate through boards
    for i in range(len(board)):
        for j in range(len(board[i])):
            # If cell is unassigned
            if board[i][j] == 0:
                return False
    # If every cell assigned, return true
    return True


'''
Function takes in a list of cells and returns True if they're all 
assigned (not 0) and unique. Used to validate that rows, columns, and boxes
are unique.
'''


def all_diff(cells):
    for i in range(len(cells) - 1):
        for j in range(i + 1, len(cells)):
            if cells[i] == cells[j] and cells[i] != 0 and cells[j] != 0:
                return False
    return True


'''
Function for selecting the cell (X,Y) to assign next. Selects the
cell with the minimum number of values (MRV) possible.
'''


def select_unassigned_variable(board, domains):
    mrv = len(board)  # Initialize MRV to max domain size
    selection_x, selection_y = 0, 0  # Initialize response selection
    # Iterate through board
    for x in range(len(board)):
        for y in range(len(board[x])):
            # If board element not selected
            if board[x][y] == 0:
                # If domain size is less than MRV, select element and update MRV
                domain = get_domain(domains, x, y)
                if len(domain) < mrv:
                    selection_x = x
                    selection_y = y
                    mrv = len(domain)
    # Return selected element
    return selection_x, selection_y


'''
Validates an assignment given the current board.
Takes in a board, a cell (x,y), and an assignment
(val), and calls all_diff to ensure that every 
row, column, and box is unique.
'''


def is_valid(board, x, y, val):
    board[x][y] = val
    # First call arc consistency algorithm
    return (all_diff(board[x])  # Validate row
            # Validate column
            and all_diff([board[i][y] for i in range(len(board))])
            # Validate box using integer division
            and all_diff(
                [board[i][j] for i in range(x // 3 * 3, x // 3 * 3 + 3) for j in range(y // 3 * 3, y // 3 * 3 + 3)]))


'''
Returns the array of domains for a given board. Returns a 3D array with
each sudoku cell containing the domain for that cell.
'''


def initialize_domains(board):
    domains = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[i])):
            if board[i][j] != 0:
                row.append([])
            else:
                vals = []
                for val in range(1, len(board) + 1):
                    if is_valid(board, i, j, val):
                        vals.append(val)
                    board[i][j] = 0
                row.append(vals)
        domains.append(row)
    return domains


'''
Helper function used to count the number of
domains that get constrained by an assignment
(x, y, val). This value is used to order the 
selection queue.
'''


def get_num_constraining_vals(domains, x, y, value):
    count = 0
    # Count row neighbors that are constrined
    for i in range(len(domains)):
        if value in domains[i][y]:
            count += 1
    # Count column neighbors that are constrined
    for j in range(len(domains[x])):
        if value in domains[x][j]:
            count += 1
    # Count box neighbors that are constrined
    for i in range(x // 3 * 3, x // 3 * 3 + 3):
        for j in range(y // 3 * 3, y // 3 * 3 + 3):
            if value in domains[i][j]:
                count += 1
    return count


'''
Gets domain for selection (x,y), ordered by least constraining value (LCV)
'''


def get_domain(domains, x, y):
    domain = domains[x][y]
    # Prioritize each selection based on how many neighbors are affected
    queue = []
    response = []
    for i in range(len(domain)):
        heapq.heappush(queue, (get_num_constraining_vals(domains, x, y, domain[i]), domain[i]))
    # Add each possible value to response in order of priority
    while len(queue) > 0:
        response.append(heapq.heappop(queue)[1])
    # Return ordered domain list
    return response


'''
Prunes domain by pre-emptively removing invalid values.
'''


def prune_domain(board, domain, x, y):
    pruned_domain = []
    for val in domain:
        if is_valid(board, x, y, val):
            pruned_domain.append(val)
    return pruned_domain


'''
Implementation of the backtracking algorithm
'''


def backtrack(board, domains):
    # Check completion status of board
    if check_completion_status(board):
        print_board(board)
        return True
    # Select unassigned square on the board
    x, y = select_unassigned_variable(board, domains)
    # Get domain of possible values to iterate through
    domain = prune_domain(board, get_domain(domains, x, y), x, y)
    # For each potential value in domain
    for val in domain:
        # If value is consistent with constraints
        if is_valid(board, x, y, val):
            # Add value to board
            board[x][y] = val
            # Recursively solve the board
            result = backtrack(board.copy(), initialize_domains(board))
            if result:
                return result
            # If recursion failed, reassign and continue
        board[x][y] = 0
    # If this is reached, all no more possible values
    return False


def solve_board(board):
    backtrack(board, initialize_domains(board))


print_board(easy_board)
print_board(hard_board)
print("1. Easy Board")
print("2. Hard Board")
print("3. Custom Board")

selection = int(input("Enter the number of the board you would like to complete:"))
if selection == 1:
    solve_board(easy_board)
elif selection == 2:
    solve_board(hard_board)
elif selection == 3:
    custom_board = []
    for i in range(9):
        row = []
        for j in range(selection * selection):
            value = int(input("What value would you like for position {" + str(i) + "," + str(j) + "}. Please enter 0 "
                                                                                                   "if you would like "
                                                                                                   "to leave that "
                                                                                                   "position blank:"))
            if value < 0 or value > 9:
                raise ValueError("Invalid value. Please enter only 0-9.")
            row.append(value)
        custom_board.append(row)
    print("YOUR BOARD: ")
    print_board(custom_board)
    print("-------------------------------------------")
    if not solve_board(custom_board):
        print("The board you entered cannot be solved with the provided information.")
else:
    raise ValueError("Invalid selection. Please enter either 1, 2, or 3.")
