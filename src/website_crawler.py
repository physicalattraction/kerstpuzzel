import json
import os.path
import re

import requests

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


class WebsiteCrawler:
    MOVIES = 'movies'
    SERIES = 'series'
    DIED2017 = 'died2017'

    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.output_file_with_years = None
        self.output_file_with_tags = None
        self.tags = None

    def crawl_source(self, source: str):
        if source == self.MOVIES:
            self.input_file = os.path.join('..', 'txt', 'originals', 'DutchMoviesHtml.txt')
            self.output_file = os.path.join('..', 'txt', 'originals', 'DutchMovies.txt')
            self.output_file_with_years = os.path.join('..', 'txt', 'originals', 'DutchMoviesPerYear.json')

            for page in range(1, 16 + 1):
                print('Download page {}'.format(page))
                url = 'https://www.filmvandaag.nl/nederlandsefilms?offset={}' \
                      '&sort=release&order=DESC'.format(page)  # For movies
                response = requests.get(url)
                html_response = response.content.decode(encoding='utf-8')
                with open(self.input_file, 'w+') as f:
                    f.write(html_response)
                self.clean_movies(source)
        elif source == self.SERIES:
            self.input_file = os.path.join('..', 'txt', 'originals', 'DutchSeriesHtml.txt')
            self.output_file = os.path.join('..', 'txt', 'originals', 'DutchSeries.txt')

            url = 'https://nl.wikipedia.org/wiki/Categorie:Nederlandse_dramaserie'  # For series
            response = requests.get(url)
            html_response = response.content.decode(encoding='utf-8')
            with open(self.input_file, 'w+') as f:
                f.write(html_response)
            self.clean_movies(source)
        elif source == self.DIED2017:
            self.output_file = os.path.join('..', 'txt', 'originals', 'Died2017.txt')
            self.output_file_with_tags = os.path.join('..', 'txt', 'originals', 'Died2017.json')

            names = []
            tags = {}
            for month in MONTHS:
                print('Download month {}'.format(month))
                self.tags = [month]
                url = 'https://en.wikipedia.org/wiki/Deaths_in_{}_2017'.format(month)
                response = requests.get(url)
                html_response = response.content.decode(encoding='utf-8')
                new_names, new_tags = self.clean_string(html_response, source)
                names += new_names
                tags.update(new_tags)

            with open(self.output_file, 'w+') as f:
                print('Writing file {}'.format(self.output_file))
                f.write('\n'.join(sorted(names)))

            with open(self.output_file_with_tags, 'w+') as f:
                print('Writing file {}'.format(self.output_file_with_tags))
                f.write(json.dumps(tags))

            return names

    def clean_string(self, html_source: str, source: str) -> [str]:
        if source == self.DIED2017:
            names = []
            tags = {}
            for line in html_source.split('\n'):
                patterns = re.findall('^<li><a href="\/wiki\/(.*)" title="(.*)">(.*)<\/a>,', line)
                if len(patterns) > 0:
                    patterns = patterns[0]  # [(p0, p1, p2)] --> (p0, p1, p2)
                    name = patterns[2]
                    names.append(name)
                    tags[name] = self.tags + self.lookup_tags(line, source)

            return names, tags

    def lookup_tags(self, line: str, source: str) -> [str]:
        if source == self.DIED2017:
            patterns = re.findall('^<li><a href="\/wiki\/(.*)" title="(.*)">(.*)<\/a>, (.*), (.*),', line)
            if len(patterns) > 0:
                patterns = patterns[0]
                return [patterns[3], patterns[4]]
        return []

    def clean_movies(self, source: str):
        with open(self.input_file, 'r') as f:
            contents = f.read().split('\n')

        titles = years = []
        if source == self.MOVIES:
            contents = [line for line in contents if 'movielist-item-tiny' in line]
            titles = [re.sub('^.*">(.*) \((\d{4})\)<\/a>$', '\\1', line) for line in contents]
            years = [re.sub('.*\((\d{4})\).*$', '\\1', line) for line in contents]
        elif source == self.SERIES:
            titles = [re.sub('^.*">(.*)<\/a>.*$', '\\1', line) for line in contents]

        self.add_titles_and_years(titles, years)

    def add_titles_and_years(self, titles, years):
        if not titles:
            return

        existing_titles = []
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r') as f:
                existing_titles = f.read().split('\n')
        all_titles = set(existing_titles + titles)
        with open(self.output_file, 'w+') as f:
            print('Writing file {}'.format(self.output_file))
            f.write('\n'.join(sorted(all_titles)))

        if not years:
            return

        existing_titles_with_year = {}
        titles_with_years = {title: year for title, year in zip(titles, years)}
        if os.path.exists(self.output_file_with_years):
            with open(self.output_file_with_years, 'r') as f:
                existing_titles_with_year = json.loads(f.read())
        titles_with_years.update(existing_titles_with_year)

        with open(self.output_file_with_years, 'w+') as f:
            print('Writing file {}'.format(self.output_file_with_years))
            f.write(json.dumps(titles_with_years, indent=4, sort_keys=True))


if __name__ == '__main__':
    crawler = WebsiteCrawler()
    # cleaner.download_movie_info(source=cleaner.SERIES)
    names = crawler.crawl_source(source=crawler.DIED2017)
    print(names)
