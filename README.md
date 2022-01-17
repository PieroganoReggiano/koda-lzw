# Kompresor LZW

## Użycie:

``` sh
python3 lzw.py [opcje] <plik-wejściowy>
```

## Dostępne opcje

* `--compress|-c plik-wyjściowy` -- kompresja do podanego pliku
* `--extract|-x plik-wyjściowy` -- dekompresja do pliku
* `--entropy` -- obliczenie entropii i wypisanie na standardowe wyjście
* `--verbose` -- pokazywanie więcej informacji

### Opcje przy obliczaniu entropii

* `--block-size rozmiar` -- czytanie pliku w sposób taki, że podana ilość bajtów to jeden symbol
* `--condition-degree stopień` -- obliczenie entropii warunkowej podanego stopnia

Z powyższych dwóch opcji można użyć tylko jednej

## Szczegóły

Wynikowy plik jest w postaci binarnej w następujący sposób:
* Czterobajtowy nagłówek składający się z długości indeksu w bitach zapisany w little endian.
* Kolejne indeksy symboli zapisane na kolejnych bitach w kolejności little endian. Ostatni 'niedokończony' bajt jest wypełniony zerami.
* Zakładamy, że bajt ma 8 bitów.

## Jak wywołać testy

``` bash
./run_tests.sh
```

Skrypt **run_tests.sh** pobiera dane testowe, przeprowadza testy i obliczenia wymagane do przeprowadzenia analizy algorytmu:
- Stopien kompresji
- Procent kompresji
- Entropia
- Przepływność
- Generacja histogramu częstotliwości symboli w oryginalnych danych

Przykładowe logi: 

``` 
### Processing data/uniform.pgm ###
Compressing data/uniform.pgm of size 2097272 bytes
Przeplywnosc  11.042001228262238
Decompressing data/uniform.pgm_compressed.lzw of size 2894760 bytes

Checking if the decompressed file is the same as the input file
Checking if the decompressed file is the same as the original one
Stopień kompresji: 0.7245063494037502
Procent kompresji wynosi: -0.38025015353277974
Calculate entropy...
Block size: 1, Entropy: 7.9993194390339015
Block size: 2, Entropy: 7.793625609902205
Block size: 3, Entropy: 5.469917560141901
Plotting histogram...
File saved in data/uniform.pgm_frequency.png
```


# Generacja Danych
Dane generowane są bazowo o rozkładzie równomiernym o rozmiarze 1kB.

``` sh
python3 generateData.py -o <plik-wejściowy> [opcje]
```

## Dostępne opcje

* `-o --output plik-wyjściowy` --  kompresja do podanego pliku
* `-s --size` --  rozmiar pliku w kB
* `-l --laplace` -- obliczenie netropii i wypisanie na standardowe wyjście
* `-n --normal` -- pokazywanie więcej informacji

# Rysowanie Histogramu
``` sh
python3 plotHistogram.py --filename <plik-wejściowy>
```






