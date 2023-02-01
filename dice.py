#! /usr/bin/python3

import random, re

ops = {'die':'d', 'low':'<', 'high':'>', 'plus':'+', 'minus':'-'}
regex_string = r'''^(?P<dice>\d+{0}\d+)
        (?P<selects>([{1}{2}]\d+)*)
        (?P<scalars>([{3}{4}]\d+)*)$'''.format(ops['die'], ops['low'], ops['high'], ops['plus'], ops['minus'])
pattern = re.compile(regex_string, re.VERBOSE)

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

def validate(dice_string):
    """
    Checks whether the dice_string is a valid formula

    :param dice_string:     text reprepsenting the dice formula to be validated
    :returns:               a boolean value indicating whether dice_string meets formatting requirements
    """

    if pattern.match(dice_string) == None:
        print("Error: Invalid die formula")
        return False

    # Check if each successive selection mod is lower than the previous
    selections = re.search(pattern, dice_string).group('selects')
    # Get an array of selection counts, then make sure they descend
    vals = [int(i) for i in selections.replace('>','<').split('<')[1:]]
    for i in range(1, len(vals)-1):
        if vals[i] > vals[i-1]:
            print("Error: you cannot select more dice than you have (", selections, ")")
            return False

    return True
#######################################################################################################################

def roll(dice_string):
    """
    Isolates the die count and sides, then generates the appropriate rolls

    :param dice_string:     text reprepsenting the dice formula to be validated
    :returns:               a sorted, size-N list of randomly generated integers between 1...S
    """
    dice = re.search(pattern, dice_string).group('dice')
    num = int(dice.split(ops['die'])[0])
    sides = int(dice.split(ops['die'])[1])

    rolls = []
    for i in range(num):
        rolls.append(random.randint(1,sides))
    rolls.sort()

    return rolls
#######################################################################################################################

def selection_mods(rolls, dice_string):
    """
    Adjusts the die rolls by keeping a series of the highest or lowest values

    :rolls:                 a sorted, size-N list of randomly generated integers between 1...S
    :param dice_string:     text reprepsenting the dice formula to be validated
    :returns:               a sorted and pruned size-N list of randomly generated integers between 1...S
    """
    selections = re.search(pattern, dice_string).group('selects')
    mods = re.findall(r'([{0}{1}]\d+)'.format(ops['low'], ops['high']), selections)
    # ['>40', '<3', ...]
    for mod in mods:
        if mod[0] == ops['low']:
            rolls = rolls[0:int(mod[1:])]
        elif mod[0] == ops['high']:
            rolls = rolls[(-1 * int(mod[1:])):]
    
    return rolls
#######################################################################################################################

def scalar_mods(rolls, dice_string):
    """
    Sums the list of die rolls and then adds/subtracts a series of scalar adjustments

    :rolls:                 a sorted, size-N list of randomly generated integers between 1...S
    :param dice_string:     text reprepsenting the dice formula to be validated
    :returns:               An integer which is the sum of the list of die rolls and any scalar adjustments
    """
    scalars = re.search(pattern, dice_string).group('scalars')
    mods = re.findall(r'([{0}{1}]\d+)'.format(ops['plus'], ops['minus']), scalars)    

    final = 0
    for r in rolls:
        final += r
    for mod in mods:
        final += int(mod)

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
        
        valid_string = validate(dice_string)
        if not valid_string:
            break;

        rolls = roll(dice_string)
        print("You rolled: ", rolls)
        rolls = selection_mods(rolls, dice_string)
        print("After Selections: ", rolls)
        final = scalar_mods(rolls, dice_string)
        print("Your final roll: ", final)
#######################################################################################################################

main()
