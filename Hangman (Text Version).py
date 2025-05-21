"""✅ Q5 – Hangman (Text Version)
🕐 Estimated time: 45–60 mins
📚 Teaches: list vs str, game logic, loops, sets, input validation, reusable functions

❓Task:
Create a simple version of the Hangman game:

Store a secret word.

Show _ _ _ _ _ to the user.

User guesses a letter.

If correct → reveal all positions.

If wrong → count strikes.

End game when all letters are guessed or after 6 wrong tries.

🔑 Concepts:
list() and ''.join(list)

in and not in

Loops with conditionals

Sets for tracking guessed letters
l1 = " T"
l2 = " E"
l3 = " N"
l4 = " I"
l5 = " S"


Fix how you split the word and the blanks:

secret_word.split() splits on spaces, so for "TENIS" you get ["TENIS"], not ["T", "E", "N", "I", "S"].
"_____" as input to .split() gives you ["_____"].
Instead, use list(secret_word) and ["_"] * len(secret_word).
Use enumerate for looping through indexes and letters:

Instead of for i in range(6), use for i, letter in enumerate(letters):.
Reset got_letter at the correct place:

Make sure got_letter is set to False at the start of each guess, not outside the loop.
Correct the loop condition:

The while should be while not guessed and strikes > 0:.
Check if the word is guessed:

After updating hLetters, check if "".join(hLetters) equals secret_word to set guessed = True.
Remove unnecessary double input() and fix the except block:

Don’t use chr in input, and don’t prompt again inside the except; just continue the loop.
Use input validation for single alpha letters.

Check both length and .isalpha() if you want robust input.
No need to increment i yourself; let the loop do it.

Show the word progress in a user-friendly way:

Print " ".join(hLetters) to show separated blanks/letters.
Apply these ideas and your code will work much better!
Print (" ".join(hLetters))
"""


print("This is a hangman game!")
secret_word = "TENIS"
letters = []
letters = list(secret_word)
hidden_Letters = []
hidden_Letters = ["_"] * len(secret_word)
guessed = False
strikes = 6
while not guessed:
    if strikes >0 :
        got_letter = False
        i = 0
        try:
            active_letter = input("Guess a letter! :")
            if active_letter.isalpha() and len(active_letter) == 1:
        # This is a valid single letter
                active_letter = active_letter.upper()
                for i, letter in enumerate(letters):
                    if active_letter == letters[i]: #if i do a if active_letter in letters, i can't know which one of the letters he got but this also dones't work as the list index is out of range
                        print("You got one!")
                        hidden_Letters[i] = active_letter
                        print(hidden_Letters)
                        

                        if "".join(hidden_Letters) == secret_word:
                            print("You got the word!")
                            guessed = True #Ends the program

                        got_letter = True
                if got_letter == False:
                    print("Sorry, that letter is not in")
                    strikes = strikes -1
                    print(f"You have {strikes} strikes left")
                    print(hidden_Letters)
        except ValueError:
            print("That is not a letter")
    else:
        print("Sorry, you are out of strikes. You loose :(")
       