import random
from queue import Queue, LifoQueue, PriorityQueue


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

    def is_valid_state(self, state):
        x, y = state
        return 0 <= x < self.width and 0 <= y < self.height and state not in self.blocking_blocks_positions

    def bfs(self):
        return self.search(Queue())

    def dfs(self):
        return self.search(LifoQueue())

    def ucs(self):
        return self.search(PriorityQueue(), ucs=True)

    def astar(self, heuristic):
        return self.search(PriorityQueue(), ucs=True, heuristic=heuristic)

    def greedy(self, heuristic):
        return self.search(PriorityQueue(), heuristic=heuristic)

    def search(self, frontier, ucs=False, heuristic=None):
        explored = set()
        start_node = MoveBlockNode(self.initial_state, 0, [], self.blocking_blocks_positions)
        frontier.put((0, start_node))

        initial_blocking_blocks_positions = self.blocking_blocks_positions.copy()
        blocking_blocks_positions = initial_blocking_blocks_positions.copy()

        while not frontier.empty():
            current_priority, current_node = frontier.get()
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
                    next_node = MoveBlockNode(next_state, cost, current_node.actions + [action],  next_blocking_blocks_positions)
                    frontier.put((priority, next_node))

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


# Problem Definition
width = 8
height = 7
initial_state = (0, 3)
goal_position = (7, 4)
num_blocking_blocks = 3

move_block_problem = MoveBlockProblem(width, height, initial_state, goal_position, num_blocking_blocks)


# Select Algorithm
# algorithm = 'bfs'
algorithm = 'dfs'
# algorithm = 'ucs'
# algorithm = 'greedy'
# algorithm = 'astar'

# heuristic_function = Heuristics.misplaced_blocks
# heuristic_function = Heuristics.manhattan_distance

if algorithm == 'bfs':
    result = move_block_problem.bfs()
elif algorithm == 'dfs':
    result = move_block_problem.dfs()
elif algorithm == 'ucs':
    result = move_block_problem.ucs()
elif algorithm == 'greedy' or algorithm == 'astar':
    result = move_block_problem.greedy(heuristic_function) if algorithm == 'greedy' else move_block_problem.astar(heuristic_function)
else:
    print("Invalid algorithm")

if result:
    actions, cost, initial_blocking_blocks, blocking_blocks_positions = result
    if actions is not None:
        total_cost = sum(cost for _ in actions)  # Calculate total cost
        print(f"{algorithm.upper()}: Goal reached with actions {actions}")
        print(f"Total cost to reach goal is {total_cost}")
    else:
        print(f"{algorithm.upper()}: Goal reached with no actions.")
    print(f"Initial blocking block positions: {initial_blocking_blocks}")
    print(f"Final blocking block positions: {blocking_blocks_positions}")
else:
    print(f"{algorithm.upper()}: Goal not reachable.")
