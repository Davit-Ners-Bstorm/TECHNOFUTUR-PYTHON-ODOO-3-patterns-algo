# Lien LeetCode : https://leetcode.com/problems/valid-parentheses/description/

### Valid Parentheses (Stack)

def isValid(s: str) -> bool:
    combinaisons = {
        ")": "(",
        "]": "[",
        "}": "{"
    }

    stack = []

    for e in s:
        if e in '([{':
            stack.append(e)
        else:
            if not stack:
                return False
            if combinaisons.get(e) != stack[-1]:
                return False
            stack.pop()
    return not stack
