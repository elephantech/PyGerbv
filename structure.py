from ctypes import *

from .enumeration import *

# GDK Typedefs
c_gboolean = c_int

# GDK Structures
# Will use gtk.gdk library
class GArray(Structure):
    _fields_ = [('data', POINTER(c_char)),
                ('len', c_uint)]

class GdkColor(Structure):
    _fields_ = [('pixel', c_uint),
                ('red', c_ushort),
                ('green', c_ushort),
                ('blue', c_ushort)]

class GString(Structure):
    _fields_ = [('str', c_char_p),
                ('len', c_ulong),
                ('allocated_len', c_ulong)]

# Gerbv Constants
APERTURE_MIN = 10
APERTURE_MAX = 9999
APERTURE_PARAMETERS_MAX = 102
INITIAL_SCALE = 200
MAX_ERRMSGLEN = 25
MAX_COORDLEN = 28
MAX_DISTLEN = 90
MAX_STATUSMSGLEN = MAX_ERRMSGLEN + MAX_COORDLEN + MAX_DISTLEN

# Gerbv Structures
# gerbv_HID_Attr_Val
class GerbvHIDAttrVal(Structure):
    _fields_ = [('int_value', c_int),
                ('str_value', c_char_p),
                ('real_value', c_double)]

# gerbv_HID_Attribute
class GerbvHIDAttribute(Structure):
    _fields_ = [('name', c_char_p),
                ('help_text', c_char_p),
                ('type', c_int), # enum: HID_Label, HID_Integer, HID_Real, HID_String, HID_Boolean, HID_Enum, HID_Mixed, HID_Path
                ('min_val', c_int),
                ('max_val', c_int),
                ('default_val', GerbvHIDAttrVal),
                ('enumerations', POINTER(c_char_p)),
                ('value', c_void_p),
                ('hash', c_int)]

# gerbv_error_list_t
class GerbvErrorList(Structure):
    pass
GerbvErrorList._fields_ = [('layer', c_int),
                ('error_text', c_char_p),
                ('type', c_gerbv_message_type_t),
                ('next', POINTER(GerbvErrorList))]

# gerbv_instruction_t
class GerbvInstructionData(Union):
    _fields_ = [('ival', c_int),
               ('fval', c_float)]

class GerbvInstruction(Structure):
    pass
GerbvInstruction._fields_ = [('opcode', c_gerbv_opcodes_t),
                ('data', GerbvInstructionData),
                ('next', POINTER(GerbvInstruction))]

# gerbv_amacro_t
class GerbvAmacro(Structure):
    pass
GerbvAmacro._fields_ = [('name', c_char_p),
                ('program', POINTER(GerbvInstruction)),
                ('nuf_push', c_uint),
                ('next', POINTER(GerbvAmacro))]

# gerbv_simplified_amacro_t
class GerbvSimplifiedAmacro(Structure):
    pass
GerbvSimplifiedAmacro._fields_ = [('type', c_gerbv_aperture_type_t),
                ('parameter', c_double * APERTURE_PARAMETERS_MAX),
                ('next', POINTER(GerbvSimplifiedAmacro))]

# gerbv_aperture_t
class GerbvAperture(Structure):
    _fields_ = [('type', c_gerbv_aperture_type_t),
                ('amacro', POINTER(GerbvAmacro)),
                ('simplified', POINTER(GerbvSimplifiedAmacro)),
                ('parameter', c_double * APERTURE_PARAMETERS_MAX),
                ('nuf_parameters', c_int),
                ('unit', c_gerbv_unit_t)]

# gerbv_aperture_list_t;
class GerbvApertureList(Structure):
    pass
GerbvApertureList._fields_ = [('number', c_int),
                ('layer', c_int),
                ('count', c_int),
                ('type', c_gerbv_aperture_type_t),
                ('parameter', c_double*5),
                ('next', POINTER(GerbvApertureList))]

# gerbv_stats_t
class GerbvStats(Structure):
    _fields_ = [('error_list', POINTER(GerbvErrorList)),
                ('aperture_list', POINTER(GerbvApertureList)),
                ('D_code_list', POINTER(GerbvApertureList)),
                ('layer_count', c_int),
                ('G0', c_int),
                ('G1', c_int),
                ('G2', c_int),
                ('G3', c_int),
                ('G4', c_int),
                ('G10', c_int),
                ('G11', c_int),
                ('G12', c_int),
                ('G36', c_int),
                ('G37', c_int),
                ('G54', c_int),
                ('G55', c_int),
                ('G70', c_int),
                ('G71', c_int),
                ('G74', c_int),
                ('G75', c_int),
                ('G90', c_int),
                ('G91', c_int),
                ('G_unknown', c_int),
                ('D1', c_int),
                ('D2', c_int),
                ('D3', c_int),
                ('D_unknown', c_int),
                ('D_error', c_int),
                ('M0', c_int),
                ('M1', c_int),
                ('M2', c_int),
                ('M_unknown', c_int),
                ('X', c_int),
                ('Y', c_int),
                ('I', c_int),
                ('J', c_int),
                ('star', c_int),
                ('unknown', c_int)]

