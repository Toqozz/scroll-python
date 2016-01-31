#!/usr/bin/env python

from time import sleep #Import the sleep function, which allows us to delay prints to stdout.
import argparse #For parsing arguments easily.
import sys #For reading stdin and also using sys.exit to break the program.

#Parser
parser = argparse.ArgumentParser(description='Scrolls input text via stdin or file to a stdout or fifo -- use with a bar, or a notifictaion daeemon like statnot')
parser.add_argument('-i', '--input', help='Input text, you can also pipe input to scroll.py, which will be taken over any text in -i', type=str, required=False, metavar='TEXT')
parser.add_argument('-c', '--characters', help='Number of characters to display at a time (this includes blank characters) - default: 20', type=int, required=False, metavar='INT')
parser.add_argument('-s', '--spaces', help='The character to use for the spaces (will only use the first character!)', type=str, required=False, metavar='CHAR')
parser.add_argument('-t', '--time', help='The time interval between a scroll it seconds -- how long it takes for the next frame of text to display - default: 0.5', type=float, required=False, metavar='FLOAT')
parser.add_argument('-n', '--newline', help='Put each string on a new line, for piping to a bar or similar', required=False, action='store_true')
parser.add_argument('-b', '--beginning', help='Character (or string) to put at the beginning of each line, to help with searching for strings to put in a bar', type=str, required=False, metavar='CHAR')
#Set some defaults so that our code does not break every time.
parser.set_defaults(input='placeholder', characters=20, spaces=' ', time=0.5, action=False, beginning='')
args = parser.parse_args()

def scroll():
    #Definitions
    #For str, we need to check if the user has piped anything through stdin, if not we can resort to the -i value.
    str = sys.stdin.read().strip() if not sys.stdin.isatty() else args.input.strip() #Strings to hold the actual offset character.
    characters = args.characters #The number of charactrs to print at a single time.
    spaces = args.spaces[0]      #The space character to use, make sure to only select the first one and prevent errors.
    time = args.time             #The time interval between scrolls.
    newline = args.newline       #Carriage return or newline?
    beginning = args.beginning   #Character to place at the beginning of each line (use with -n).
    str2 = ''                    #An additional string to work with [str]
    final = ''                   #A final string to keep track of the characters that are being printed.
    t = True                     #Boolean using in check for starting character.

    #We add spaces to the front of the string to make it 'scroll' in from the right.
    # '-' is used in the comment examples so that it is more readable.
    for i in range(0, characters-1):
        str2 = str2 + spaces

    #Create the string '--------hello--------'
    str = str2 + str
    str = str + str2

    for i in range(0, len(str)):
        #If the begining of the 'string' at this current point is equal to '--', do nothing
        #This is to keep from printing all of the spacing at the start of the strings.
        #For example, this makes '------h' the first printed string, rather than '-'.
        if str[i] == spaces and t == True:
            pass
        #If the above is not the case, print [final(which is '-----h' at first)], with the additon of the character on the end
        #Sleep for [time] after printing the string
        #We dont need to check for non-blank characters after the first part of the string has
        #been identified, so make t == False!!
        elif newline == True: #Check newline option.
            sys.stdout.write('\n' + beginning + final + str[i]) #Newline before so we dont run into weird stuff with multiple things writing to the same fifo.
            sys.stdout.flush() #Flush every time to stop python from buffering the stdout file -- 'real' stdout.
            sleep(time)
            t = False
        else:
            sys.stdout.write(final + str[i] + '\r')
            sys.stdout.flush()
            sleep(time)
            t = False

        #We make final == to final, plus the additional string character.  In the end, this will
        #end up being the whole string, including all the blank characters beforehand
        final = final + str[i]
        #If the length of final is equal to the maximum number of characters, cut off the first
        #character
        if len(final) > characters-1:
            final = final[1:]

        #Increment i, this is basically the cursor position in the string.

    #End on a new line.
    sys.stdout.write('\n ')
    sys.stdout.flush()

if __name__ == '__main__':
    scroll()
