'''
Created on Mar 19, 2015

@author: Erwin Rossen
'''

from io import BytesIO
import os

from PIL import Image, ImageFont, ImageDraw, ImageOps
import requests
import math


class ImageCreator(object):
    '''
    Abstract base class to convert images to make them suitable for newsletters.
    '''

    @staticmethod
    def get_img_root_dir():
        '''Return a string which contains the root Aurora img directory.

        Current directory structure:
        Aurora
            src
                ImageEditing
                NewlestterImages
            img
                img_original
        '''
        current_dir = os.path.dirname(__file__)
        img_dir = os.path.join(current_dir, '..', '..', 'img')
        return img_dir

    def __init__(self):
        self.img_size = 400
        self.margin = 20
        self.photos = list()

    def set_img_dir(self, img_dir):
        '''Set the directory in which to store the created images.

        Inputs:
        -------
        img_dir: string
            Name of the directory.
            This needs to be a directory inside the img directory.

        Returns:
        --------
        None

        Postconditions:
        ---------------
        Image output directory is set in object.
        '''

        img_root_dir = ImageCreator.get_img_root_dir()
        self._ensure_dir_exists(img_root_dir)
        full_img_dir = os.path.join(img_root_dir, img_dir)
        self._ensure_dir_exists(full_img_dir)
        self.img_dir = full_img_dir

    def download_img(self, url):
        '''Download an image as PIL object

        If the img is not present yet, it is downloaded from the specified URL.

        Inputs:
        -------
        url: string

        Outputs:
        --------
        img: Image
            Opened original image of the given article number.
            If img = None, this means that the requested image does not exist.
        '''

        if url is None:
            return
        r = requests.get(url)
        try:
            img = Image.open(BytesIO(r.content))
            img = img.resize((self.img_size, self.img_size), Image.ANTIALIAS)
            self.photos.append(img)
        except OSError as e:
            # Print the error message, but continue downloading
            print(e.msg)

    def create_collage(self, user, match=False):
        '''
        Collect all photos and place user info under the photos
        '''

        nr_photos = len(self.photos)
        if nr_photos == 1:
            W = self.img_size
        else:
            W = 2 * self.img_size
        H = int(math.ceil(nr_photos / 2.0) * self.img_size)

        img = Image.new(mode='RGB', size=(W, H), color='white')

        index_x = 0
        index_y = 0
        for photo in self.photos:
            x = index_x * self.img_size
            y = index_y * self.img_size
            img.paste(photo, box=(x, y, x + photo.size[0], y + photo.size[1]))
            if index_x == 0:
                # Move to the right
                index_x = 1
            elif index_x == 1:
                # Move below and back to the left
                index_x = 0
                index_y += 1
        img = self._write_user_info(img, user, match)
        img = self._add_bottom_margin(img)

        if match:
            filename = 'MATCH_{}_{}.jpg'.format(user['name'], user['_id'])
        else:
            filename = '{}_{}.jpg'.format(user['name'], user['_id'])
        full_img_name = os.path.join(self.img_dir, filename)
        img.save(full_img_name, quality=95, optimize=True)

    def _write_user_info(self, img, user, match):
        self.first_text = True

        if match:
            img = self._put_text_in_img(img, '!!! MATCH !!!')

        img = self._put_text_in_img(img, 'Naam: {}'.format(user['name']))

        img = self._put_text_in_img(img, 'Geboortedatum: {}'.format(user['birth_date'][0:10]))

        jobs = list()
        for job in user['jobs']:
            this_job = list()
            if 'title' in job and 'name' in job['title']:
                this_job.append(job['title']['name'])
            if 'company' in job and 'name' in job['company']:
                this_job.append(job['company']['name'])
            if len(this_job) > 0:
                this_job_string = ' - '.join(this_job)
                jobs.append(this_job_string)
        if len(jobs) > 0:
            img = self._put_text_in_img(img, 'Werk: {}'.format(', '.join(jobs)))

        schools = list()
        for school in user['schools']:
            schools.append(school['name'])
        if len(schools) > 0:
            img = self._put_text_in_img(img, 'School: {}'.format(', '.join(schools)))

        common_friends = list()
        for friend in common_friends:
            print(friend)
            common_friends.append(friend['name'])
        if len(common_friends) > 0:
            img = self._put_text_in_img(img, 'Vrienden: {}'.format(', '.join(common_friends)))

        distance_km = int(round(user['distance_mi'] * 1.609))
        img = self._put_text_in_img(img, 'Afstand: {} km'.format(distance_km))
        img = self._put_text_in_img(img, 'Bio: {}'.format(user['bio']))

        return img

    def _put_text_in_img(self, img, text):
        '''
        Put the relevant text of a person in the img.
        '''

        font_size = 24
        line_height = font_size + 2
        if (self.first_text):
            new_height = img.size[1] + line_height + self.margin
        else:
            new_height = img.size[1] + line_height

        # Create more space to output text
        result = Image.new(mode='RGB', size=(img.size[0], new_height), color='white')
        result.paste(img, (0, 0, img.size[0], img.size[1]))

        # Initialize draw object
        draw = ImageDraw.Draw(result)

        # Define font
        font = ImageFont.truetype("Trebuchet MS Bold.ttf", font_size)

        # Define text location
        x = self.margin
        if self.first_text:
            y = img.size[1] + self.margin
        else:
            y = img.size[1]

        # Draw the text
        draw.text((x, y), text, fill='black', font=font)

        # Indicate that we have drawn at least one text
        self.first_text = False

        return result

    def _add_bottom_margin(self, img):
        result = Image.new(mode='RGB', size=(img.size[0], img.size[1] + self.margin), color='white')
        result.paste(img, (0, 0, img.size[0], img.size[1]))
        return result

    def _ensure_dir_exists(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

if __name__ == '__main__':
    pass