# gerbv_drill_list_t
class GerbvDrillList(Structure):
    pass
GerbvDrillList._fields_ = [('drill_num', c_int),
                ('drill_size', c_double),
                ('drill_unit', c_char_p),
                ('drill_count', c_int),
                ('next', POINTER(GerbvDrillList))]

# gerbv_drill_stats_t
class GerbvDrillStats(Structure):
    _fields_ = [('layer_count', c_int),
                ('error_list', POINTER(GerbvErrorList)),
                ('drill_list', POINTER(GerbvDrillList)),
                ('comment', c_int),
                ('F', c_int),
                ('G00', c_int),
                ('G01', c_int),
                ('G02', c_int),
                ('G03', c_int),
                ('G04', c_int),
                ('G05', c_int),
                ('G90', c_int),
                ('G91', c_int),
                ('G93', c_int),
                ('G_unknown', c_int),
                ('M00', c_int),
                ('M01', c_int),
                ('M18', c_int),
                ('M25', c_int),
                ('M30', c_int),
                ('M31', c_int),
                ('M45', c_int),
                ('M47', c_int),
                ('M48', c_int),
                ('M71', c_int),
                ('M72', c_int),
                ('M95', c_int),
                ('M97', c_int),
                ('M98', c_int),
                ('M_unknown', c_int),
                ('R', c_int),
                ('unknown', c_int),
                ('total_count', c_int),
                ('detect', c_char_p)]

# gerbv_selection_item_t
class GerbvSelectionItem(Structure):
    _fields_ = [('image', c_void_p),
                ('net', c_void_p)]

# gerbv_selection_info_t
class GerbvSelectionInfo(Structure):
    _fields_ = [('type', c_gerbv_selection_t),
                ('lowerLeftX', c_double),
                ('lowerLeftY', c_double),
                ('upperRightX', c_double),
                ('upperRightY', c_double),
                ('selectedNodeArray', POINTER(GArray))]

# gerbv_user_transformation_t
class GerbvUserTransformation(Structure):
    _fields_ = [('translateX', c_double),
                ('translateY', c_double),
                ('scaleX', c_double),
                ('scaleY', c_double),
                ('rotation', c_double),
                ('mirrorAroundX', c_gboolean),
                ('mirrorAroundY', c_gboolean),
                ('inverted', c_gboolean)]

# gerbv_render_size_t
class GerbvRenderSize(Structure):
    _fields_ = [('left', c_double),
                ('right', c_double),
                ('bottom', c_double),
                ('top', c_double)]

# gerbv_cirseg_t
class GerbvCirseg(Structure):
    _fields_ = [('cp_x', c_double),
                ('cp_y', c_double),
                ('width', c_double),
                ('height', c_double),
                ('angle1', c_double),
                ('angle2', c_double)]

# gerbv_step_and_repeat_t
class GerbvStepAndRepeat(Structure):
    _fields_ = [('X', c_int),
                ('Y', c_int),
                ('dist_X', c_double),
                ('dist_Y', c_double)]

# gerbv_knockout_t
class GerbvKnockout(Structure):
    _fields_ = [('firstInstance', c_gboolean),
                ('type', c_gerbv_knockout_type_t),
                ('polarity', c_gerbv_polarity_t),
                ('lowerLeftX', c_double),
                ('lowerLeftY', c_double),
                ('width', c_double),
                ('height', c_double),
                ('border', c_double)]

# gerbv_layer_t
class GerbvLayer(Structure):
    _fields_ = [('stepAndRepeat', GerbvStepAndRepeat),
                ('knockout', GerbvKnockout),
                ('rotation', c_double),
                ('polarity', c_gerbv_polarity_t),
                ('name', c_char_p),
                ('next', c_void_p)]

# gerbv_netstate_t
class GerbvNetstate(Structure):
    _fields_ = [('axisSelect', c_gerbv_axis_select_t),
                ('mirrorState', c_gerbv_mirror_state_t),
                ('unit', c_gerbv_unit_t),
                ('offsetA', c_double),
                ('offsetB', c_double),
                ('scaleA', c_double),
                ('scaleB', c_double),
                ('next', c_void_p)]

