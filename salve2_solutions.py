# 1047. Remove All Adjacent Duplicates In String
# Pattern : Stack
# Temps : O(n)
# Mémoire : O(n) dans le pire cas
class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []

        for el in s:
            if stack and stack[-1] == el:
                stack.pop()
            else:
                stack.append(el)

        return "".join(stack)


# 1456. Maximum Number of Vowels in a Substring of Given Length
# Pattern : Sliding Window / fenêtre glissante
# Temps : O(n)
# Mémoire : O(1), car le set de voyelles a une taille fixe
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = set("aeiou")
        max_v = 0

        for i in range(0, k):
            if s[i] in vowels:
                max_v += 1

        actual = max_v

        for i in range(k, len(s)):
            if s[i - k] in vowels:
                actual -= 1

            if s[i] in vowels:
                actual += 1

            max_v = max(max_v, actual)

        return max_v


# 35. Search Insert Position
# Pattern : Binary Search
# Temps : O(log n)
# Mémoire : O(1)
class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if target < nums[mid]:
                right = mid - 1
            elif target > nums[mid]:
                left = mid + 1
            else:
                return mid

        return left


# 242. Valid Anagram
# Pattern : HashMap / fréquence
# Temps : O(n + m)
# Mémoire : O(k), avec k = nombre de caractères distincts
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        dico_s = {}
        dico_t = {}

        for l in s:
            dico_s[l] = dico_s.get(l, 0) + 1

        for l in t:
            dico_t[l] = dico_t.get(l, 0) + 1

        return dico_s == dico_t


# Triangle Number Check
# Pattern : simulation / soustractions successives
# Temps : O(sqrt(n))
# Mémoire : O(1)
def is_triangle_number(number: int) -> bool:
    cpt = 1

    while number > 0:
        number -= cpt
        cpt += 1

    return number == 0


# Version mathématique :
# Un nombre n est triangulaire si 8*n + 1 est un carré parfait.
#
# Exemple :
# n = 6
# 8*6 + 1 = 49 = 7²
# => 6 est triangulaire
