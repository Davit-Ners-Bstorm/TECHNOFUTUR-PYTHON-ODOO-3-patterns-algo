# 1. Duplicate Encoder
# https://www.codewars.com/kata/54b42f9314d9229fd6000d9c
# Pattern : HashMap / fréquence
# Temps : O(n)
# Mémoire : O(k), avec k = nombre de caractères distincts
def duplicate_encode(word):
    word = word.lower()

    counts = {}

    for char in word:
        counts[char] = counts.get(char, 0) + 1

    result = ""

    for char in word:
        if counts[char] == 1:
            result += "("
        else:
            result += ")"

    return result


# 2. Unique In Order
# https://www.codewars.com/kata/54e6533c92449cc251001667
# Pattern : parcours linéaire / comparaison avec l’élément précédent
# Temps : O(n)
# Mémoire : O(n) pour le résultat
def unique_in_order(sequence):
    result = []

    for item in sequence:
        if not result or result[-1] != item:
            result.append(item)

    return result


# 3. Sort the Odd
# https://www.codewars.com/kata/578aa45ee9fd15ff4600090d
# Pattern : extraction → tri → reconstruction
# Temps : O(n log n) à cause du tri
# Mémoire : O(n)
def sort_array(source_array):
    odds = []

    for num in source_array:
        if num % 2 != 0:
            odds.append(num)

    odds.sort(reverse=True)

    result = []

    for num in source_array:
        if num % 2 != 0:
            result.append(odds.pop())
        else:
            result.append(num)

    return result


# 4. Fizz Buzz
# https://leetcode.com/problems/fizz-buzz/description/
# Pattern : conditions / modulo (loooool)
# Temps : O(n)
# Mémoire : O(n) pour le résultat
class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        result = []

        for i in range(1, n + 1):
            if i % 15 == 0:
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))

        return result


# 5. Check if the Sentence Is Pangram
# https://leetcode.com/problems/check-if-the-sentence-is-pangram/description/
# Pattern : Set / unicité
# Temps : O(n)
# Mémoire : O(1) ici, car maximum 26 lettres différentes

# V1 ONELINE
class Solution:
    def checkIfPangram(self, sentence: str) -> bool:
        return len(set(sentence)) == 26


# V2 explicite
# Temps : O(n)
# Mémoire : O(1) ici aussi, max 26 lettres
class Solution:
    def checkIfPangram(self, sentence: str) -> bool:
        seen = set()

        for char in sentence:
            seen.add(char)

        return len(seen) == 26