# gerbv_net_t
class GerbvNet(Structure):
    pass
GerbvNet._fields_ = [('start_x', c_double),
                ('start_y', c_double),
                ('stop_x', c_double),
                ('stop_y', c_double),
                ('boundingBox', GerbvRenderSize),
                ('aperture', c_int),
                ('aperture_state', c_gerbv_aperture_state_t),
                ('interpolation', c_gerbv_interpolation_t),
                ('cirseg', POINTER(GerbvCirseg)),
                ('next', POINTER(GerbvNet)),
                ('label', POINTER(GString)),
                ('layer', POINTER(GerbvLayer)),
                ('state', POINTER(GerbvNetstate))]

# gerbv_format_t
class GerbvFormat(Structure):
    _fields_ = [('omit_zeros', c_gerbv_omit_zeros_t),
                ('coordinate', c_gerbv_coordinate_t),
                ('x_int', c_int),
                ('x_dec', c_int),
                ('y_int', c_int),
                ('y_dec', c_int),
                ('lim_seqno', c_int),
                ('lim_gf', c_int),
                ('lim_pf', c_int),
                ('lim_mf', c_int)]

# gerbv_image_info_t
class GerbvImageInfo(Structure):
    _fields_ = [('name', c_char_p),
                ('polarity', c_gerbv_polarity_t),
                ('min_x', c_double),
                ('min_y', c_double),
                ('max_x', c_double),
                ('max_y', c_double),
                ('offsetA', c_double),
                ('offsetB', c_double),
                ('encoding', c_gerbv_encoding_t),
                ('imageRotation', c_double),
                ('imageJustifyTypeA', c_gerbv_image_justify_type_t),
                ('imageJustifyTypeB', c_gerbv_image_justify_type_t),
                ('imageJustifyOffsetA', c_double),
                ('imageJustifyOffsetB', c_double),
                ('imageJustifyOffsetActualA', c_double),
                ('imageJustifyOffsetActualB', c_double),
                ('plotterFilm', POINTER(c_char)),
                ('type', c_char_p),
                ('attr_list', POINTER(GerbvHIDAttribute)),
                ('n_attr', c_int)]

# gerbv_image_t
class GerbvImage(Structure):
    _fields_ = [('layertype', c_gerbv_layertype_t),
                ('aperture', POINTER(GerbvAperture) * APERTURE_MAX),
                ('layers', POINTER(GerbvLayer)),
                ('states', POINTER(GerbvNetstate)),
                ('amacro', POINTER(GerbvAmacro)),
                ('format', POINTER(GerbvFormat)),
                ('info', POINTER(GerbvImageInfo)),
                ('netlist', POINTER(GerbvNet)),
                ('gerbv_stats', POINTER(GerbvStats)),
                ('drill_stats', POINTER(GerbvDrillStats))]

# gerbv_fileinfo_t
class GerbvFileInfo(Structure):
    _fields_ = [('image', POINTER(GerbvImage)),
                ('color', GdkColor),
                ('alpha', c_uint16),
                ('isVisible', c_gboolean),
                ('privateRenderData', c_void_p),
                ('fullPathname', c_char_p),
                ('name', c_char_p),
                ('transform', GerbvUserTransformation),
                ('layer_dirty', c_gboolean)]

# gerbv_bbox_t
class GerbvBbox(Structure):
    _fields_ = [('x1', c_double),
                ('y1', c_double),
                ('x2', c_double),
                ('y2', c_double)]

# gerbv_project_t
class GerbvProject(Structure):
    _fields_ = [('background', GdkColor),
                ('max_files', c_int),
                ('file', POINTER(POINTER(GerbvFileInfo))),
                ('curr_index', c_int),
                ('last_loaded', c_int),
                ('renderType', c_int),
                ('check_before_delete', c_gboolean),
                ('path', c_char_p),
                ('execpath', c_char_p),
                ('execname', c_char_p),
                ('project', c_char_p)]

# gerbv_layer_color
class GerbvLayerColor(Structure):
    _fields_ = [('red', c_ubyte),
                ('green', c_ubyte),
                ('blue', c_ubyte),
                ('alpha', c_ubyte)]

# gerbv_render_info_t
class GerbvRenderInfo(Structure):
    _fields_ = [('scaleFactorX', c_double),
                ('scaleFactorY', c_double),
                ('lowerLeftX', c_double),
                ('lowerLeftY', c_double),
                ('renderType', c_gerbv_render_types_t),
                ('displayWidth', c_int),
                ('displayHeight', c_int)]
