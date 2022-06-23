# create circular text-image using PIL or Wand (ImageMagik)
# then send this image line by line to the Pico so as not to overwhelm it

# for circular text
# https://stackoverflow.com/questions/68979045/how-can-i-draw-a-curved-text-using-python-converting-text-to-curved-image
# create individual shapes using wand
# then paste these images into a general image
# https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil

# https://www.mfitzp.com/displaying-images-oled-displays/
# to send to the pico convert to .pbm
# then use ampy to push image to pico
# potentially only make smaller images (e.g. 800 x 20 rather than 800 x 400)
# make sure thonny is closed when doing

# 'undefined'

# 'alpha' - Only available with ImageMagick-7

# 'atop'

# 'blend'

# 'blur'

# 'bumpmap'

# 'change_mask'

# 'clear'

# 'color_burn'

# 'color_dodge'

# 'colorize'

# 'copy_black'

# 'copy_blue'

# 'copy'

# 'copy_alpha' - Only available with ImageMagick-7

# 'copy_cyan'

# 'copy_green'

# 'copy_magenta'

# 'copy_opacity' - Only available with ImageMagick-6

# 'copy_red'

# 'copy_yellow'

# 'darken'

# 'darken_intensity'

# 'difference'

# 'displace'

# 'dissolve'

# 'distort'

# 'divide_dst'

# 'divide_src'

# 'dst_atop'

# 'dst'

# 'dst_in'

# 'dst_out'

# 'dst_over'

# 'exclusion'

# 'hard_light'

# 'hard_mix'

# 'hue'

# 'in'

# 'intensity' - Only available with ImageMagick-7

# 'lighten'

# 'lighten_intensity'

# 'linear_burn'

# 'linear_dodge'

# 'linear_light'

# 'luminize'

# 'mathematics'

# 'minus_dst'

# 'minus_src'

# 'modulate'

# 'modulus_add'

# 'modulus_subtract'

# 'multiply'

# 'no'

# 'out'

# 'over'

# 'overlay'

# 'pegtop_light'

# 'pin_light'

# 'plus'

# 'replace'

# 'saturate'

# 'screen'

# 'soft_light'

# 'src_atop'

# 'src'

# 'src_in'

# 'src_out'

# 'src_over'

# 'threshold'

# 'vivid_light'

# 'xor'

# 'stereo'

from ast import operator
from wand.image import Image, COMPOSITE_OPERATORS
from wand.font import Font
from wand.display import display
from wand.drawing import Drawing

# main image is image to paste new text onto - arc amount is 0-360, rotation is -360 to 360, 
def add_arced_text(main_image, text_to_add, arc_amount, rotation_amount, font_size, radius):
    # I'm unsure how to implement a radius?
    temp_image = Image(filename='temp:')
    temp_image.font = Font('Arial', font_size)
    text_v = 'label:'+ text_to_add
    temp_image.read(filename=text_v)
    temp_image.virtual_pixel = 'white'
    temp_image.distort('arc', (arc_amount, rotation_amount))
    main_image.composite(operator='alpha', left=0, top=0, width=main_image.width, height=main_image.height, image = temp_image)
    return main_image

