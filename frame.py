import datetime
import locale
import os
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET
from os import walk
from random import shuffle

import exifread
import pyglet
import yaml
from tendo import singleton

bufferedStream = open('frame.log', 'a', buffering=1)
sys.stdout = bufferedStream
sys.stderr = bufferedStream

print("")
print("-------------------------------------")
print("Launching new instance of frame.py...")
print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
print("-------------------------------------")
print("")


class Config(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Config'

    def __init__(self):
        self.cecEnabled = True
        self.basePath = "/mnt/photos"
        self.pathSeparator = "/"
        self.locale = ""


config = Config()
with open("config.yml") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

cecAvailable = False
if config.cecEnabled:
    try:
        import cec
        cecAvailable = True
    except ImportError:
        cecAvailable = False

print("CEC is", "available" if cecAvailable else "unavailable.")

me = singleton.SingleInstance()

images = []


def images_load():
    global images
    global config
    images.clear()

    for (_, _, filenames) in walk(config.basePath):
        images.extend(filenames)
        break

    if len(images) == 0:
        print("Error: no images found.")
        exit(1)

    shuffle(images)


images_load()
print("Found", len(images), "pictures.")

locale.setlocale(locale.LC_ALL, config.locale)
os.environ['DISPLAY'] = ":0"

if cecAvailable:
    cec.init()

window = pyglet.window.Window(fullscreen=True, vsync=True)
window.set_mouse_visible(False)
window_dim = window.get_size()

print("Detected screen resolution:", window_dim[0], "x", window_dim[1])


class pic(object):
    def __init__(self, filename):
        self.filename = filename
        self.drawn = False

        fstream = open(self.filename, 'rb')

        try:
            self.image = pyglet.image.load(self.filename, file=fstream)
        except Exception as ex:
            print("Could not parse image" + self.filename + ":" + repr(ex))
            self.image = None
            return

        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        fstream.seek(0, 0)
        self.tags = exifread.process_file(fstream)

        fstream.seek(0, 0)
        data = fstream.read().decode('utf-8', 'ignore')
        fstream.close()
        xmp_start = data.find('<x:xmpmeta')
        xmp_end = data.find('</x:xmpmeta')
        xmp_str = data[xmp_start:xmp_end + 12]

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
        except Exception:
            self.title = None

        if self.title is not None:
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

        if self.shot_time is not None:
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
        if self.image is None:
            return

        self.image.blit(window_dim[0] // 2, window_dim[1] // 2)
        self.back_label.draw()
        self.label.draw()
        self.drawn = True

    def valid(self):
        return self.image is not None

image_at = 0
current_picture = None

def picture_update(dt):
    global image_at
    global current_picture
    global images
    global config
    global cecAvailable

    while image_at < len(images):
        current_picture = pic(config.basePath + config.pathSeparator + images[image_at])
        if not current_picture.valid():
            image_at += 1
        else:
            break

    now = datetime.datetime.now().time()
    startt = datetime.time(hour=8, minute=0)
    endt = datetime.time(hour=23, minute=30)

    if cecAvailable:
        istvon = False
        try:
            global cec
            tv = cec.Device(0)

            istvon = tv.is_on()

            if startt <= now and endt >= now:
                if not istvon:
                    tv.power_on()
                    print("Powering TV on...")
            else:
                if istvon:
                    tv.standby()
                    istvon = False
                    print("Powering TV off...")
        except Exception as ex:
            print("Exception in CEC TV handling:", ex)
            istvon = True
    else:
        istvon = True

    if istvon:
        image_at += 1
        if image_at >= len(images):
            images_load()
            image_at = 0

@window.event
def on_draw():
    global window
    global current_picture
    if current_picture is not None and current_picture.drawn == False:
        window.clear()
        current_picture.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        print("ESC detected, exiting...")
        global window
        window.close()


pyglet.clock.schedule_interval_soft(picture_update, 5)
pyglet.app.run()
