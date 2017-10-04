import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    output = n * string
    return output

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    length = min([len(nums), 4])
    is_nine = False
    index = 0
    while (not is_nine) and (index < length):
        if nums[index] == 9:
            is_nine = True
        index += 1
    return is_nine


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    substr = string[-2:]
    output = 0
    for i in range(len(string[:-2])):
        if (string[i:i + 2] == substr):
            output += 1

    return output


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    output = []
    for word in array:
        output.append(len(word))
    return output

#write fizbuzz programm
def fizbuzz():
    return

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    number_toString = str(number)
    output = []
    for i in range(len(number_toString)):
        output.append(int(number_toString[i]))
    return output

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    input = text.split(' ')
    output = ''

    first_word = True
    space = ' '
    for word in input:
        if first_word:
            word = "".join(c.upper() if i == 1 else c for i, c in enumerate(word))
            first_word = False
        if word == input[-1]:
            space = ''
        first = word[0].lower()
        word_pig = word[1::] + first + 'ay'
        output += word_pig + space
    return output

#Write a proramm that returna dictionary of occurences of the alphabet for a given string.
# Test it with the Lorem upsuj
#"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
def occurences(text):
    output = dict()
    letters = list(text)
    for letter in letters:
        if letter not in output.keys():
            output[letter] = 0
        output[letter] += 1
    return output

# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):
    fizbuzz()
    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )

    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello','toto']) , [5,4])
        self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849) , [8,8,4,9])
        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")



def main():
    unittest.main()

if __name__ == '__main__':
    main()