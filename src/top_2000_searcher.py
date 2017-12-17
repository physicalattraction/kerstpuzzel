import os.path


class Top2000:
    def __init__(self):
        # TODO: Make a dict with artists
        # TODO: Clean and use for anagrams etc.
        with open(os.path.join('..', 'txt', 'originals', 'top2000_2016')) as f:
            self.top2000 = [line for line in f.read().split('\n')]


if __name__ == '__main__':
    top = Top2000()
    for song in top.top2000:
        if song.count(' ') == 2:
            print(song)
