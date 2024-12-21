#!/usr/bin/python3

import sys

FLAG="SIG24{BrUt3_m3_t1LL_U_Gu355_m3}"

user_input = input("Guess the flag:")
counter = 0

if len(user_input) == len(FLAG):
  print("Just the right length :)")
  for i in range(len(user_input)):
    if ord(user_input[i]) == ord(FLAG[counter]):
      counter+= 1
      print("Character "+str(i)+" is on target. Moving to next character :)")
    elif ord(user_input[i]) > ord(FLAG[counter]):
      print("Character "+str(i)+" is too high. Try again :)")
      break
    elif ord(user_input[I]) < ord(FLAG[counter]):
      print("Character "+str(i)+" is too low. Try again :)")
      break
elif len(user_input) > len(FLAG):
  print("Submitted input is TOO LONG. Try again :)")

elif len(user_input) < len(FLAG):
  print("Submitted input is TOO SHORT. Try again :)")

if user_input == FLAG:
  print("Well done in solving it :)")
  sys.exit(0)