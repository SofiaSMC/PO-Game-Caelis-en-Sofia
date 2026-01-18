# PIG: Multi-player game

# define rolling the dice
'''def: define, used to make recurring statements that can be used throughout the code'''
import random

def roll():
   min_value = 1
   max_value = 6
   roll = random.randint(min_value, max_value)
   
   return roll

# amount of players
while True:
   players = input("enter the amout of players (2-4): ")
   if players.isdigit():
      players = int(players)
      if 2 <= players <= 4:
         break
      else:
         print("must be between 2 and 4 players")
   else:
      print("Invalid, try again.")

# look if there is a winner
max_score = 150
player_scores = [0 for _ in range(players)] #list comprehension. puts a 0 in the list for all players (= start score). '_' is the variable.

# rolling function
while max(player_scores) < max_score:

   for player_index in range(players):
      print("\nplayer", player_index + 1,  "turn has just started.\n" )

      print(f"your total score = {player_scores[player_index]} \n")
      current_score = 0

      #simulate the turn
      while True:
         should_roll = input("Do you want to roll (y)?: ")
         if should_roll.lower() != "y":
            break

         value = roll()
         if value == 1:
            print("You rolled a 1! Your turn is over.")
            current_score = 0
            break #quite important to add, do not forget to break the loop, otherwise the turn won't end with rolling a 1!
         else: 
            current_score += value
            print(f"you rolled a {value}!")
         
         print(f"Your score is: {current_score} ")

      player_scores[player_index] += current_score
      print(f"Your total score is: {player_scores[player_index]}")

max_score = max(player_scores)
winner_index = player_scores.index(max_score)

print(f"player {winner_index + 1} is the winner with a score of: {max_score}")
