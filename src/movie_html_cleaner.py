import json
import os.path
import re


class MovieCleaner:
    def __init__(self):
        self.input_file = os.path.join('..', 'txt', 'originals', 'DutchMoviesHtml.txt')
        self.output_file = os.path.join('..', 'txt', 'originals', 'DutchMovies.txt')
        self.output_file_with_years = os.path.join('..', 'txt', 'originals', 'DutchMoviesPerYear.txt')

    def clean_movies(self):
        with open(self.input_file, 'r') as f:
            contents = f.read().split('\n')

        # Remove all lines except lines with titles
        contents = [line for line in contents if 'movielist-item-tiny' in line]

        # Extract titles and years from lines with title
        titles = [re.sub('^.*">(.*) \((\d{4})\)<\/a>$', '\\1', line) for line in contents]
        years = [re.sub('.*\((\d{4})\).*$', '\\1', line) for line in contents]

        with open(os.path.join(self.output_file), 'w+') as f:
            print('Writing file {}'.format(self.output_file))
            f.write('\n'.join(titles))

        with open(os.path.join(self.output_file), 'w+') as f:
            print('Writing file {}'.format(self.output_file))
            f.write(json.dumps({title: year} for title, year in zip(titles, years)))


if __name__ == '__main__':
    cleaner = MovieCleaner()
    cleaner.clean_movies()