# 238. Product of Array Except Self
# https://leetcode.com/problems/product-of-array-except-self/description/
# Pattern : Prefix / Suffix Products (produits préfixes et suffixes)
# Temps : O(n)
# Mémoire : O(1) supplémentaire (hors tableau résultat)
# Idée : résultat[i] = produit des éléments à gauche * produit des éléments à droite.
# On évite la division, et la méthode fonctionne aussi avec des zéros.
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        result = [1] * n

        # Premier passage : produit de tout ce qui est à GAUCHE de i.
        left_product = 1
        for i in range(n):
            result[i] = left_product
            left_product *= nums[i]

        # Deuxième passage : on multiplie par tout ce qui est à DROITE de i.
        right_product = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right_product
            right_product *= nums[i]

        return result


# 11. Container With Most Water
# https://leetcode.com/problems/container-with-most-water/description/
# Pattern : Two Pointers
# Temps : O(n)
# Mémoire : O(1)
# Idée : aire = largeur * plus petite des deux hauteurs.
# Pour espérer améliorer l'aire en réduisant la largeur,
# on doit avancer le pointeur qui correspond à la plus petite hauteur.
class Solution:
    def maxArea(self, height: list[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0

        while left < right:
            width = right - left
            h = min(height[left], height[right])
            max_area = max(max_area, width * h)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area


# 3. Longest Substring Without Repeating Characters
# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
# Pattern : Sliding Window / HashSet
# Temps : O(n)
# Mémoire : O(k), avec k = nombre de caractères distincts dans la fenêtre
# Idée : maintenir une fenêtre [left, right] sans caractères répétés.
# Si un caractère existe déjà, retirer des caractères par la gauche
# jusqu'à ce qu'on puisse l'ajouter sans doublon.
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1

            seen.add(s[right])
            max_length = max(max_length, right - left + 1)

        return max_length


# 15. 3Sum
# https://leetcode.com/problems/3sum/description/
# Pattern : Sorting + Two Pointers
# Temps : O(n²)
# Mémoire : O(n) pour le tri en Python (hors résultat)
# Idée : trier le tableau, fixer un nombre nums[i], puis chercher
# deux autres nombres dont la somme vaut -nums[i].
# ATTENTION aux doublons : chaque triplet doit apparaître une seule fois.
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []

        for i in range(len(nums) - 2):
            # Évite de repartir plusieurs fois du même premier nombre.
            if i > 0 and nums[i] == nums[i - 1]:
                continue
