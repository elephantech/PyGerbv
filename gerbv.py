# encoding: utf-8

import argparse
from ctypes import *
from ctypes.util import find_library

from .structure import *
from .utils import show_info

class FileInfo(object):
    def __init__(self, file_info):
        self._file_info = file_info
        self._color = None
        self.color = (0, 0, 0, 0)
        self._alpha = None
        self.alpha = 1.0
        self._is_visible = None
        self.is_visible = True
        self._file_info.transform = GerbvUserTransformation(0, 0, 1, 1, 0, False, False, False)
        self.inverted = False

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._file_info.color = GdkColor(*[int(x * 65535) for x in color])
        self._color = color

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._file_info.alpha = int(alpha * 65535)
        self._alpha = alpha

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, is_visible):
        self._file_info.isVisible = is_visible
        self._is_visible = is_visible

    def translate(self, x, y):
        self._file_info.transform.translateX += x
        self._file_info.transform.translateY += y

    def scale(self, x, y):
        self._file_info.transform.scaleX *= x
        self._file_info.transform.scaleY *= y

    def rotate(self, theta):
        self._file_info.transform.rotation += theta

    def mirror(self, x, y):
        self._file_info.transform.mirrorAroundX = x
        self._file_info.transform.mirrorAroundY = y

    @property
    def inverted(self):
        return self._inverted

    @inverted.setter
    def inverted(self, inverted):
        self._file_info.transform.inverted = inverted
        self._inverted = inverted

    @property
    def min_x(self):
        return self._file_info.image.contents.info.contents.min_x

    @property
    def min_y(self):
        return self._file_info.image.contents.info.contents.min_y

    @property
    def max_x(self):
        return self._file_info.image.contents.info.contents.max_x

    @property
    def max_y(self):
        return self._file_info.image.contents.info.contents.max_y


class Project(object):
    _libgerbv = CDLL(find_library('gerbv'))
    _libgerbv.gerbv_create_project.restype = POINTER(GerbvProject)
    _libgerbv.gerbv_open_layer_from_filename.argtypes = [POINTER(GerbvProject), c_char_p]
    _libgerbv.gerbv_export_pdf_file_from_project.argtypes = [POINTER(GerbvProject), POINTER(GerbvRenderInfo), c_char_p]
    _libgerbv.gerbv_export_png_file_from_project.argtypes = [POINTER(GerbvProject), POINTER(GerbvRenderInfo), c_char_p]
    _libgerbv.gerbv_render_get_boundingbox.argtypes = [POINTER(GerbvProject), POINTER(GerbvRenderSize)]

    def __init__(self):
        self._project = self._libgerbv.gerbv_create_project()[0]
        self._background = None
        self.background = (0, 1, 1, 1)
        self.file = []

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, color):
        self._project.background = GdkColor(*[int(x * 65535) for x in color])
        self._background = color

    def open_layer_from_filename(self, filename):
        self._libgerbv.gerbv_open_layer_from_filename(self._project, filename.encode('utf-8'))
        file_info = FileInfo(self._project.file[self._project.last_loaded].contents)
        self.file.append(file_info)
        return file_info

    def export_pdf_file_autosized(self, filename):
        render_info = self._generate_render_info()
        self._libgerbv.gerbv_export_pdf_file_from_project(self._project, render_info, filename.encode('utf-8'))

    def export_png_file_autosized(self, filename):
        render_info = self._generate_render_info()
        self._libgerbv.gerbv_export_png_file_from_project(self._project, render_info, filename.encode('utf-8'))

    def _generate_render_info(self, dpi=72):
        # Make all layers visible once to get a consistent bounding box regardless the visibilities of layers
        visibilities = [layer.is_visible for layer in self.file]
        for layer in self.file:
            layer.is_visible = True

        libgerbv = self._libgerbv
        # exportimage.c
        # gerbv_export_autoscale_project
        bb = GerbvRenderSize(0, 0, 0, 0)
        libgerbv.gerbv_render_get_boundingbox(self._project, byref(bb))

        # Plus margins
        margin_in_inch = 0.05

        width  = bb.right  - bb.left + margin_in_inch * 2;
        height = bb.bottom - bb.top + margin_in_inch * 2;

        # Change visibilities back
        for i, layer in enumerate(self.file):
            layer.is_visible = visibilities[i]

        return GerbvRenderInfo(dpi, dpi, bb.left-margin_in_inch, bb.top-margin_in_inch, 3, int(width*dpi), int(height*dpi))
