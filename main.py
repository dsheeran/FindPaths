# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import PathSearch

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    n=6
    ps = PathSearch.PathSearch(n)
    ps.search()
    number_solutions = len(ps.solutions)
    print(f"Path length {ps.PATH_LENGTH} has {number_solutions} solutions.")
    print(f"Visited {ps.visited} paths in {ps.time} seconds")
    print(ps.solutions)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
