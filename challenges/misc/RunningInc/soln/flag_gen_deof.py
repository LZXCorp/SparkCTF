initial = "SIG24"
num_to_word = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"
}
undefined = "BFS fr tried to reverse engineer my code, but he couldn't figure out the distance."

def obfuscate(word):
    obfuscated = ""
    for i, char in enumerate(word):
        if char.isalpha():
            if i % 3 == 0:
                obfuscated += char.upper()
            elif i % 2 == 0:
                obfuscated += str(ord(char))
            else:
                obfuscated += char.lower()
        else:
            obfuscated += char
    return obfuscated

def flag_gen(dist):
    words = [num_to_word[char] for char in str(dist)]
    joined_words = "_".join(words)
    obfuscated_words = "_".join(obfuscate(word) for word in joined_words.split("_"))

    flag = f"{initial}{{{obfuscated_words}}}"
    return flag

if __name__ == "__main__":
    flag = flag_gen(input("Enter the distance: "))
    print("Gen Flag: ", flag)