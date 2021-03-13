"""Assemble a Brainfuck function to create a given string

Optionally, the function may take user input."""

__author__ = "Tamzin Hadasa Kelly"
__copyright__ = "Copyright 2021, Tamzin Hadasa Kelly"
__license__ = "The MIT License"

import brainfuck
import re


def createbf(text):
    """Creates brainfuck function that will output `text`.

    Arg:
      text: A str of ASCII characters.

    Returns:
      A str that can compile into valid brainfuck.
    """
    ords = [ord(c) for c in text if c != "$"]
    try:
        # Tells us where to stop normal printing and instead copy input
        inp_idx = text.index("$")
    except ValueError:
        inp_idx = None
    bf = f"""
    ++++    c0 = 4
    [
        -    4 loops
        >++++    Multiply c1 by 8
        ++++
        <
    ]    Ends at c0 = 0; c1 = 32
    >    c1
    [
        -    32 loops
        >+    Set c2 to 32
        {"".join(">" + "+"*(round(n/16) // 2) for n in ords)}    Increment in multiples of 32
        {"<" * (1+len(ords))}
    ]    Ends at c1 = 0; c2 = 32; rest variable
    >    c2
    [
        --    16 loops 
        {"".join(">" + "+"*(round(n/16) % 2) for n in ords)}    Increment in multiples of 16
        {"<"*len(ords)}
    ]
    """
    for idx, n in enumerate(ords):
        bf += f">{plusminus(n - round(n/16)*16)}."
        # Check here in case $ is final character.
        if inp_idx is not None and idx + 1 == inp_idx:
            # brainfuck.py treats EOF as -1
            bf += ",+[-.[-],+]    Copy input and print back out"
    bf = re.sub("[^][<>+-.,#]", "", bf)   # Remove comments and whitespace
    return bf


def plusminus(n):
    """Get a number of +s or -s corresponding to n's value.

    If n == 0, returns "".
    
    Arg:
      n: An int
    
    Returns:
      A str, possibly empty.
    """
    return ("-", "+")[n > 0] * abs(n)


while True:
    text = input("Assemble brainfuck. ($) for single line of user input: ")
    bf = createbf(text)
    print(bf)
    bf_func = brainfuck.to_function(bf)
    if "," in bf:
        ask = input("Input for brainfuck function: ")
        print(bf_func(ask))
    else:
        print(bf_func())