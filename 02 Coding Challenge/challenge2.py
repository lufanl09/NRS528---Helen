######################
# Coding Challenge 2 #
######################

#1. List Values
num_list = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]

new_list = []

for i in num_list:
    if i < 5:
        new_list.append(i)
print(new_list)

#2. List overlap
list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']
overlap_list = list(set(list_a) & set(list_b))
print(overlap_list)

no_overlap_list = list(set(list_a) ^ set(list_b))
print(no_overlap_list)

#3. Given a single phrase, count the occurrence of each word
string = 'hi dee hi how are you mr dee'

string_split = string.split()
print(string_split)

l = len(string_split)
wordlist = []
for i in range(l):
    temp = 0
    for x in wordlist:
        if string_split[i] == x:
            temp = 1
    if temp == 0:
        wordlist.append(string_split[i])
wordcount = [0] * len(wordlist)
for j in range(l):
    for k in range(len(wordlist)):
        if string_split[j]==wordlist[k]:
            wordcount[k]=wordcount[k] + 1

for m in range(len(wordlist)):
    print( wordlist[m] + " " + str(wordcount[m]))

#4. User input
age = input("What is your age? ")
print("Your age is " + str(age))
retire_age = 65 - int(age)
print("You have " + str(retire_age) + " years until retirement")

#5. Scrabble
word = input("Pick a word! ")
print("The word you picked is " + str(word))

word_list = list(word)
print(word_list)

scores = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4,
          "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1,
          "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1,
          "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8,
          "y": 4, "z": 10}

total = 0
for letter in word_list:
    total = total + scores[letter]
print(total)























