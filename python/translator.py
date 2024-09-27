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

BRAILLE_SPACE = "......"

def decode_braille(input: str) -> str:
    '''
    Decodes a Braille string to English if possible; throwing an exception if not.

    :param input: The input Braille string.
    :returns: The Braille string, decoded into English.
    :raises ValueError: if the string cannot be decoded to English; e.g. because
        of an incomplete Braille cell, or invalid number codes.
    '''

    if len(input) % 6 != 0:
        raise ValueError("Last Braille cell is incomplete")

    is_capital = False
    is_number = False

    next_match = None

    with StringIO() as out_buf:
        # loop over every 6 characters
        for i in range(0, len(input), 6):
            cell = input[i:i+6]

            if (next_match := BRAILLE_OP_TABLE.get(cell)) is not None:
                # Match opcodes: special characters that affect subsequent characters
                if is_capital or is_number:
                    raise ValueError("Adjacent opcode cells disallowed in Braille")
                if next_match == OP_CAPITAL:
                    is_capital = True
                elif next_match == OP_NUMBER:
                    is_number = True
            # handle opcode modes
            elif is_capital:
                # capital opcode needs to be followed by a letter.
                if (next_match := BRAILLE_ALPHA_TABLE.get(cell)) is None:
                    raise ValueError("Unexpected non-letter cell following capital opcode")
                out_buf.write(next_match.upper())
                is_capital = False
            elif is_number:
                # spaces end number mode.
                if cell == BRAILLE_SPACE:
                    out_buf.write(' ')
                    is_number = False
                # otherwise it must be a number.
                elif (next_match := BRAILLE_NUM_TABLE.get(cell)) is not None:
                    out_buf.write(next_match)
                else: 
                    raise ValueError("Unexpected non-digit cell following number opcode")
            # Handle letters and symbols that can be encoded
            elif cell == BRAILLE_SPACE:
                out_buf.write(' ')
            elif (next_match := BRAILLE_ALPHA_TABLE.get(cell)) is not None:
                out_buf.write(next_match)
            # Otherwise it's invalid
            else:
                raise ValueError(f"Invalid Braille cell: {cell}")
            
        return out_buf.getvalue()

def encode_braille(input: str) -> str:
    '''
    Encodes an English string to Braille if possible; throwing an exception if not.

    :param input: The input English string.
    :returns: The English string, encoded into Braille.
    :raises ValueError: if the string cannot be encoded into Braille; i.e. it contains 
        symbols that cannot be encoded, or has a number not followed by a space.
    '''
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
                    raise ValueError("Number without trailing space cannot be encoded into Braille")
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
                raise ValueError(f"Character '{char}' cannot be encoded into Braille")

        return out_buf.getvalue()


def is_probably_braille(input: str) -> bool:
    '''
    Makes an educated guess as to whether a string is English or Braille.

    :param input: The input string, probably either English or Braille.
    :returns: `True` if the string is probably written in Braille, `False` otherwise.
    '''

    for char in input:
        if char not in ['.', 'O']:
            return False
        
    return True

# Assume one space between each argument
input_str = " ".join(sys.argv[1:])
output_str = None

if is_probably_braille(input_str):
    output_str = decode_braille(input_str)
else:
    output_str = encode_braille(input_str)

print(output_str)