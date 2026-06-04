class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        match_dict = {"2":["a","b","c"], "3":["d","e","f"], "4":["g","h","i"], "5":["j","k","l"], "6":["m","n","o"], "7":["p","q","r","s"], "8":["t","u","v"], "9":["w","x","y","z"]}
        
        result = []
        def backtrack(index: int, path: list[str]):
            if len(path) == len(digits):
                result.append("".join(path))
                return
            current_digit = digits[index]
            letters = match_dict[current_digit]
            for letter in letters:
                path.append(letter)
                backtrack(index+1, path)
                path.pop()
    
        backtrack(0,[])
        return result

test = Solution()
print(test.letterCombinations("23"))