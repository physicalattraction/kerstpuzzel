from itertools import permutations, combinations

meeting_rooms = [
    ['Notes', 'Obelix', 'Balletje', 'Vleermuis', 'Hulst', 'Spar', ],
    ['Balletje', 'Beervlinder', 'Rio de Janeiro', 'Oprecht', 'Dokkum', 'Pluto', ],
    ['Mandela', 'Balletje', 'Obelix', 'Pluto', 'Fremont', 'Spar', ],
    ['Hulst', 'Oprecht', 'Lekbrug', 'Vleermuis', 'Mandela', 'Pluto', ],
    ['Hulst', 'Boardroom New York', 'Balletje', 'Beervlinder', 'Oprecht', 'Speeltuin', ],
    ['Sofia', 'Lekbrug', 'Dokkum', 'Speeltuin', 'Boardroom New York', 'Maisveld', ],
    ['Dokkum', 'Beervlinder', 'Fremont', 'Obelix', 'Oprecht', 'Hulst', ]
]
all_meeting_rooms = set([col for row in meeting_rooms for col in row ])
wrong_meeting_rooms = ['Speeltuin', 'Rio de Janeiro', 'Lekbrug', 'Dokkum', 'Maisveld', 'Sofia',]
correct_meeting_rooms = sorted([room for room in all_meeting_rooms if room not in wrong_meeting_rooms])

def number_correct_rooms():
    meeting_rooms_in_sets = [set(row) for row in meeting_rooms]
    for combination in combinations(correct_meeting_rooms, 6):
        combination = set(combination)
        numbers = [len(combination.intersection(row)) for row in meeting_rooms_in_sets]
        if numbers == [2, 2, 2, 2, 2, 1, 2]:
            print(', '.join(sorted(combination)))
            return(combination)

def meeting_room_per_person():
    correct_rooms = number_correct_rooms()
    meeting_rooms_per_person = [[row[index] for row in meeting_rooms] for index in range(6)]
    correct_meeting_rooms_per_person = [[room for room in row if room in correct_rooms] for row in meeting_rooms_per_person]
    print(correct_meeting_rooms_per_person)

if __name__ == '__main__':
    print(correct_meeting_rooms)
    meeting_room_per_person()