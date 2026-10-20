lst = ['A', 'B', 'C']

def backtracking(path = None):
    if not path:
        path = []

    if len(path) == len(lst):
        print(path)

    for letter in lst:
        if not letter in path:
            path.append(letter)
            backtracking(path)
            path.pop()

    return None

backtracking()
