# 1047. Remove All Adjacent Duplicates In String
class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack=[]

        for el in s:
            if stack and  stack[-1] == el:
                stack.pop()
            else:
                stack.append(el)
        return "".join(stack)



# 1456. Maximum Number of Vowels in a Substring of Given Length
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = set('aeiou')
        max_v = 0

        for i in range(0,k):
            if s[i] in vowels:
                max_v += 1

        actual = max_v
        for i in range(k,len(s)):
            if s[i-k] in vowels:
                actual -= 1
            if s[i] in vowels:
                actual += 1

            max_v = max(max_v,actual)

        return max_v


# 35. Search Insert Position
class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        
        left = 0
        right = len(nums)-1

        while left <= right:
            mid = (right + left)//2
            if target < nums[mid]:
                right=mid-1
            elif target > nums[mid]:
                left=mid+1
            else:
                return mid
        return left

# 242. Valid Anagram
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        dico_s = {}
        dico_t = {}

        for l in s:
            dico_s[l] = dico_s.get(l,0) + 1

        for l in t:
            dico_t[l] = dico_t.get(l,0) + 1
        
        return dico_s == dico_t


# Triangle number check
def is_triangle_number(number: int) -> bool:
    cpt = 1
    while number > 0:
        number -= cpt
        cpt+=1
    return number == 0
# Formule : 1 + 8*number doit donné carré parfait
