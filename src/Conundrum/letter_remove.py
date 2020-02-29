def remove_letters(original_msg: str, letters_to_remove: str) -> str:
    for letter in letters_to_remove:
        original_msg = original_msg.replace(letter, '', 1)
    return ''.join(sorted(original_msg))


if __name__ == '__main__':
    # Used in Movies 2
    msg = 'nerd averts surf straight away'
    film_1 = 'star wars'
    film_2 = 'saturday night fever'
    print(remove_letters(remove_letters(msg, film_1), film_2))
