class Solution:
    def romanToInt(self, s: str) -> int:
        total = 0
        roman_dict = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}

        current = 0
        while current < len(s):
            if current != len(s) - 1:
                if roman_dict[s[current]] < roman_dict[s[current+1]]:
                    total = total + roman_dict[s[current+1]] - roman_dict[s[current]]
                    current += 2
                else:
                    total += roman_dict[s[current]]
                    current += 1
            elif current == len(s) - 1:
                total += roman_dict[s[current]]
                current += 1

        
        return total

test = Solution()
print(test.romanToInt("MCMXCIV"))