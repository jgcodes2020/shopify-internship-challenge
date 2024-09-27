import sys
from io import StringIO

# Braille "opcodes" (special characters)
OP_CAPITAL = 0
OP_NUMBER  = 1
# Lookup opcode to braille
OP_BRAILLE_TABLE = {
    OP_CAPITAL: ".....O",
    OP_NUMBER: ".O.OOO",
}
# Reverse lookup: braille to opcode
BRAILLE_OP_TABLE = {v: k for k, v in OP_BRAILLE_TABLE.items()}

# Lookup letter to braille
ALPHA_BRAILLE_TABLE = {
    'a': "O.....",
    'b': "O.O...",
    'c': "OO....",
    'd': "OO.O..",
    'e': "O..O..",
    'f': "OOO...",
    'g': "OOOO..",
    'h': "O.OO..",
    'i': ".OO...",
    'j': ".OOO..",
    'k': "O...O.",
    'l': "O.O.O.",
    'm': "OO..O.",
    'n': "OO.OO.",
    'o': "O..OO.",
    'p': "OOO.O.",
    'q': "OOOOO.",
    'r': "O.OOO.",
    's': ".OO.O.",
    't': ".OOOO.",
    'u': "O...OO",
    'v': "O.O.OO",
    'w': ".OOO.O",
    'x': "OO..OO",
    'y': "OO.OOO",
    'z': "O..OOO",
}
# reverse lookup: braille to letter
BRAILLE_ALPHA_TABLE = {v: k for k, v in ALPHA_BRAILLE_TABLE.items()}

# Lookup number to braille
NUM_BRAILLE_TABLE = {
    '1': "O.....",
    '2': "O.O...",
    '3': "OO....",
    '4': "OO.O..",
    '5': "O..O..",
    '6': "OOO...",
    '7': "OOOO..",
    '8': "O.OO..",
    '9': ".OO...",
    '0': ".OOO..",
}
# reverse lookup: braille to number
BRAILLE_NUM_TABLE = {v: k for k, v in NUM_BRAILLE_TABLE.items()}

# Lookup symbol to braille
SYMBOL_BRAILLE_TABLE = {
    '.': "..OO.O",
    ',': "..O...",
    '?': "..O.OO",
    '!': "..OOO.",
    ':': "..OO..",
    ';': "..O.O.",
    '-': "....OO",
    '/': ".O..O.",
    '<': ".OO..O",
    '>': "O..OO.",
    '(': "O.O..O",
    ')': ".O.OO.",
}
# reverse lookup: braille to symbol
BRAILLE_SYMBOL_TABLE = {v: k for k, v in SYMBOL_BRAILLE_TABLE.items()}

BRAILLE_SPACE = "......"

def decode_braille(input: str) -> str:
    # 
    out_buf = StringIO()

    # loop over every 6 characters
    for i in range(0, len(input), 6):
        pass

    return ""

def encode_braille(input: str) -> str:
    number_mode = False

    with StringIO() as out_buf:
        for char in input:
            # number mode is set after the first digit is written.
            if number_mode:
                # numbers must always be terminated by space, otherwise it can't be safely encoded.
                # this doesn't handle decimal points at the moment. parsing it requires lookahead, which can't
                # be handled by the loop we're using at the moment.
                if char == ' ':
                    out_buf.write(BRAILLE_SPACE)
                    number_mode = False
                elif char.isdigit():
                    out_buf.write(NUM_BRAILLE_TABLE[char])
                else:
                    raise ValueError("Number without trailing space cannot be encoded into Braille!")
            elif char == ' ':
                out_buf.write(BRAILLE_SPACE)
            elif char.isalpha():
                # it's an alphabetical character. Uppercase must be preceded by the "capital" character
                if char.isupper():
                    out_buf.write(OP_BRAILLE_TABLE[OP_CAPITAL])
                out_buf.write(ALPHA_BRAILLE_TABLE[char.lower()])
            elif char.isdigit():
                # Initiate number mode.
                out_buf.write(OP_BRAILLE_TABLE[OP_NUMBER])
                out_buf.write(NUM_BRAILLE_TABLE[char])
                number_mode = True
            else:
                # We only have encodings for a select set of symbols.
                output = SYMBOL_BRAILLE_TABLE.get(char)
                if output is None:
                    raise ValueError(f"Character '{char}' cannot be encoded into Braille!")
                out_buf.write(output)

        return out_buf.getvalue()



# Assume one space between each argument
input_str = " ".join(sys.argv[1:])

print(encode_braille(input_str))