import sys


# scanner
def validate_lexemes():
    global sentence
    for lexeme in sentence:
        if not valid_lexeme(lexeme):
            return False
    return True


def valid_lexeme(lexeme):
    return lexeme in ["function", "math", "loop", "add", "sub", "multi", "divide", "mod", "for", "while", "if",
                      "var1", "var2", "var3", "var4", "func1", "func2", "func3", "1", "2", "3", "4", "5",
                      "6", "7", "8", "9", "0", ">", "<", ">=", "<=", "="]


def depth_print():
    for i in range(0, depth):
        print("\t", end="")


def get_next_lexeme():
    global lexeme
    global lexeme_index
    global sentence
    global num_lexemes
    global error

    lexeme_index = lexeme_index + 1
    if lexeme_index < num_lexemes:
        lexeme = sentence[lexeme_index]
    else:
        lexeme = " "


def get_previous_lexeme():
    return sentence[lexeme_index - 1]


# <expr> := <first> | <first> <expr>
def expr():
    global lexeme
    global lexeme_index
    global num_lexemes
    global error
    first()
    if not error and lexeme in ["function", "loop", "math"]:
        expr()


# <first> := <function> | <loop> | <math>
def first():
    global lexeme
    global error
    global depth
    # Do we have a one?

    if lexeme == "function":
        depth = 0
        print("def ", end="")
        function()
        depth += 1
    elif lexeme == "loop":
        loop()
    elif lexeme == "math":
        math()
    else:
        error = True


# <function> := <funcName> <accVars>
def function():
    global lexeme
    global error
    # Do we have a one?
    get_next_lexeme()
    if lexeme in ["func1", "func2", "func3"]:
        print(lexeme + "(", end="")
        get_next_lexeme()
        acc_vars()
        print("): ")
    else:
        error = True


# <accVars> := var | var <accVars>
def acc_vars():
    global lexeme
    global error
    # Do we have a one?
    if lexeme in ["var1", "var2", "var3", "var4"]:
        depth_print()
        print(lexeme + ", ", end="")
        get_next_lexeme()
        acc_vars()
    elif get_previous_lexeme() not in ["var1", "var2", "var3", "var4"]:
        error = True


# <loop> := <loopType> <constraints>
def loop():
    global lexeme
    global error
    global depth
    # Do we have a one?
    get_next_lexeme()
    isIf = lexeme == "if"
    if lexeme in ["for", "while", "if"]:
        depth_print()
        print(lexeme, end="")
        constraints(isIf)
        print(": ")
        depth += 1
        get_next_lexeme()


# <constraints> := <input> <compare> <input>
def constraints(is_if):
    global lexeme
    global error
    # Do we have a one?
    get_next_lexeme()
    firstVar = lexeme
    input_function()
    get_next_lexeme()
    if lexeme not in ["<", ">", "<=", ">="]:
        error = True
    sign = lexeme
    get_next_lexeme()
    secondVar = lexeme
    input_function()
    if not is_if:
        if sign == "<":
            print(" i in range(" + firstVar + ", " + secondVar + ")", end="")
        elif sign == "<=":
            print(" i in range(" + firstVar + ", " + secondVar + " + 1)", end="")
        elif sign == ">":
            print(" i in range(" + firstVar + ", " + secondVar + ", -1)", end="")
        elif sign == ">=":
            print(" i in range(" + firstVar + ", " + secondVar + " + 1, -1)", end="")
    else:
        print(" " + firstVar + " " + sign + " " + secondVar, end="")



def input_function():
    global lexeme
    global error

    if lexeme not in [str(x) for x in range(0, 10)] and lexeme not in ["var1", "var2", "var3", "var4"]:
        error = True


# <math> := <mathType> <input> <input> (| <mathType> <input> <input> <input>)
def math():
    global lexeme
    global error
    get_next_lexeme()
    convert = {"add": "+", "sub": "-", "multi": "*", "divide": "/", "mod": "%"}
    sign = convert[lexeme]
    third = False
    if lexeme in ["add", "sub", "multi", "divide", "mod"]:
        get_next_lexeme()
        firstVal = lexeme
        input_function()
        get_next_lexeme()
        secondVal = lexeme
        input_function()
        thirdVal = ""
        if get_next_lexeme() is not None:
            third = True
            get_next_lexeme()
            thirdVal = lexeme
            input_function()
        depth_print()
        if third:
            print(firstVal + " = " + secondVal + " " + sign + " " + thirdVal)
        else:
            print("var0" + " = " + firstVal + " " + sign + " " + secondVal)
    else:
        error = True


# main program
# read in the input sentence`
#
# ces
for line in sys.stdin:
    line = line[:-1]  # remove trailing newline
    sentence = line.split()
    print(sentence)

    num_lexemes = len(sentence)

    lexeme_index = -1
    error = False
    depth = 0

    if validate_lexemes():
        get_next_lexeme()
        print("var1 = var2 = var3 = var4 = 0")

        expr()

        # Either an error occurred or
        # the input sentence is not entirely parsed.
        # or lexeme_index < num_lexemes - 1
        if error:
            print('"{}" is not a sentence.'.format(line))
        else:
            print('"{}" is a sentence.'.format(line))
    else:
        print('"{}" contains invalid lexemes and, thus, ''is not a sentence.'.format(line))
