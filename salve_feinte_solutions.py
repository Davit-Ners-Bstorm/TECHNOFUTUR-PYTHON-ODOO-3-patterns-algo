# 1. Move Zeroes
# https://leetcode.com/problems/move-zeroes/
# Pattern : Two Pointers
# Temps : O(n)
# Mémoire : O(1)
class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        j = 0

        for i in range(len(nums)):
            if nums[i] != 0:
                nums[j], nums[i] = nums[i], nums[j]
                j += 1


# 2. First Unique Character in a String
# https://leetcode.com/problems/first-unique-character-in-a-string/
# Pattern : HashMap / comptage
# Temps : O(n)
# Mémoire : O(k), avec k = nombre de caractères distincts
class Solution:
    def firstUniqChar(self, s: str) -> int:
        counts = {}

        for char in s:
            counts[char] = counts.get(char, 0) + 1

        for i, char in enumerate(s):
            if counts[char] == 1:
                return i

        return -1


# 3. Best Time to Buy and Sell Stock
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
# Pattern : Greedy / minimum courant
# Temps : O(n)
# Mémoire : O(1)
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = prices[0]
        best_profit = 0

        for price in prices:
            min_price = min(min_price, price)
            best_profit = max(best_profit, price - min_price)

        return best_profit


# 4. Ransom Note
# https://leetcode.com/problems/ransom-note/description/
# Pattern : HashMap / fréquences
# Temps : O(n + m)
# Mémoire : O(k), avec k = nombre de caractères distincts
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        counts = {}

        for char in magazine:
            counts[char] = counts.get(char, 0) + 1

        for char in ransomNote:
            if char not in counts or counts[char] == 0:
                return False

            counts[char] -= 1

        return True


# 5. Merge Sorted Array
# https://leetcode.com/problems/merge-sorted-array/description/
# Pattern : Two Pointers / remplissage depuis la fin
# Temps : O(m + n)
# Mémoire : O(1)
class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        i = m - 1
        j = n - 1
        k = m + n - 1

        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1

            k -= 1

        while j >= 0:
            nums1[k] = nums2[j]
            j -= 1
            k -= 1
