def number_list():
    original_number_list = [1350, -89, -140, -123, -86, -194, -90, -156, 221, -192, -58, -25, -122,
                            89, 31, -179, 172]
    x = 0
    result = []
    for i in original_number_list:
        x += i
        result.append(x)
    print(result)


def print_wind_list():
    winds = "W/NW NW/NO N/NW Z/Z NW/W ZW/ZO Z/Z NW/N ZW/W Z/NO Z/Z O/NO NW/ZW NO/ZW NO/Z NW/O Z/Z NO/O ZW/NW ZO/ZW Z/N O/NW Z/Z O/ZW W/NW NW/W O/W W/ZO Z/Z O/NO Z/NO N/Z Z/Z W/O W/NW NO/ZW ZW/NO Z/Z ZW/Z ZO/ZW Z/N Z/Z Z/O Z/ZW NO/ZW ZW/NO Z/Z ZW/NW ZW/ZO Z/Z ZO/Z O/W Z/NO NO/Z ZW/ZO Z/Z"
    wind_list = winds.split(sep=' ')

    permutation_dict = {
        'W/NW': 'a', 'NW/NO': 'b', 'N/NW': 'c', 'Z/Z': ' ', 'NW/W': 'e', 'ZW/W': 'f',
        'ZW/ZO': 'g', 'NW/N': 'h', 'Z/NO': 'i', 'O/NO': 'j', 'NW/ZW': 'k', 'NO/ZW': 'l',
        'NO/Z': 'm', 'NW/O': 'n', 'NO/O': 'o', 'ZW/NW': 'p', 'ZO/ZW': 'q', 'Z/N': 'r',
        'O/NW': 's', 'O/ZW': 't', 'O/W': 'u', 'W/ZO': 'v', 'N/Z': 'w', 'W/O': 'x',
        'ZW/NO': 'y', 'ZW/Z': 'z', 'Z/O': 'd', 'Z/ZW': '1', 'ZO/Z': '2'
    }
    output_list = []
    for c in wind_list:
        permutation_dict[c]
        new_c = permutation_dict.get(c) or c
        output_list.append(new_c)
    print(''.join(output_list))


if __name__ == '__main__':
    print_wind_list()
