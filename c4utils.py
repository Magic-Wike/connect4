import sys
import os

y_responses = ['y', 'yes', 'ya', 'yup', 'send it', 'hit me']
n_responses = ['n', 'no', 'nope', 'nah']
quit_commands = ['quit', 'exit', 'x', 'bye']
user_commands = {}
userOS = str(sys.platform)

welcome = '''----------------------------------------------------------
Welcome! Thank you for playing....
   _____ ____  _   _ _   _ ______ _____ _______   _  _   
  / ____/ __ \| \ | | \ | |  ____/ ____|__   __| | || |  
 | |   | |  | |  \| |  \| | |__ | |       | |    | || |_ 
 | |   | |  | | . ` | . ` |  __|| |       | |    |__   _|
 | |___| |__| | |\  | |\  | |___| |____   | |       | |  
  \_____\____/|_| \_|_| \_|______\_____|  |_|       |_|  

                      a mediocre python game by Magic-Wike
----------------------------------------------------------'''

# utility functions, input handling 

# clear screen 
def clearFunc():
  if "win32" not in userOS:
    os.system('clear')
  else:
    os.system('cls')

def clean_input(string):
    cleaned = string.strip().lower()
    return cleaned 

def killswitch():
    print("\n\n\n\nGoobye!\n\n\n\n")
    quit()

# def print_user_commands():
#     print("\n")
#     for k, v in user_commands.items():
#         print("{}: {}".format(k, v))   

# def command_parse(user_input):
#    user_input.strip()
#    try:
#       user_input.lower()
#    except ValueError:
#       pass
#    if user_input in quit_commands:
#       killswitch()
#    elif type(raw_input) == int:
#       return raw_input
#    elif "What is your name?" in user_input:
#       if raw_input == "":
#             print("\nPlease enter a name!")
#             continue
#       elif raw_input.isalpha() == False:
#             print("\nPlease use letters only")
#             continue
#       else:
#             return raw_input
#    cleaned = raw_input.strip().lower()
#    if cleaned in ["chips", "ch"]:
#       try:
#             print("You have {} chips.".format(player1.chip_count))
#             continue
#       except NameError:
#             print("Player does not exist. (start a game first)")
#             continue
#    elif cleaned in ["commands", "cmd"]:
#             print_user_commands()
#             continue
#    elif cleaned in hand_commands:
#       return cleaned
#    elif cleaned in y_responses:
#       return "y"
#    elif cleaned in n_responses:
#       return "n"
#    else: 
#       print("Invalid input")
#       continue
