import math


class ColorFilter:
    def __init__(self):
        self.img = 'NWOBBGRWZBWRGWPRWGNRORWN' \
                   'WGBNGBRWWRWWGZRGRWBNRNGW' \
                   'GWNPPBPWPOGBGORPZONBORBB' \
                   'BRRPRNWONZGRNGPBZWBPRWBG' \
                   'WWWGNGRWWBWBWBWRWGWRWOGN'
        self.color_values = {'W': (0, 0, 0),
                             'B': (0, 0, 1),
                             'G': (0, 1, 0),
                             'N': (0, 1, 1),
                             'R': (1, 0, 0),
                             'P': (1, 0, 1),
                             'O': (1, 1, 0),
                             'Z': (1, 1, 1)}

    def print_image(self, filter: str):
        length = len(self.img)
        for n in range(length, int(math.sqrt(length)), -1):
            img = [self.img[i:i+n] for i in range(0, len(self.img), n)]
            if not len(img[-1]) == len(img[0]):
                continue

            print('-' * 80)
            filter_index = ['R', 'G', 'B'].index(filter)
            for line in img:
                print_line = ['*' if self.color_values[letter][filter_index] else ' ' for letter in line]
                print(''.join(print_line))


if __name__ == '__main__':
    color_filter = ColorFilter()
    color_filter.print_image('B')
