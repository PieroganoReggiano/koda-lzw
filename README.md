# Kompresor LZW

## Użycie:

``` sh
python3 lzw.py [opcje] <plik-wejściowy>
```

## Dostępne opcje

`--compress|-c plik-wyjściowy` -- kompresja do podanego pliku
`--extract|-x plik-wyjściowy` -- dekompresja do pliku
`--entropy` -- obliczenie netropii i wypisanie na standardowe wyjście
`--verbose` -- pokazywanie więcej informacji

### Opcje przy obliczaniu entropii

`--block-size rozmiar` -- czytanie pliku w sposób taki, że podana ilość bajtów to jeden symbol
`--condition-degree stopień` -- obliczenie entropii warunkowej podanego stopnia

Z powyższych dwóch opcji można użyć tylko jednej

## Szczegóły

Wynikowy plik jest w postaci binarnej w następujący sposób:
* Czterobajtowy nagłówek składający się z długości indeksu w bitach zapisany w little endian.
* Kolejne indeksy symboli zapisane na kolejnych bitach w kolejności little endian. Ostatni 'niedokończony' bajt jest wypełniony zerami.

