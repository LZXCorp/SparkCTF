from collections import deque
import flag_gen_deof

def solve_maze(maze):
    height = len(maze)
    width = len(maze[0])
    start = (0, 1)
    end = (height - 1, width - 2)

    # Directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # BFS initialization
    queue = deque([(start, 0)])
    visited = set()
    visited.add(start)
    path = {}

    while queue:
        (x, y), steps = queue.popleft()

        # Check if we've reached the exit
        if (x, y) == end:
            # Reconstruct the path
            solution_path = []
            while (x, y) != start:
                solution_path.append((x, y))
                x, y = path[(x, y)]
            solution_path.append(start)
            solution_path.reverse()
            return solution_path, len(solution_path)

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and (nx, ny) not in visited and maze[nx][ny] == ' ':
                queue.append(((nx, ny), steps + 1))
                visited.add((nx, ny))
                path[(nx, ny)] = (x, y)

    return None, 0  # If no solution is found

def visualize_solution(maze, solution):
    # Create a copy of the maze for visualization
    visualized_maze = [row[:] for row in maze]
    
    # Mark the solution path with '.'
    for x, y in solution:
        if visualized_maze[x][y] == ' ':
            visualized_maze[x][y] = '.'
    
    # Convert the maze back to string format
    visualized_maze_str = '\n'.join(''.join(row) for row in visualized_maze)
    return visualized_maze_str

with open("../dist/run_inc_chal.txt", "r") as file:
    maze_grid = [list(line.strip()) for line in file]



# Solve the maze
solution, steps = solve_maze(maze_grid)
visualized_solution = visualize_solution(maze_grid, solution)

visualized_filename = "./run_inc_soln.txt"
with open(visualized_filename, "w") as file:
    file.write(visualized_solution)

print(f"Steps: {steps}")
print(f"Flag: {flag_gen_deof.flag_gen(steps)}")