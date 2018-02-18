import pyglet
import exifread
import xml.etree.ElementTree as ET
import datetime
import locale
import os, subprocess
import time
from os import walk
from random import shuffle
import threading

basepath = '/mnt/photos'
pathseparator = '/'

images = []
for (dirpath, dirnames, filenames) in walk(basepath):
    images.extend(filenames)
    break
shuffle(images)

locale.setlocale(locale.LC_ALL, '')
os.environ['DISPLAY'] = ":0"

window = pyglet.window.Window(fullscreen=True)
window_dim = window.get_size()

class pic(object):
    def __init__(self, filename):
        self.filename = filename
        fstream = open(self.filename, 'rb')

        self.image = pyglet.image.load(self.filename, file=fstream)
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        fstream.seek(0, 0)
        self.tags = exifread.process_file(fstream)

        fstream.seek(0, 0)
        data = fstream.read().decode('utf-8', 'ignore')
        xmp_start = data.find('<x:xmpmeta')
        xmp_end = data.find('</x:xmpmeta')
        xmp_str = data[xmp_start:xmp_end+12]

        namesp = {
                'x': 'adobe:ns:meta/',
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'photoshop': 'http://ns.adobe.com/photoshop/1.0/',
                'dc': 'http://purl.org/dc/elements/1.1/'
                }

        xmp_tree = ET.fromstring(xmp_str)
        xmp_desc = xmp_tree.find('rdf:RDF', namesp).find('rdf:Description', namesp)

        try:
            self.title = xmp_desc.find('dc:title', namesp).find('rdf:Alt', namesp).find('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li').text.strip()
        except:
            self.title = None

        if  self.title != None:
            self.fullname = self.title
        else:
            self.city = xmp_desc.get('{http://ns.adobe.com/photoshop/1.0/}City')
            self.state = xmp_desc.get('{http://ns.adobe.com/photoshop/1.0/}State')
            self.country = xmp_desc.get('{http://ns.adobe.com/photoshop/1.0/}Country')

            self.fullname = ', '.join(filter(None, [self.city, self.state, self.country]))

        if 'EXIF DateTimeOriginal' in self.tags:
            t = str(self.tags['EXIF DateTimeOriginal'])
            self.shot_time = datetime.datetime.strptime(t, "%Y:%m:%d %H:%M:%S")
        else:
            self.shot_time = None

        if self.shot_time != None:
            self.fullname += self.shot_time.strftime(" (%d %B %Y)")

        self.label = pyglet.text.Label(self.fullname,
                                        font_name='Droid Sans Bold',
                                        font_size=36,
                                        x=10, y=10,
                                        anchor_x='left', anchor_y='bottom')

        self.back_label = pyglet.text.Label(self.fullname,
                                        font_name='Droid Sans Bold',
                                        font_size=36,
                                        x=12, y=8,
                                        color=(0, 0, 0, 255),
                                        anchor_x='left', anchor_y='bottom')

    def draw(self):
        self.image.blit(window_dim[0] // 2, window_dim[1] // 2)
        self.back_label.draw()
        self.label.draw()


image_at = 0
current_picture = None

def picture_update(dt):
    global image_at
    global current_picture
    global images
    global basepath
    current_picture = pic(basepath + pathseparator + images[image_at])

    image_at += 1
    if image_at == len(images):
        image_at = 0

@window.event
def on_draw():
    global window
    global current_picture
    window.clear()
    if current_picture != None:
        current_picture.draw()

pyglet.clock.schedule_interval(picture_update, 5)
pyglet.app.run()
