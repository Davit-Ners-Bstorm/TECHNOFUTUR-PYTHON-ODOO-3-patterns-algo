# 392. Is Subsequence
# https://leetcode.com/problems/is-subsequence/description/
# Pattern : Two Pointers
# Temps : O(m), avec m = longueur de t
# Mémoire : O(1)
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0

        for char in t:
            if i < len(s) and s[i] == char:
                i += 1

        return i == len(s)


# 169. Majority Element V1
# https://leetcode.com/problems/majority-element/description/
# Pattern : HashMap / comptage de fréquences
# Temps : O(n)
# Mémoire : O(k), avec k = nombre de valeurs distinctes
class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        counts = {}

        for num in nums:
            counts[num] = counts.get(num, 0) + 1

            if counts[num] > len(nums) // 2:
                return num



# 169. Majority Element V2
# https://leetcode.com/problems/majority-element/description/
# Pattern : Boyer-Moore Voting Algorithm
# Temps : O(n)
# Mémoire : O(1)
# L'énoncé garantit qu'un élément apparaît plus de n/2 fois.
class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        candidate = None
        count = 0

        for num in nums:
            if count == 0:
                candidate = num

            if num == candidate:
                count += 1
            else:
                count -= 1

        return candidate


# 977. Squares of a Sorted Array
# https://leetcode.com/problems/squares-of-a-sorted-array/description/
# Pattern : Two Pointers
# Temps : O(n)
# Mémoire : O(n) pour le tableau résultat
class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        left = 0
        right = len(nums) - 1
        result = [0] * len(nums)
        index = len(nums) - 1

        while left <= right:
            left_square = nums[left] ** 2
            right_square = nums[right] ** 2

            if left_square > right_square:
                result[index] = left_square
                left += 1
            else:
                result[index] = right_square
                right -= 1

            index -= 1

        return result


# 349. Intersection of Two Arrays
# https://leetcode.com/problems/intersection-of-two-arrays/description/
# Pattern : Hash Set
# Temps : O(n + m) en moyenne
# Mémoire : O(n + m) dans le pire cas
class Solution:
    def intersection(self, nums1: list[int], nums2: list[int]) -> list[int]:
        seen = set(nums1)
        result = set()

        for num in nums2:
            if num in seen:
                result.add(num)

        return list(result)


# 605. Can Place Flowers
# https://leetcode.com/problems/can-place-flowers/description/
# Pattern : Greedy / algorithme glouton
# Temps : O(n), avec n = longueur de flowerbed
# Mémoire : O(1), car le tableau est modifié sur place
class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        count = 0

        for i in range(len(flowerbed)):
            if flowerbed[i] == 0:
                left_empty = i == 0 or flowerbed[i - 1] == 0
                right_empty = i == len(flowerbed) - 1 or flowerbed[i + 1] == 0

                if left_empty and right_empty:
                    flowerbed[i] = 1
                    count += 1

                    if count >= n:
                        return True

        return count >= n
