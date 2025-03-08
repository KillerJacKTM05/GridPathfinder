import heapq
from typing import List, Tuple, Dict, Set

class GridPathfinder:
    def __init__(self, grid: List[str]):
        # Convert the grid string representation to a 2D list
        self.grid = [list(row) for row in grid]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        
        # Find start (S) and goal (G) positions
        self.start = self.find_position('S')
        self.goal = self.find_position('G')
        
    def find_position(self, char: str) -> Tuple[int, int]:
        """Find the position of a character in the grid."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == char:
                    return (i, j)
        return None

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions (N, S, E, W)."""
        row, col = pos
        neighbors = []
        # Check all four directions
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:  # N, S, W, E
            new_row, new_col = row + dr, col + dc
            # Check if position is valid and not blocked
            if (0 <= new_row < self.rows and 
                0 <= new_col < self.cols and 
                self.grid[new_row][new_col] != '1'):
                neighbors.append((new_row, new_col))
        return neighbors

    def find_shortest_path(self) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Find shortest path using Dijkstra's algorithm.
        Returns the path and set of explored cells.
        """
        # Priority queue for Dijkstra's algorithm
        pq = [(0, self.start, [self.start])]  # (distance, position, path)
        distances = {self.start: 0}  # Keep track of shortest distances
        explored = set()  # Keep track of explored cells

        while pq:
            current_dist, current_pos, current_path = heapq.heappop(pq)
            
            # Skip if we've found a shorter path to this position
            if current_pos in explored:
                continue
                
            # Mark as explored
            explored.add(current_pos)
            
            # Check if we've reached the goal
            if current_pos == self.goal:
                return current_path, explored
            
            # Explore neighbors
            for next_pos in self.get_neighbors(current_pos):
                # Calculate new distance
                new_dist = current_dist + 1
                
                # If we haven't found a shorter path to this neighbor
                if new_dist < distances.get(next_pos, float('inf')):
                    distances[next_pos] = new_dist
                    new_path = current_path + [next_pos]
                    heapq.heappush(pq, (new_dist, next_pos, new_path))
        
        return None, explored

    def visualize_path(self, path: List[Tuple[int, int]], explored: Set[Tuple[int, int]]):
        """Visualize the path and exploration."""
        # Create a copy of the grid for visualization
        vis_grid = [row[:] for row in self.grid]
        
        # Mark explored cells
        for r, c in explored:
            if (r, c) not in path and vis_grid[r][c] not in ['S', 'G']:
                vis_grid[r][c] = '.'
        
        # Mark path cells
        for r, c in path:
            if vis_grid[r][c] not in ['S', 'G']:
                vis_grid[r][c] = '*'
        
        # Print the visualization
        for row in vis_grid:
            print(''.join(row))

# Example usage
if __name__ == "__main__":
    # Your grid
    grid = [
        "0000100000",
        "0010100110",
        "0110001010",
        "0001000010",
        "0110000110",
        "0100110100",
        "0101010110",
        "01G1011000",
        "0111110110",
        "0000S00000"
    ]
    
    pathfinder = GridPathfinder(grid)
    path, explored = pathfinder.find_shortest_path()
    
    if path:
        print("Path found! Length:", len(path) - 1)
        print("\nVisualization ('.' = explored, '*' = path):")
        pathfinder.visualize_path(path, explored)
        
        # Print directions
        directions = []
        for i in range(len(path) - 1):
            curr_r, curr_c = path[i]
            next_r, next_c = path[i + 1]
            if next_r < curr_r:
                directions.append('N')
            elif next_r > curr_r:
                directions.append('S')
            elif next_c < curr_c:
                directions.append('W')
            else:
                directions.append('E')
        print("\nDirections:", ''.join(directions))
    else:
        print("No path found!")