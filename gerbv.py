# encoding: utf-8

import argparse
from ctypes import *
from ctypes.util import find_library
import platform

from .exceptions import *
from .enumeration import *
from .structure import *
from .utils import show_info


library_path = find_library('gerbv')
if not library_path:
    raise ModuleNotFoundError
if platform.system() == 'Linux':
    _libgerbv = CDLL('/usr/local/lib/' + library_path)
else:
    _libgerbv = CDLL(library_path)


class Aperture:
    @classmethod
    def create_circle_aperture(cls, diameter_in_mm):
        params = c_double * APERTURE_PARAMETERS_MAX
        diameter_in_inch = diameter_in_mm / 25.4
        return cls(GerbvAperture(ApertureType.CIRCLE, None, None, params(diameter_in_inch), 0, 0))

    def __init__(self, aperture):
        self._aperture = aperture

    @property
    def type(self):
        return self._aperture.type

    @property
    def amacro(self):
        return self._aperture.amacro

    @property
    def simplified(self):
        return self._aperture.simplified

    @property
    def parameter(self):
        return self._aperture.parameter

    @property
    def nuf_parameters(self):
        return self._aperture.nuf_parameters

    @property
    def unit(self):
        return self._aperture.unit


class Image:
    _libgerbv.gerbv_image_create_line_object.argtypes = [POINTER(GerbvImage), c_double, c_double, c_double, c_double, c_double, c_gerbv_aperture_type_t]
    _libgerbv.gerbv_export_rs274x_file_from_image.restype = c_bool
    _libgerbv.gerbv_export_rs274x_file_from_image.argtypes = [c_char_p, POINTER(GerbvImage), POINTER(GerbvUserTransformation)]

    def __init__(self, image):
        self._image = image
        aperture_ids = set()
        net = image.contents.netlist.contents
        while(net.next):
            net = net.next.contents
            aperture_ids.add(net.aperture)
        self._apertures = [(aperture_id, Aperture(image.contents.aperture[aperture_id].contents)) for aperture_id in aperture_ids]

    @property
    def apertures(self):
        return self._apertures

    @apertures.setter
    def apertures(self, apertures):
        self._apertures = apertures
        for aperture_id, aperture in apertures:
            self._image.contents.aperture[aperture_id].contents = GerbvAperture(aperture.type, aperture.amacro, aperture.simplified, aperture.parameter, aperture.nuf_parameters, aperture.unit)

    @property
    def min_x(self):
        return self._image.contents.info.contents.min_x

    @property
    def min_y(self):
        return self._image.contents.info.contents.min_y

    @property
    def max_x(self):
        return self._image.contents.info.contents.max_x

    @property
    def max_y(self):
        return self._image.contents.info.contents.max_y

    def create_line_object(self, start_x, start_y, end_x, end_y, line_width, aperture_type):
        _libgerbv.gerbv_image_create_line_object(self._image, start_x, start_y, end_x, end_y, line_width, aperture_type)

    def export_rs274x_file(self, filename, transformation):
        return _libgerbv.gerbv_export_rs274x_file_from_image(filename.encode('utf-8'), self._image, transformation)


class FileInfo:
    def __init__(self, file_info):
        self._file_info = file_info
        self.image = Image(self._file_info.image)
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


class Project:
    _libgerbv.gerbv_create_project.restype = POINTER(GerbvProject)
    _libgerbv.gerbv_open_layer_from_filename.argtypes = [POINTER(GerbvProject), c_char_p]
    _libgerbv.gerbv_export_pdf_file_from_project.argtypes = [POINTER(GerbvProject), POINTER(GerbvRenderInfo), c_char_p]
    _libgerbv.gerbv_export_png_file_from_project.argtypes = [POINTER(GerbvProject), POINTER(GerbvRenderInfo), c_char_p]
    _libgerbv.gerbv_export_svg_file_from_project.argtypes = [POINTER(GerbvProject), POINTER(GerbvRenderInfo), c_char_p]
    _libgerbv.gerbv_render_get_boundingbox.argtypes = [POINTER(GerbvProject), POINTER(GerbvRenderSize)]

    def __init__(self):
        self._project = _libgerbv.gerbv_create_project()[0]
        self._background = None
        self.background = (0, 1, 1, 1)
        self.file = []
        self.margin = 0.001
        self._bounding_box = GerbvRenderSize(0, 0, 0, 0)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, color):
        self._project.background = GdkColor(*[int(x * 65535) for x in color])
        self._background = color

    @property
    def bounding_box(self):
        bb = self._bounding_box
        layer_visibilities = []
        # Make all layers visible once to get a consistent bounding box regardless the visibilities of layers
        for layer in self.file:
            layer_visibilities.append(layer.is_visible)
            layer.is_visible = True

        _libgerbv.gerbv_render_get_boundingbox(self._project, byref(self._bounding_box))
        # Set visibilities again
        for i, layer in enumerate(self.file):
            layer.is_visible = layer_visibilities[i]
        return self._bounding_box

    def open_layer_from_filename(self, filename):
        files_loaded = self.files_loaded()
        _libgerbv.gerbv_open_layer_from_filename(self._project, filename.encode('utf-8'))
        if self.files_loaded() == files_loaded:
            raise GerberFormatError
        file_info = FileInfo(self._project.file[self._project.last_loaded].contents)
        self.file.append(file_info)
        return file_info

    def export_pdf_file_autosized(self, filename):
        if self.files_loaded() == 0:
            raise GerberNotFoundError
        else:
            render_info = self._generate_render_info()
            _libgerbv.gerbv_export_pdf_file_from_project(self._project, render_info, filename.encode('utf-8'))

    def export_png_file_autosized(self, filename):
        if self.files_loaded() == 0:
            raise GerberNotFoundError
        else:
            render_info = self._generate_render_info()
            _libgerbv.gerbv_export_png_file_from_project(self._project, render_info, filename.encode('utf-8'))

    def export_svg_file_autosized(self, filename):
        if self.files_loaded() == 0:
            raise GerberNotFoundError
        else:
            render_info = self._generate_render_info(dpi=72*3/4) # SVG will use pt instead of px
            _libgerbv.gerbv_export_svg_file_from_project(self._project, render_info, filename.encode('utf-8'))

    def translate(self, x, y):
        for layer in self.file:
            layer.translate(x, y)

    def scale(self, x, y):
        for layer in self.file:
            layer.scale(x, y)

    def rotate(self, theta):
        for layer in self.file:
            layer.rotate(theta)
            layer.translate(0, self.width)

    def set_margin(self, margin):
        self.margin = margin
        if self.margin < 0.001:
            self.margin = 0.001

    @property
    def min_x(self):
        return self.bounding_box.left

    @property
    def min_y(self):
        return self.bounding_box.top

    @property
    def max_x(self):
        return self.bounding_box.right

    @property
    def max_y(self):
        return self.bounding_box.bottom

    @property
    def width(self):
        return self.bounding_box.right - self.bounding_box.left

    @property
    def height(self):
        return self.bounding_box.bottom - self.bounding_box.top

    def files_loaded(self):
        """Returns the number of loaded files"""
        return self._project.last_loaded + 1

    def _generate_render_info(self, dpi=72):
        # Plus a little extra to prevent from missing items due to round-off errors
        width = self.width + self.margin * 2
        height = self.height + self.margin * 2
        height, width = sorted([width, height])
        return GerbvRenderInfo(dpi, dpi, self.min_x - self.margin, self.min_y - self.margin, 3, int(width * dpi), int(height * dpi))
