"""
Module contains a version of Wordle that uses the Python Shell to play
Author: Oliver Clark
Date: 16th December 2022
"""

import random
import enchant

class Wordle:
    """Main class, ca`lls itself automaticlly to start the game"""
    def __init__(self):
        """
        Calls the get_word() function and splits the word into a list 
        for later. contains other variables that are global to other functions.
        """
        self.word_str, self.list_of_words = self.get_word()
        #print(self.word_str)
        self.word_list = [i for i in self.word_str]
        self.trys_remaining = 6
        self.word_attempts_split = [[],
                              [],
                              [],
                              [],
                              [],
                              []]
        self.list_of_keys = [
            'q','w','e','r','t','y','u','i','o','p',
            'a','s','d','f','g','h','j','k','l','z',
            'x','c','v','b','n','m'
        ]
        self.keyboard = {letter: '_' for letter in self.list_of_keys}        
        self.word_attempt_fill = 0
        self.won = False
        self.introduction()
        
    def get_word(self):
        """Gets the word using a randomly generated word and a txt file"""
        random_int = random.randint(0,483)
        list_of_words = open("words.txt").readlines()
        list_of_words = [i[0:5] for i in list_of_words]
        return list_of_words[random_int], list_of_words    

    def introduction(self):
        """Introduction message including rules and how to play the game"""
        print(20*"-")
        get_help = input("type 'help' for instuctions on how to play this" 
        " version of WORDLE: ")
        print(20*"-")        
        if get_help == "help":
            self.instructions() 
                
        print(4*" ", "|WORDLE|")
        print(20*"-")
        self.display_words()
        self.play()
     
    def instructions(self):
        """Prints the instructions for the player"""
        print(20*"-")
        print("You get six attempts in getting the word.")
        print(20*"-")
        print("To enter the word, just type the word.")
        print(20*"-")        
        print("If a letter is in the correct place, it will be in uppercase.")
        print("If a letter is in the word but in the wrong place, it will be "
              "incased in '||'.")
        print("If a letter is lower case, it isn't in the word at all.")
        print(20*"-")
        exit = input("type anything to exit: ")
        print(20*"-")

    def play(self):
        """Main function what plays the game"""
        while self.trys_remaining > 0 and self.won == False:
            print(f"You have {self.trys_remaining} trys remaining")
            print(20*"-")
            self.display_keyboard()            
            valid = False
            while not valid:
                self.word_attempt = input("Enter your word: ")
                print(20*"-")                
                valid = self.check_valid(self.word_attempt.lower())
            self.trys_remaining -= 1
            self.process_word(self.word_attempt.lower())
        if self.won == False:
            print(f"GAME OVER! THE WORD WAS '{self.word_str.upper()}'")
            print(20*"-")   
                
    def check_valid(self, word):
        """Checks if the word is valid"""
        if len(word) != 5:
            print("WORD MUST BE 5 LETTERS ONLY")
            print(20*"-")
            return False
        dictionary = enchant.Dict("en_US")
        if dictionary.check(word) == False:
            print("WORD MUST BE IN ENGLISH")
            print(20*"-") 
            return False
        return True
           
    def process_word(self, word_attempt):
        """Prints the word to give the player information about their attempt"""
        win_count = 0
        word_attempt_list = [i for i in word_attempt]#splits the word into a list
        word_to_print = [] #appened over the for loop
        for slot in range(5):
            if word_attempt_list[slot] == self.word_list[slot]: #green
                word_to_print.append([word_attempt_list[slot].upper()])
                win_count += 1
            elif word_attempt_list[slot] in self.word_str: #orange, this is checked later in self.check_orange()
                word_to_print.append([f"|{word_attempt_list[slot]}|"])
            else: #gray
                word_to_print.append([word_attempt_list[slot]])
        word_to_print = self.check_orange(word_to_print)
        self.add_to_keyboard(word_to_print)
        if win_count == 5: #the game is won
            self.add_entry(word_to_print)            
            self.win_game()
        else: #continue the game as usual
            self.add_entry(word_to_print)
            self.display_words()
            
    def check_orange(self, word_list):
        """
        Checks if a letter should be 'orange' because self.process_word takes
        a naive approach.
        Firstly, the function determinds if the word and guess is two-lettered
        or not and gets the letters that are two lettered.
        Secondly, it goes through the letters that are two lettered and determinds
        if there is an orange and green letter that is the same of the two 
        lettered word. 
        Thirdly, it determinds if that requirement is met OR if the two letter
        lists are not equal and changes the letter from orange to gray and 
        returns words_list to be used in self.process_word().
        This function avoids a case there two letter guesses make it look like
        the word may be two-lettered when it is is only one-lettered. 
        For example, if the word is 'hopes' and the guess is 'happy', the second 
        'p' in happy should be gray but without this function it is orange. This
        confuses the player.
        """
        is_two_letter_word, two_letter_word_list = self.check_two_letter_word()#word
        is_two_letter_guess, two_letter_guess_list = self.check_two_letter_guess(two_letter_word_list)#guess
        confirm = 0
        if is_two_letter_guess and not is_two_letter_word:
            for double_letter in two_letter_guess_list:
                for letter_list in word_list:
                    letter_guess = letter_list[0]
                    if "|" in letter_guess and double_letter in letter_guess: #is orange and same letter
                        confirm += 1
                    if letter_guess.isupper() and letter_guess.lower() == double_letter:#is green and same letter
                        confirm += 1
        if confirm == 2 or two_letter_guess_list != two_letter_word_list:#might need to be looked at. may be temp fix for aural and rural
            for double_letter in two_letter_guess_list:
                for i in range(5):
                    if "|" in word_list[i][0] and double_letter in word_list[i][0]:
                        word_list[i] = [f"{double_letter}"]# changes the letter in place
        return word_list
    
    def add_to_keyboard(self, word_list):
        """
        Adds the entered letters into a something so it can prints the players 
        entered letters so the player can see what letters they have entered 
        """
        for letter_list in word_list:
            letter = letter_list[0]
            if '|' in letter: #filter oranges from grays and greens
                if self.keyboard[letter[1]] == '_':
                    self.keyboard[letter[1]] = f"|{letter[1]}|"
            else:
                if letter.isupper() and self.keyboard[letter.lower()] == '_': #green and new letter
                    self.keyboard[letter.lower()] = letter
                elif letter.isupper() and self.keyboard[letter.lower()] == f'|{letter.lower()}|': #green and was orange
                    self.keyboard[letter.lower()] = letter
                elif letter.islower() and self.keyboard[letter] == '_':#new gray
                    self.keyboard[letter] = letter
                elif letter.islower() and self.keyboard[letter] == f'|{letter}|':
                    pass

    def check_two_letter_word(self):
        """Checks if the self.word_str is a two letter word"""
        is_two_letter = False
        two_letters = []
        count = 0
        for letter in self.word_str:
            for i in range(5):
                if letter == self.word_str[i]:
                    count += 1
            if count == 2 and letter not in two_letters: #avoids duplicates
                two_letters.append(letter)
                is_two_letter = True
            count = 0
        return is_two_letter, two_letters
    
    def check_two_letter_guess(self, two_letter_word_list):
        """
        checks if the guess has two letters in it that are the same. 
        and returns the list that only appear in the word
        """
        is_two_letter = False
        two_letters = []
        count = 0
        for letter in self.word_attempt:
            for i in range(5):
                if letter == self.word_attempt[i]:
                    count += 1
            if count == 2 and letter not in two_letters:
                two_letters.append(letter)
                is_two_letter = True
            count = 0
        return is_two_letter, two_letters
            
    def add_entry(self, word_list):
        """Adds the entry to list of the words that have been guessed so far"""
        fill_slot = self.word_attempt_fill
        for letter in range(5):
            self.word_attempts_split[fill_slot].append(word_list[letter])
        self.word_attempt_fill += 1
            
    def display_words(self):
        """
        Prints all of the words that have been guessed so far and the other 
        attempts the player has left
        """
        for word_attempt in self.word_attempts_split:
            if len(word_attempt) != 0:
                print(word_attempt[0][0], word_attempt[1][0], 
                      word_attempt[2][0], word_attempt[3][0], 
                      word_attempt[4][0])
                print(20*"-")                
            else:
                print(5*"[] ")
                print(20*"-") 
    
    def display_keyboard(self):
        """Prints the keyboard"""
        board = self.keyboard
        keys = self.list_of_keys
        print("KEYS USED TO FAR:")
        print(board[keys[0]], board[keys[1]], board[keys[2]],board[keys[3]], 
        board[keys[4]], board[keys[5]],board[keys[6]], board[keys[7]], 
        board[keys[8]], board[keys[9]])
        print(1*'', board[keys[10]], board[keys[11]], board[keys[12]],board[keys[13]], 
        board[keys[14]], board[keys[15]],board[keys[16]], board[keys[17]], 
        board[keys[18]])
        print(2*' ', board[keys[19]], board[keys[20]], board[keys[21]],board[keys[22]], 
        board[keys[23]], board[keys[24]],board[keys[25]])
        print(20*"-")
            
    def win_game(self):
        """If the player guesses the word the game ends and displays a message"""
        [print("|") for i in range(7)] 
        print(20*"-")        
        self.display_words()
        print(f"CONGRATUATIONS! THE WORD IS '{self.word_str.upper()}' :)")
        print(20*"-")
        self.won = True
                      
Wordle()