import tkinter as tk
from tkinter import ttk
import random

class Heuristics:
    @staticmethod
    def manhattan_distance(state, goal_position):
        x1, y1 = state
        x2, y2 = goal_position
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def misplaced_blocks(state, goal_position, blocking_blocks_positions):
        if state == goal_position:
            return 0

        if state in blocking_blocks_positions:
            return 1

        return 1

class MoveBlockNode:
    def __init__(self, state, cost, actions, blocking_blocks_positions):
        self.state = state
        self.cost = cost
        self.actions = actions
        self.blocking_blocks_positions = blocking_blocks_positions

    def __lt__(self, other):
        return self.cost < other.cost

class MoveBlockProblem:
    def __init__(self, width, height, initial_state, goal_position, num_blocking_blocks):
        self.width = width
        self.height = height
        self.initial_state = initial_state
        self.goal_position = goal_position
        self.num_blocking_blocks = num_blocking_blocks
        self.cost = 0
        self.actions_taken = []
        self.blocking_blocks_positions = self.get_blocking_blocks_positions()

    def actions(self, state):
        possible_actions = ['left', 'right', 'up', 'down']
        return [action for action in possible_actions if self.is_valid_action(state, action)]

    def result(self, state, action):
        x, y = state
        if action == 'left':
            return (x - 1, y)
        elif action == 'right':
            return (x + 1, y)
        elif action == 'up':
            return (x, y - 1)
        elif action == 'down':
            return (x, y + 1)

    def is_valid_action(self, state, action):
        next_state = self.result(state, action)
        x, y = next_state
        return 0 <= x < self.width and 0 <= y < self.height and next_state not in self.blocking_blocks_positions

    def goal_test(self, state):
        return state == self.goal_position

    def get_blocking_blocks_positions(self):
        blocking_blocks_positions = set()
        while len(blocking_blocks_positions) < self.num_blocking_blocks:
            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 2)
            orientation = random.choice(['horizontal', 'vertical'])

            if orientation == 'horizontal':
                blocking_blocks_positions.add((x, y))
                blocking_blocks_positions.add((x + 1, y))
            else:
                blocking_blocks_positions.add((x, y))
                blocking_blocks_positions.add((x, y + 1))

        return blocking_blocks_positions

    def perform_action(self, action):
        if action == 'left':
            self.initial_state = self.result(self.initial_state, 'left')
        elif action == 'right':
            self.initial_state = self.result(self.initial_state, 'right')
        elif action == 'up':
            self.initial_state = self.result(self.initial_state, 'up')
        elif action == 'down':
            self.initial_state = self.result(self.initial_state, 'down')

    def is_valid_state(self, state):
        x, y = state
        return 0 <= x < self.width and 0 <= y < self.height and state not in self.blocking_blocks_positions

    def bfs(self):
        return self.search()

    def dfs(self):
        return self.search()

    def ucs(self):
        return self.search(ucs=True)

    def astar(self, heuristic):
        return self.search(ucs=True, heuristic=heuristic)

    def greedy(self, heuristic):
        return self.search(heuristic=heuristic)

    def search(self, ucs=False, heuristic=None):
        explored = set()
        start_node = MoveBlockNode(self.initial_state, 0, [], self.blocking_blocks_positions)
        frontier = [start_node]

        initial_blocking_blocks_positions = self.blocking_blocks_positions.copy()
        blocking_blocks_positions = initial_blocking_blocks_positions.copy()

        while frontier:
            frontier.sort(key=lambda x: x.cost, reverse=True) if ucs else frontier.sort(key=lambda x: x.cost + heuristic(x.state, self.goal_position) if heuristic else 0, reverse=True)
            current_node = frontier.pop()

            current_state = current_node.state

            print("Exploring state:", current_state, "with actions:", current_node.actions, "and cost:", current_node.cost)

            if current_state in explored or not self.is_valid_state(current_state):
                continue

            explored.add(current_state)

            if self.goal_test(current_state):
                self.actions_taken = current_node.actions
                self.cost = current_node.cost
                blocking_blocks_positions = self.get_blocking_blocks_positions()
                return self.actions_taken, self.cost, initial_blocking_blocks_positions, blocking_blocks_positions

            for action in self.actions(current_state):
                next_state = self.result(current_state, action)
                next_blocking_blocks_positions = self.update_blocking_blocks(current_state, next_state, blocking_blocks_positions)
                cost = current_node.cost + 1  # Each action has a cost of 1

                if heuristic is not None:
                    if heuristic.__name__ == 'manhattan_distance':
                        heuristic_value = heuristic(next_state, self.goal_position)
                    elif heuristic.__name__ == 'misplaced_blocks':
                        heuristic_value = heuristic(next_state, self.goal_position, next_blocking_blocks_positions)
                    else:
                        raise ValueError("Unsupported heuristic")

                else:
                    heuristic_value = 0

                priority = cost + heuristic_value

                if next_state not in explored and self.is_valid_state(next_state):
                    next_node = MoveBlockNode(next_state, cost, current_node.actions + [action], next_blocking_blocks_positions)
                    frontier.append(next_node)

        return None, None, None, None

    def update_blocking_blocks(self, current_state, next_state, blocking_blocks_positions):
        current_x, current_y = current_state
        next_x, next_y = next_state

        if next_x > current_x:
            action = 'right'
        elif next_x < current_x:
            action = 'left'
        elif next_y > current_y:
            action = 'down'
        elif next_y < current_y:
            action = 'up'
        else:
            action = None

        if action == 'left':
            blocking_blocks_positions = {(x + 1, y) for x, y in blocking_blocks_positions}
        elif action == 'right':
            blocking_blocks_positions = {(x - 1, y) for x, y in blocking_blocks_positions}
        elif action == 'up':
            blocking_blocks_positions = {(x, y + 1) for x, y in blocking_blocks_positions}
        elif action == 'down':
            blocking_blocks_positions = {(x, y - 1) for x, y in blocking_blocks_positions}

        return blocking_blocks_positions

