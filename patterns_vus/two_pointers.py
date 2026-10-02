# Lien LeetCode : https://leetcode.com/problems/valid-palindrome/description/

### Valid Palindrome (Two Pointers)

def isPalindrome(s: str) -> bool:
    left = 0
    rigth = len(s) - 1

    while left < rigth:
        while left < rigth and not s[left].isalnum():
            left += 1
        
        while left < rigth and not s[rigth].isalnum():
            rigth -= 1
        
        if s[left].lower() != s[rigth].lower():
            return False
        left += 1
        rigth -= 1
    
    return True
