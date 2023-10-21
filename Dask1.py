import dask.array as da
import random
import time
# Game of Life ----- Haniye - Ali
# Set the grid size and number of generations here
width = 5
height = 5
generations = 1

def initialize_grid(width, height):
    return da.random.choice([0, 1], size=(height, width), chunks=(100, 100))

def save_grid(grid, filename):
    grid.compute()
    height, width = grid.shape
    with open(filename, "w") as f:
        f.write(f"{width} {height}\n")
        for y in range(height):
            for x in range(width):
                if grid[y, x]:
                    f.write(f"{y} {x}\n")

def tick(grid):
    height, width = grid.shape
    temp = da.zeros((height, width), dtype=int, chunks=(100, 100))
    for y in range(height):
        for x in range(width):
            neighbors = grid[(y-1):(y+2), (x-1):(x+2)]
            live_neighbors = da.sum(neighbors) - grid[y, x]

            if grid[y, x] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    temp[y, x] = 0
                else:
                    temp[y, x] = 1
            elif grid[y, x] == 0:
                if live_neighbors == 3:
                    temp[y, x] = 1

    return temp

def main():
    grid = initialize_grid(width, height)

    start = time.time()

    for i in range(generations):
        grid = tick(grid)

    grid.compute()  # Ensure all Dask computations are completed before saving the result.

    print("{} seconds elapsed for {} generations.".format(round(time.time() - start, 2), generations))

    save_grid(grid, "output.txt")

if __name__ == "__main__":
    main()
#mprof run executable
#mprof plot