class MoveBlockGUI(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self)
        self.move_block_problem = None
        self.algorithm = None
        self.heuristic_function = None

        self.title("Move Block Puzzle Solver")
        self.geometry("800x600")

        self.algorithm_var = tk.StringVar()
        self.heuristic_var = tk.StringVar()

        self.create_algorithm_selection()
        self.create_heuristic_selection()
        self.create_solve_button()
        self.create_canvas()  # Create canvas once

    def create_algorithm_selection(self):
        label = tk.Label(self, text="Select Algorithm:")
        label.pack(pady=10)

        algorithm_options = ['BFS', 'DFS', 'UCS', 'Greedy', 'A*']
        algorithm_combobox = ttk.Combobox(self, textvariable=self.algorithm_var, values=algorithm_options)
        algorithm_combobox.set(algorithm_options[0])
        algorithm_combobox.pack()

    def create_heuristic_selection(self):
        label = tk.Label(self, text="Select Heuristic (for Greedy and A*):")
        label.pack(pady=10)

        heuristic_options = ['Manhattan Distance', 'Misplaced Blocks']
        heuristic_combobox = ttk.Combobox(self, textvariable=self.heuristic_var, values=heuristic_options)
        heuristic_combobox.set(heuristic_options[0])
        heuristic_combobox.pack()

    def create_solve_button(self):
        solve_button = ttk.Button(self, text="Solve Puzzle", command=self.solve_puzzle)
        solve_button.pack(pady=20)

    def create_canvas(self):
        self.canvas = tk.Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack()

    def solve_puzzle(self):
        width = 8
        height = 8
        initial_state = (random.randint(0, 7), random.randint(0, 7))
        goal_position = (random.randint(0, 7), random.randint(0, 7))
        num_blocking_blocks = random.randint(0, 8)  # Adjust as needed

        self.move_block_problem = MoveBlockProblem(width, height, initial_state, goal_position, num_blocking_blocks)

        self.algorithm = self.algorithm_var.get().lower()
        if self.algorithm in ['greedy', 'astar']:
            heuristic_option = self.heuristic_var.get()
            self.heuristic_function = getattr(Heuristics, heuristic_option.lower().replace(" ", "_"))

        if self.algorithm == 'bfs':
            result = self.move_block_problem.bfs()
        elif self.algorithm == 'dfs':
            result = self.move_block_problem.dfs()
        elif self.algorithm == 'ucs':
            result = self.move_block_problem.ucs()
        elif self.algorithm in ['greedy', 'astar']:
            result = self.move_block_problem.greedy(self.heuristic_function)
        else:
            print("Invalid algorithm")
            return

        if result:
            actions, cost, initial_blocking_blocks, blocking_blocks_positions = result
            self.animate_moves(actions)
            total_cost = sum(cost for _ in actions)
            self.draw_grid()  # Ensure the final grid is displayed
            self.after(500, lambda: self.show_info_dialog(f"{self.algorithm.upper()}",
                                                          f"Goal reached with actions {actions}\nTotal cost to reach goal is {total_cost}"))
            self.after(1000, lambda: self.show_info_dialog("Blocking Block Positions",
                                                           f"Initial blocking block positions: {initial_blocking_blocks}\nFinal blocking block positions: {blocking_blocks_positions}"))

    def show_info_dialog(self, title, message):
        print(title + ":", message)

    def animate_moves(self, actions):
        self.move_block_problem = MoveBlockProblem(width, height, initial_state, goal_position, num_blocking_blocks)
        self.draw_grid()

        def animate(step=iter(actions)):
            try:
                action = next(step)
                self.move_block_problem.perform_action(action)
                self.draw_grid()
                self.after(500, animate, step)
            except StopIteration:
                pass

        animate()

    def draw_grid(self):
        self.canvas.delete("all")
        cell_size = 600 // self.move_block_problem.width
        for x in range(self.move_block_problem.width):
            for y in range(self.move_block_problem.height):
                color = "white"
                if (x, y) == self.move_block_problem.goal_position:
                    color = "blue"
                elif (x, y) in self.move_block_problem.blocking_blocks_positions:
                    color = "red"
                self.canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size,
                                             (y + 1) * cell_size, fill=color)

if __name__ == "__main__":
    width = 8
    height = 8
    initial_state = (random.randint(0, 7), random.randint(0, 7))
    goal_position = (random.randint(0, 7), random.randint(0, 7))
    num_blocking_blocks = random.randint(0, 8)  # Adjust as needed

    app = MoveBlockGUI()
    app.move_block_problem = MoveBlockProblem(width, height, initial_state, goal_position, num_blocking_blocks)
    app.mainloop()
