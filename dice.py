#! /usr/bin/python3

import random, math

ops = ['d','<','>','+','-']

def print_help():
    """
    Prints the help menu
    """
    print("Usage: NdS [>|< N...] [+|- V...]")
    print("NdS \t\tAt minimum, a roll must be formatted like \'NdS\', where N is the number of dice to roll")
    print("\t\tand S is the number of sides on each. EX: 3d6 will roll 3 six-sided die.")
    print()
    print("[>|< N...]\tAny number of sorted dice rolls may be kept. EX:  >3 will keep the highest 3 dice ")
    print("\t\tand <2 will keep the lowest 2 dice. These may be chained, e.g. 5d6>4<3 will keep the highest")
    print("\t\t4 rolls, and of those rolls, the lowest 3.")
    print()
    print("[+|- V...]\tAdds or subtracts a value V to the final roll. EX: 3d6+2. These can be chained.")
    print()
    print("The formula MUST start with NdS, followed by selection mods, with scalar mods at the end. For example:")
    print("5d6<4>3+2-1+6 is valid. 5d6<4>3+2-1>6 is not.\n")
#######################################################################################################################

def validate(dice_string, ops_char_pos):
    """
    Checks whether the dice_string is a valid formula

    :param dice_string:     text reprepsenting the dice formula to be validated
    :param ops_char_pos:    list of indices at which Ops characters appear in dice_string
    :returns:               a boolean value indicating whether dice_string meets formatting requirements
    """
    # check if the NdS format is met
    if len(dice_string)<3:
        print("Error: dice string too short")
        return False
    if dice_string.find('d') == -1:
        print("Error: NdS format not found")
        return False

    # check that the first Ops character is a 'd'
    if not ops_char_pos[0] == dice_string.find('d'):
        print("Error: dice string does not begin with NdS format")
        return False
    # check that the first characters before the 'd' are numeric:
    if not dice_string[:ops_char_pos[0]].isdigit():
        print("Error: invalid number of dice")
        return False
    # check only digits exist after Ops characters
    for i in range(1, len(ops_char_pos)-1):
        substr = dice_string[(ops_char_pos[i]+1):ops_char_pos[i+1]]
        if not substr.isdigit():
            print("Error: Invalid character found in dice string, ", substr )
            return False
    # check that the final characters are digits
    if not dice_string[(ops_char_pos[-1]+1):].isdigit():
        print("Error: final segment not a valid number, ", dice_string[ops_char_pos[-1]:])
        return False
    return True
#######################################################################################################################

def roll(dice_string, ops_char_pos):
    """
    Isolates the die count and sides, then generates the appropriate rolls

    :param dice_string:     text reprepsenting the dice formula to be validated
    :param ops_char_pos:    list of indices at which Ops characters appear in dice_string
    :returns:               a sorted, size-N list of randomly generated integers between 1...S
    """
    num = int(dice_string[:ops_char_pos[0]])
    sides = 0
    if len(ops_char_pos) > 1:
        sides = int(dice_string[(ops_char_pos[0]+1):ops_char_pos[1]])
    else:
        sides = int(dice_string[(ops_char_pos[0]+1):])
    rolls = []
    for i in range(num):
        rolls.append(random.randint(1,sides))

    # remove the 'd' Op from the list
    del ops_char_pos[0]

    rolls.sort()
    return rolls
#######################################################################################################################

def selection_mods(rolls, dice_string, ops_char_pos):
    """
    Adjusts the die rolls by keeping a series of the highest or lowest values

    :rolls:                 a sorted, size-N list of randomly generated integers between 1...S
    :param dice_string:     text reprepsenting the dice formula to be validated
    :param ops_char_pos:    list of indices at which Ops characters appear in dice_string
    :returns:               a sorted and pruned size-N list of randomly generated integers between 1...S
    """
    # while there are selection ops left to perform...
    while len(ops_char_pos) > 0 and dice_string[ops_char_pos[0]] in ops[1:3]:
        selection_count = 0
        # split behavior depending on whether the current op is the last in the string
        if len(ops_char_pos) == 1:
            selection_count = int(dice_string[(ops_char_pos[0]+1):])
        else:
            selection_count = int(dice_string[(ops_char_pos[0]+1):ops_char_pos[1]])
        # select the highest n or lowest n rolls
        if dice_string[ops_char_pos[0]] == '<':
            rolls = rolls[:selection_count]
        elif dice_string[ops_char_pos[0]] == '>':
            rolls = rolls[(-1 * selection_count):]
        del ops_char_pos[0]

    return rolls
#######################################################################################################################

def scalar_mods(rolls, dice_string, ops_char_pos):
    """
    Sums the list of die rolls and then adds/subtracts a series of scalar adjustments

    :rolls:                 a sorted, size-N list of randomly generated integers between 1...S
    :param dice_string:     text reprepsenting the dice formula to be validated
    :param ops_char_pos:    list of indices at which Ops characters appear in dice_string
    :returns:               An integer which is the sum of the list of die rolls and any scalar adjustments
    """

    final = 0
    for r in rolls:
        final += r

    # while there are scalar ops left to perform...
    while len(ops_char_pos) > 0 and dice_string[ops_char_pos[0]] in ops[3:5]:
        value = 0
        # split behavior depending on whether the current op is the last in the string
        if len(ops_char_pos) == 1:
            value = int(dice_string[(ops_char_pos[0]+1):])
        else:
            value = int(dice_string[(ops_char_pos[0]+1):ops_char_pos[1]])

        if dice_string[ops_char_pos[0]] == '+':
            final += value
        elif dice_string[ops_char_pos[0]] == '-':
            final -= value
        del ops_char_pos[0]

    return final
#######################################################################################################################

def main():
    """
    CLI to collects and evaluates dice formulae from the user in a loop
    """
    valid_string = True;
    while valid_string:
        ops_char_pos = []
        print("enter your dice string. q to quit, h for help")
        dice_string = input().replace(' ', '');
        if dice_string == 'q':
            break;
        if dice_string == 'h':
            print_help()
            continue;
        
        # build a list of Ops character locations for parsing
        for i in range(len(dice_string)):
            if dice_string[i] in ops:
                ops_char_pos.append(i)
        valid_string = validate(dice_string, ops_char_pos)
        if not valid_string:
            break;

        rolls = roll(dice_string, ops_char_pos)
        print("You rolled: ", rolls)
        rolls = selection_mods(rolls, dice_string, ops_char_pos)
        print("After Selections: ", rolls)
        final = scalar_mods(rolls, dice_string, ops_char_pos)
        print("Your final roll: ", final)
#######################################################################################################################

main()
