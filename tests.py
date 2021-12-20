import glob
import os
import filecmp
from lzw import compress, extract, entropy
import matplotlib.pyplot as plt

def calculate_stopien_kompresji(original_size, compressed_size):
    result  = original_size/compressed_size
    print(f"Stopień kompresji: {result}")
    return result

def calculate_procent_kompresji(original_size, compressed_size):
    result = (original_size - compressed_size) / original_size
    print(f"Procent kompresji wynosi: {result}")
    return result

def calculate_entropy_zero_condition(file, block_size):
    result, nb_symbols = entropy(file, block_size, 0)
    print(f"Block size: {block_size}, Entropy: {result}")

    return result, nb_symbols

def calculate_przeplywnosc(compressed_size, nb_symbols):
    l = compressed_size / nb_symbols
    print("Przeplywnosc ", l)
    return l

def calculate_frequencies(file_name):
    content = bytearray(open(file_name, 'rb').read())

    freq, bins, patches = plt.hist(content, 256)
    plt.xlabel("Symbol")
    plt.ylabel("Frequency")
    plt.title(f'Bytes frequencies in {file_name}')
    plt.grid(True)
    out = file_name + "_frequency.png"
    plt.savefig(out)
    print(f"File saved in {out}")
    plt.clf()

if __name__ == "__main__":

    for file in glob.glob("data/*"):
        print(f"### Processing {file} ###")

        compressed = f"{file}_compressed.lzw"
        decompressed = f"{file}_decompressed.lzw"
        file_size = os.path.getsize(file)

        print(f"Compressing {file} of size {file_size} bytes")
        compress(file, compressed)
        compressed_size = os.path.getsize(compressed)

        print(f"Decompressing {compressed} of size {compressed_size} bytes")
        extract(compressed, decompressed)
        decompressed_size = os.path.getsize(decompressed)

        print("Checking if the decompressed file is the same as the input file")
        assert decompressed_size==file_size

        print("Checking if the decompressed file is the same as the original one")
        assert True == filecmp.cmp(file, decompressed)

        calculate_stopien_kompresji(file_size, compressed_size)
        
        calculate_procent_kompresji(file_size, compressed_size)

        print("Calculate entropy...")

        _, nb_symbols = calculate_entropy_zero_condition(file, 1)
        calculate_przeplywnosc(compressed_size, nb_symbols)

        _, nb_symbols = calculate_entropy_zero_condition(file, 2)
        calculate_przeplywnosc(compressed_size, nb_symbols)

        _, nb_symbols = calculate_entropy_zero_condition(file, 3)
        calculate_przeplywnosc(compressed_size, nb_symbols)


        print(f"Plotting histogram...")
        calculate_frequencies(file)
