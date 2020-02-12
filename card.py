# Copyright (c) 2009-14 Walter Bender
# Copyright (c) 2009 Michele Pratusevich

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

from gi.repository import GdkPixbuf

from constants import COLORS, NUMBER, FILLS, CARD_WIDTH, CARD_HEIGHT
from sprites import Sprite


class Card:

    ''' Individual cards '''

    def __init__(self, scale=1.0):
        ''' Create the card and store its attributes '''
        self.spr = None
        self.index = None  # Calculated index
        self._scale = scale

    def create(self, string, attributes=None, sprites=None, file_path=None):
        if attributes is None:
            if self.spr is None:
                self.spr = Sprite(sprites, 0, 0, svg_str_to_pixbuf(string))
            else:
                self.spr.set_image(svg_str_to_pixbuf(string))
            self.index = None
        else:
            self.shape = attributes[0]
            self.color = attributes[1]
            self.num = attributes[2]
            self.fill = attributes[3]
            self.index = self.shape * COLORS * NUMBER * FILLS + \
                self.color * NUMBER * FILLS + \
                self.num * FILLS + \
                self.fill
            self.spr = Sprite(sprites, 0, 0, svg_str_to_pixbuf(string, True))
            if file_path is not None:
                self.spr.set_image(load_image(file_path, self._scale), i=1,
                                   dx=int(self._scale * CARD_WIDTH * .125),
                                   dy=int(self._scale * CARD_HEIGHT * .125))
        self.spr.set_label_attributes(self._scale * 24)
        self.spr.set_label('')

    def show_card(self, layer=2000):
        ''' Show the card '''
        if self.spr is not None:
            self.spr.set_layer(layer)
            self.spr.draw()

    def hide_card(self):
        ''' Hide a card '''
        if self.spr is not None:
            self.spr.hide()


def svg_str_to_pixbuf(string, embedded_picture=False):
    ''' Load pixbuf from SVG string '''
    pl = GdkPixbuf.PixbufLoader.new_with_type('svg')
    pl.write(string.encode('utf-8'))
    pl.close()
    pixbuf = pl.get_pixbuf()
    pixbuf2 = None

    if embedded_picture:
        p_path = None
        p_size = [0, 0]

        for line in string.splitlines():
            # Extract png data
            if line.startswith('xlink:href="file://'):
                p_path = line[19:-1]  # xlink:href="file:///home/..."

            elif line.startswith("width="):
                p_size[0] = int(float(line[7:-1]))  # width="data"

            elif line.startswith("height="):
                p_size[1] = int(float(line[8:-1]))  # height="data"

        if p_path is not None and p_size != [0, 0]:
            pixbuf2 = GdkPixbuf.Pixbuf.new_from_file_at_size(p_path, p_size[0], p_size[1])

    if pixbuf2 is None:
        return pixbuf
    else:
        return [pixbuf, pixbuf2]

def load_image(object, scale):
    ''' Load pixbuf from file '''
    return GdkPixbuf.Pixbuf.new_from_file_at_size(
        object.file_path, int(scale * CARD_WIDTH * .75),
        int(scale * CARD_HEIGHT * .75))
