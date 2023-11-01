#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import os 
from PIL import Image, ImageDraw, ImageOps, ImageFont
from ..categories import icons
from ..config import color_mapping, COLORS
from .graphics_functions import (hex_to_rgb,
                                 get_color_values,
                                 text_panel,
                                 combine_images,
                                 apply_outline_and_border)                                                       

font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

#try:
#    import Markdown
#except ImportError:
#    import pip
#    pip.main(['install', 'Markdown'])

#---------------------------------------------------------------------------------------------------------------------#
        
ALIGN_OPTIONS = ["top", "center", "bottom"]                 
ROTATE_OPTIONS = ["text center", "image center"]
JUSTIFY_OPTIONS = ["left", "center", "right"]
PERSPECTIVE_OPTIONS = ["top", "bottom", "left", "right"]

#---------------------------------------------------------------------------------------------------------------------#

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 
  
#---------------------------------------------------------------------------------------------------------------------#
class CR_SimpleMemeTemplate:
    
    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        bar_opts = ["no bars", "top", "bottom", "top and bottom"]
        colors = COLORS[1:]
        simple_meme_presets = ["custom",
                               "One Does Not Simply ... MEME IN COMFY",
                               "This is fine.",
                               "Good Morning ... No Such Thing!"]        
        
        return {"required": {
                "image": ("IMAGE",),
                "preset": (simple_meme_presets,),   
                "text_top": ("STRING", {"multiline": True, "default": "text_top"}),
                "text_bottom": ("STRING", {"multiline": True, "default": "text_bottom"}),
                "font_name": (file_list,),
                "max_font_size": ("INT", {"default": 150, "min": 20, "max": 500}),
                "font_color": (colors,),
                "font_outline": (["none", "thin", "thick"],),
                "bar_color": (colors,),
                "bar_options": (bar_opts,),
                }        
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_meme"
    CATEGORY = icons.get("Comfyroll/Graphics/Template")

    def make_meme(self, image, preset,
                  text_top, text_bottom,
                  font_name, max_font_size, font_color, font_outline,
                  bar_color, bar_options):

        text_color = color_mapping.get(font_color, (0, 0, 0))  # Default to black if the color is not found
        
        # Convert tensor images
        image_3d = image[0, :, :, :]

        # Calculate the height factor
        if bar_options == "top":
            height_factor = 1.2
        elif bar_options == "bottom":
            height_factor = 1.2
        elif bar_options == "top and bottom":
            height_factor = 1.4
        else:
            height_factor = 1.0
        
        if preset == "One Does Not Simply ... MEME IN COMFY":
            text_top = "One Does Not Simply"
            text_bottom = "MEME IN COMFY"
        if preset == "This is fine.":
            text_top = "This is fine."
            text_bottom = ""            
        if preset == "Good Morning ... No Such Thing!":
            text_top = "Good Morning"
            text_bottom = "\"No Such Thing!\""  
        
        # Create PIL images for the image and text bars
        back_image = tensor2pil(image_3d)   
        size = back_image.width, int(back_image.height * height_factor)
        result_image = Image.new("RGB", size)

        # Define font settings
        #font_file = "fonts\\" + str(font_name)
        font_file = os.path.join("fonts", font_name)
        resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    
        # Create the drawing context
        draw = ImageDraw.Draw(result_image)
 
        # Create two color bars at the top and bottom
        bar_width = back_image.width
        bar_height = back_image.height // 5    ### add parameter for this in adv node
        top_bar = Image.new("RGB", (bar_width, bar_height), bar_color)
        bottom_bar = Image.new("RGB", (bar_width, bar_height), bar_color)

        # Composite the result image onto the input image
        if bar_options == "top" or bar_options == "top and bottom":
            image_out = result_image.paste(back_image, (0, bar_height))
        else:
            image_out = result_image.paste(back_image, (0, 0))
        
        # Get the font size and draw the text
        if bar_options == "top" or bar_options == "top and bottom":
            result_image.paste(top_bar, (0, 0))
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, font_outline)
            
        if bar_options == "bottom" or bar_options == "top and bottom":
            result_image.paste(bottom_bar, (0, (result_image.height - bar_height)))
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            if bar_options == "bottom":
                y_position = back_image.height
            else:
                y_position = bar_height + back_image.height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, font_outline)

        # Overlay text on image
        if bar_options == "bottom" and text_top > "":
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, font_outline)

        if (bar_options == "top" or bar_options == "none") and text_bottom > "":
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            y_position = back_image.height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, font_outline)

        if bar_options == "no bars" and text_bottom > "":
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            y_position = back_image.height - bar_height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, font_outline)

        if bar_options == "no bars" and text_top > "":
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, font_outline)
 
        show_help = """Help:
        
        The two text entry boxes are for the top and bottom text.
        these can be added either on a color bar or as an overlay.
        Both top and bottom text are optional.
        
        Only the first two lines will be used for top and bottom text.
        If you enter more than two lines any additional lines will be ignored.
        
        If you enter both top and bottom text and select a single bar (top or bottom),
        then one of texts will be ouput as overlay text.
        
        If you enter both top and bottom text and select no bars,
        then both texts will be ouput as overlay text."""
        
        image_out = np.array(result_image).astype(np.float32) / 255.0
        image_out = torch.from_numpy(image_out).unsqueeze(0)          
        
        # Convert the PIL image back to a torch tensor
        #return (pil2tensor(image_out), show_help, )
        return (image_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_PageLayout:

    @classmethod
    def INPUT_TYPES(s):

        layout_options = ["header", "footer", "header and footer", "no header or footer"]               
        
        return {"required": {
                "layout_options": (layout_options,),
                "image_panel": ("IMAGE",),
                "header_height": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "header_text": ("STRING", {"multiline": True, "default": "text"}),
                "header_align": (JUSTIFY_OPTIONS, ),
                "footer_height": ("INT", {"default": 0, "min": 0, "max": 1024}), 
                "footer_text": ("STRING", {"multiline": True, "default": "text"}),
                "footer_align": (JUSTIFY_OPTIONS, ),
                "font_name": (file_list,),
                "font_color": (COLORS,),
                "header_font_size": ("INT", {"default": 150, "min": 0, "max": 1024}),
                "footer_font_size": ("INT", {"default": 50, "min": 0, "max": 1024}),
                "border_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "border_color": (COLORS[1:],),                
                "background_color": (COLORS,),
               },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "layout"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def layout(self, layout_options, image_panel,
               border_thickness, border_color, background_color,
               header_height, header_text, header_align,
               footer_height, footer_text, footer_align,
               font_name, font_color,
               header_font_size, footer_font_size,
               font_color_hex='#000000', border_color_hex='#000000', bg_color_hex='#000000'):

        # Get RGB values for the text and background colors    
        font_color = get_color_values(font_color, font_color_hex, color_mapping)
        border_color = get_color_values(border_color, border_color_hex, color_mapping)
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping)
                    
        main_panel = tensor2pil(image_panel)
        
        # Get image width and height        
        image_width = main_panel.width
        image_height = main_panel.height 

        # Set defaults
        margins = 50
        line_spacing = 0
        position_x = 0
        position_y = 0
        align = "center"
        rotation_angle = 0
        rotation_options = "image center"
        
        images = []
        
        ### Create text panels and add to images array       
        if layout_options == "header" or layout_options == "header and footer":
            header_panel = text_panel(image_width, header_height, header_text,
                                      font_name, header_font_size,
                                      font_color, background_color,
                                      margins, line_spacing,
                                      position_x, position_y,
                                      align, header_align,
                                      rotation_angle, rotation_options)
            images.append(header_panel)
        
        images.append(main_panel)
               
        if layout_options == "footer" or layout_options == "header and footer":        
            footer_panel = text_panel(image_width, footer_height, footer_text,
                                      font_name, footer_font_size,
                                      font_color, background_color,
                                      margins, line_spacing,
                                      position_x, position_y,
                                      align, footer_align,
                                      rotation_angle, rotation_options)
            images.append(footer_panel)                                                           
       
        combined_image = combine_images(images, 'vertical')

        # Add a border to the combined image
        if border_thickness > 0:
            combined_image = ImageOps.expand(combined_image, border_thickness, border_color)
            
        show_help = "example help text"

        return (pil2tensor(combined_image), show_help, )    
 
#---------------------------------------------------------------------------------------------------------------------#    
class CR_ImagePanel:

    @classmethod
    def INPUT_TYPES(s):

        directions = ["horizontal", "vertical"]               
        
        return {"required": {
                "image_1": ("IMAGE",),
                "border_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "border_color": (COLORS,),
                "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "outline_color": (COLORS[1:],),
                "layout_direction": (directions,),
               },
                "optional": {
                "image_2": ("IMAGE",), 
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_panel"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_panel(self, image_1,
                   border_thickness, border_color,
                   outline_thickness, outline_color, 
                   layout_direction, image_2=None, image_3=None, image_4=None,
                   border_color_hex='#000000'):

        border_color = get_color_values(border_color, border_color_hex, color_mapping)

        # Convert PIL images to NumPy arrays
        images = []
        #image_1 = image_1[0, :, :, :]
        images.append(tensor2pil(image_1))
        if image_2 is not None:
            #image_2 = image_2[0, :, :, :]
            images.append(tensor2pil(image_2))
        if image_3 is not None:
            #image_3 = image_3[0, :, :, :]
            images.append(tensor2pil(image_3))
        if image_4 is not None:
            #image_4 = image_4[0, :, :, :]
            images.append(tensor2pil(image_4))
            
        # Apply borders and outlines to each image        
        images = apply_outline_and_border(images, outline_thickness, outline_color, border_thickness, border_color)

        combined_image = combine_images(images, layout_direction)

        show_help = "example help text"

        return (pil2tensor(combined_image), show_help, )   

#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageGridPanel:

    @classmethod
    def INPUT_TYPES(s):

        directions = ["horizontal", "vertical"]               
        
        return {"required": {
                    "images": ("IMAGE",),
                    "border_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                    "border_color": (COLORS,),
                    "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                    "outline_color": (COLORS[1:],),
                    "max_columns": ("INT", {"default": 5, "min": 0, "max": 256}), 
                },
                "optional": {
                    "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_panel"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_panel(self, images,
                   border_thickness, border_color,
                   outline_thickness, outline_color, 
                   max_columns, border_color_hex='#000000'):

        border_color = get_color_values(border_color, border_color_hex, color_mapping)

        # Convert PIL images to NumPy arrays
        images = [tensor2pil(image) for image in images]
            
        # Apply borders and outlines to each image
        images = apply_outline_and_border(images, outline_thickness, outline_color, border_thickness, border_color)

        # Calculate dimensions for the grid
        num_images = len(images)
        num_rows = (num_images - 1) // max_columns + 1
        combined_width = max(image.width for image in images) * min(max_columns, num_images)
        combined_height = max(image.height for image in images) * num_rows

        combined_image = Image.new('RGB', (combined_width, combined_height))

        x_offset, y_offset = 0, 0  # Initialize offsets
        for image in images:
            combined_image.paste(image, (x_offset, y_offset))
            x_offset += image.width
            if x_offset >= max_columns * image.width:
                x_offset = 0
                y_offset += image.height

        show_help = "example help text"

        return (pil2tensor(combined_image), show_help, )   

#---------------------------------------------------------------------------------------------------------------------#
class CR_ImageBorder:

    @classmethod
    def INPUT_TYPES(s):
                    
        return {"required": {
                    "image": ("IMAGE",),
                    "top_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "bottom_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "left_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "right_thickness": ("INT", {"default": 0, "min": 0, "max": 4096}),
                    "border_color": (COLORS,),
                    "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 1024}),
                    "outline_color": (COLORS[1:],),
                },
                "optional": {
                    "border_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_panel"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_panel(self, image,
                   top_thickness, bottom_thickness,
                   left_thickness, right_thickness, border_color,
                   outline_thickness, outline_color, 
                   border_color_hex='#000000'):

        images = []

        border_color = get_color_values(border_color, border_color_hex, color_mapping)

        for img in image:
            img = tensor2pil(img)
            
            # Apply the outline
            if outline_thickness > 0:
                img = ImageOps.expand(img, outline_thickness, fill=outline_color)
            
            # Apply the borders
            if left_thickness > 0 or right_thickness > 0 or top_thickness > 0 or bottom_thickness > 0:
                img = ImageOps.expand(img, (left_thickness, top_thickness, right_thickness, bottom_thickness), fill=border_color)
                
            images.append(pil2tensor(img))
        
        images = torch.cat(images, dim=0)                

        show_help = "example help text"

        return (images, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ColorPanel:

    @classmethod
    def INPUT_TYPES(s):
                    
        return {"required": {
                    "panel_width": ("INT", {"default": 512, "min": 8, "max": 4096}),
                    "panel_height": ("INT", {"default": 512, "min": 8, "max": 4096}),
                    "fill_color": (COLORS,),
                },
                "optional": {
                    "fill_color_hex": ("STRING", {"multiline": False, "default": "#000000"})                
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_panel"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def make_panel(self, panel_width, panel_height,
                   fill_color, fill_color_hex='#000000'):

        fill_color = get_color_values(fill_color, fill_color_hex, color_mapping)

        size = (panel_width, panel_height)
        panel = Image.new('RGB', size, fill_color)
        
        show_help = "example help text"

        return (pil2tensor(panel), show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SimpleTextPanel:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {
                "panel_width": ("INT", {"default": 512, "min": 8, "max": 4096}),
                "panel_height": ("INT", {"default": 512, "min": 8, "max": 4096}),
                "text": ("STRING", {"multiline": True, "default": "text"}),
                "font_name": (file_list,),
                "font_color": (COLORS,),
                "font_size": ("INT", {"default": 100, "min": 0, "max": 1024}),
                "background_color": (COLORS,),                
                "align": (ALIGN_OPTIONS, ),
                "justify": (JUSTIFY_OPTIONS, ),
               },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
               }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "layout"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")
    
    def layout(self, panel_width, panel_height,
               text, align, justify,
               font_name, font_color, font_size,
               background_color, 
               font_color_hex='#000000', bg_color_hex='#000000'):

        # Get RGB values for the text and background colors    
        font_color = get_color_values(font_color, font_color_hex, color_mapping)
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping)
        
        # Set defaults
        margins = 50
        line_spacing = 0
        position_x = 0
        position_y = 0
        rotation_angle = 0
        rotation_options = "image center"
        
        ### Create text panels
        
        panel = text_panel(panel_width, panel_height, text,
                           font_name, font_size,
                           font_color, background_color,
                           margins, line_spacing,
                           position_x, position_y,
                           align, justify,
                           rotation_angle, rotation_options)
                                                       
        show_help = "example help text"

        return (pil2tensor(panel), show_help, )    
               
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Simple Meme Template": CR_SimpleMemeTemplate,
    "CR Page Layout": CR_PageLayout,
    "CR Image Grid Panel": CR_ImageGridPanel,
    "CR Image XY Panel": CR_ImageXYPanel,
    "CR Image Border": CR_ImageBorder,
    "CR Color Panel": CR_ColorPanel,
    "CR Simple Text Panel": CR_SimpleTextPanel,
}
'''

