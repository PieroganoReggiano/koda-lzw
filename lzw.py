#!/usr/bin/python3

import sys
import argparse
import math


verbosity = 0


def compress(input_file, output_file):
    the_input = None
    the_output = None
    if input_file == '-':
        the_input = sys.stdin.buffer
    elif input_file == output_file:
        sys.stderr.write("Error: don't use same file as input and output")
        return -1
    else:
        the_input = open(input_file, "rb")

    if output_file == '-':
        the_output = sys.stdout.buffer
    else:
        the_output = open(output_file, "wb")


    code = 256
    dictionary = {}
    res = []
    symbol_count = 0

    for i in range(256):
        dictionary[i.to_bytes(1, byteorder='little', signed=False)] = i

    c = the_input.read(1)
    if c == None:
        return 0

    while True:
        s = the_input.read(1)
        if s:
            if c + s in dictionary:
                c += s
            else:
                res.append(dictionary[c])
                symbol_count += 1
                dictionary[c+s] = code
                code += 1
                c = s
        else:
            res.append(dictionary[c])
            break

    # przetworzenie wielkości słownika i wpisanie wszystkiego do pliku
    index_length = (code-1).bit_length()

    if verbosity >= 1:
        sys.stderr.write("Długość indexu: {}\nIlość symboli: {}\n".format(index_length, symbol_count))

    if verbosity >= 3:
        sys.stderr.write("Słownik:\n")
        for k,v in dictionary.items():
            sys.stderr.write("{:4d} -> {}\n".format(v, k))

    the_output.write(index_length.to_bytes(length=4, byteorder='little'))

    buffer = bytearray((index_length+7)//8)

    bufbit = 0
    for sign in res:
        for bit in range(index_length):
            if sign & (2**bit):
                buffer[bufbit//8] |= 2**(bufbit % 8)
            bufbit += 1
            if bufbit >= len(buffer)*8:
                the_output.write(buffer)
                buffer = bytearray((index_length+7)//8)
                bufbit = 0

    if bufbit > 0:
        buffer = buffer[0:((bufbit+7)//8)]
        the_output.write(buffer)

    return 0

def extract(input_file, output_file):
    the_input = None
    the_output = None
    if input_file == '-':
        the_input = sys.stdin.buffer
    elif input_file == output_file:
        sys.stderr.write("Error: don't use same file as input and output")
        return -1
    else:
        the_input = open(input_file, "rb")

    if output_file == '-':
        the_output = sys.stdout.buffer
    else:
        the_output = open(output_file, "wb")

    dictionary = {}
    for i in range(256):
        dictionary[i] = i.to_bytes(1, byteorder='little', signed=False)

    code = 256
    symbol_count = 0

    index_size = the_input.read(4)
    if not index_size or len(index_size) != 4:
        raise Exception("Could not read index size")

    index_size = int.from_bytes(bytes=index_size, byteorder='little', signed=False)

    if verbosity >= 1:
        sys.stderr.write("Index size: {}\n".format(index_size))

    index_old = -1 # -1, więc mamy do odczytania pierwszy index, który jest trochę inaczej
    index = 0
    indexbit = 0
    bufbit = 0
    buffer = the_input.read(1)
    while True:
        if verbosity >= 4:
            sys.stderr.write("Bit reading indexbit={}, bufbit={}".format(indexbit, bufbit))
        if buffer[0] & (2**bufbit):
            index |= (2**indexbit)
            if verbosity >= 4:
                sys.stderr.write(" 1")
        elif verbosity >= 4:
            sys.stderr.write(" 0")
        indexbit += 1
        bufbit += 1
        if indexbit >= index_size:
            if verbosity >= 4:
                sys.stderr.write(" index={}".format(index))

            #######

            if index_old < 0: # odczytano dopiero pierwszy index
                if verbosity >= 4:
                    sys.stderr.write(" first")
                index_old = index
                the_output.write(dictionary[index])
            else: # tu już normalnie
                text_old = dictionary[index_old]
                if index in dictionary:
                    if verbosity >= 4:
                        sys.stderr.write(" normal")
                    dictionary[code] = text_old + dictionary[index][0:1]
                    code += 1
                    the_output.write(dictionary[index])
                else: # sCsCs
                    if verbosity >= 4:
                        sys.stderr.write(" sCsCs")
                    dictionary[code] = text_old + text_old[0:1]
                    code += 1
                    the_output.write(text_old + text_old[0:1])
                index_old = index

            
            #######

            index = 0
            indexbit = 0
            symbol_count += 1
        if bufbit >= 8:
            if verbosity >= 4:
                sys.stderr.write(" byte")
                pass
            bufbit = 0
            buffer = the_input.read(1)
            if not buffer:
                sys.stderr.write("\n")
                break
        if verbosity >= 4:
            sys.stderr.write("\n")

    if verbosity >= 1:
        sys.stderr.write("Symbol count: {}\n".format(symbol_count))

    if verbosity >= 5:
        sys.stderr.write("Słownik:\n")
        for k,v in dictionary.items():
            sys.stderr.write("{:4d} -> {}\n".format(k, v))


    return 0

def entropy(input_file, block_size, condition_size):

    if block_size > 1 and condition_size > 0:
        raise Exception("Cannot use both block and conditional entropy at once")

    if condition_size > 3:
        raise Exception("Max condition entropy is 3")

    the_input = None
    if input_file == '-':
        the_input = sys.stdin.buffer
    else:
        the_input = open(input_file, "rb")

    entropy = 0.0

    if condition_size <= 0:
        occurrences = {}
        allc = 0
        while True:
            chunk = the_input.read(block_size)
            if chunk:
                if chunk in occurrences:
                    occurrences[chunk] += 1
                else:
                    occurrences[chunk] = 1
                allc += 1
            else:
                break

        for k,v in occurrences.items():
            p = v/allc
            one_entropy = -p * math.log2(p)
            entropy += one_entropy
            if verbosity >= 2:
                sys.stderr.write("Symbol: {}, probability: {}, entropy: {}\n".format(k, p, one_entropy))
    else:
        context = b''
        occurrences = {}
        allc = 0
        while True:
            chunk = the_input.read(1)
            if chunk:
                if context in occurrences:
                    occurrences[context]["count"] += 1
                else:
                    occurrences[context] = { "count": 1, "occurrences": {} }
                if chunk in occurrences[context]["occurrences"]:
                    occurrences[context]["occurrences"][chunk] += 1
                else:
                    occurrences[context]["occurrences"][chunk] = 1
                allc += 1
                context = context + chunk
                context = context[-condition_size:]
            else:
                break

        for k,v in occurrences.items():
            sum = 0.0
            for kk,vv in v["occurrences"].items():
                p = vv/v["count"]
                sum -= p * math.log2(p)
            p = v["count"]/allc
            entropy += p * sum

    #print(entropy)
    nb_symbols = len(occurrences.keys())
    return entropy, nb_symbols

        



def main():

    parser = argparse.ArgumentParser(description="LZW compression and decompression")
    parser.add_argument('input', metavar='input-file', type=str, help="Path to input file or - for stdin")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--compress', '-c', action='store', metavar="output-file", type=str, help="Compress input to file")
    group.add_argument('--extract', '-x', action='store', metavar="output-file", type=str, help="Decompress input to file")
    group.add_argument('--entropy', '-e', action='store_true', help="Calculate entropy")

    parser.add_argument('--verbose', '-v', action='count', default=0)

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--block-size', '-s', action='store', metavar="block-size", type=int, default=1, help="Set size of block entropy")
    group2.add_argument('--condition-degree', '-C', action='store', metavar="degree", type=int, default=0, help="Set deegree of conditional entropy")

    args = parser.parse_args()

    global verbosity
    verbosity = args.verbose


    if args.compress:
        if verbosity >= 1:
            sys.stderr.write("Compression of '{}' to '{}'\n".format(args.input, args.compress))
        return compress(args.input, args.compress)
    elif args.extract:
        if verbosity >= 1:
            sys.stderr.write("Decompression of '{}' to '{}'\n".format(args.input, args.extract))
        return extract(args.input, args.extract)
    elif args.entropy:
        if verbosity >= 1:
            sys.stderr.write("Calculation of entropy{}\n".format(
                "" if args.block_size <=1 and args.condition_degree <= 0 else
                " with block of size {}".format(args.block_size) if args.block_size > 1 else
                " with condition {}".format(args.condition_degree)
            ))
        return entropy(args.input, args.block_size, args.condition_degree)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
