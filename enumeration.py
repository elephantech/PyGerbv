import enum
from ctypes import *


c_gerbv_aperture_state_t = c_int
c_gerbv_aperture_type_t = c_int
c_gerbv_axis_select_t = c_int
c_gerbv_cirseg_t = c_int
c_gerbv_coordinate_t = c_int
c_gerbv_encoding_t = c_int
c_gerbv_image_justify_type_t = c_int
c_gerbv_interpolation_t = c_int
c_gerbv_knockout_type_t = c_int
c_gerbv_layertype_t = c_int
c_gerbv_message_type_t = c_int
c_gerbv_mirror_state_t = c_int
c_gerbv_omit_zeros_t = c_int
c_gerbv_opcodes_t = c_int
c_gerbv_polarity_t = c_int
c_gerbv_render_types_t = c_int
c_gerbv_selection_t = c_int
c_gerbv_unit_t = c_int


class ApertureType(enum.IntEnum):
    NONE = 0
    CIRCLE = 1
    RECTANGLE = 2
    OVAL = 3
    POLYGON = 4
    MACRO = 5
    MACRO_CIRCLE = 6
    MACRO_OUTLINE = 7
    MACRO_POLYGON = 8
    MACRO_MOIRE = 9
    MACRO_THERMAL = 10
    MACRO_LINE20 = 11
    MACRO_LINE21 = 12
    MACRO_LINE22 = 13


class Unit(enum.IntEnum):
    INCH = 0,
    MM = 1,
    UNSPECIFIED = 2
