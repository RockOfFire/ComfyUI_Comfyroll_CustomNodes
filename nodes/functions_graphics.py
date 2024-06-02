#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
from ..config import color_mapping

font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]


def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 


def align_text(align, img_height, text_height, text_pos_y, margins):
    if align == "center":
        text_plot_y = img_height / 2 - text_height / 2 + text_pos_y
    elif align == "top":
        text_plot_y = text_pos_y + margins                       
    elif align == "bottom":
        text_plot_y = img_height - text_height + text_pos_y - margins 
    return text_plot_y        


def justify_text(justify, img_width, line_width, margins):
    if justify == "left":
        text_plot_x = 0 + margins
    elif justify == "right":
        text_plot_x = img_width - line_width - margins
    elif justify == "center":
        text_plot_x = img_width/2 - line_width/2
    return text_plot_x   


def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)

    # Calculate the text width and height
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return text_width, text_height


def draw_masked_text(text_mask, text,
                     font_name, font_size,
                     margins, line_spacing,
                     position_x, position_y, 
                     align, justify,
                     rotation_angle, rotation_options):
    
    # Create the drawing context        
    draw = ImageDraw.Draw(text_mask)

    # Define font settings
    font_folder = "fonts"
    font_file = os.path.join(font_folder, font_name)
    resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    font = ImageFont.truetype(str(resolved_font_path), size=font_size) 

     # Split the input text into lines
    text_lines = text.split('\n')

    # Calculate the size of the text plus padding for the tallest line
    max_text_width = 0
    max_text_height = 0

    for line in text_lines:
        # Calculate the width and height of the current line
        line_width, line_height = get_text_size(draw, line, font)
 
        line_height = line_height + line_spacing
        max_text_width = max(max_text_width, line_width)
        max_text_height = max(max_text_height, line_height)
    
    # Get the image width and height
    image_width, image_height = text_mask.size
    image_center_x = image_width / 2
    image_center_y = image_height / 2

    text_pos_y = position_y
    sum_text_plot_y = 0
    text_height = max_text_height * len(text_lines)

    for line in text_lines:
        # Calculate the width of the current line
        line_width, _ = get_text_size(draw, line, font)
                            
        # Get the text x and y positions for each line                                     
        text_plot_x = position_x + justify_text(justify, image_width, line_width, margins)
        text_plot_y = align_text(align, image_height, text_height, text_pos_y, margins)
        
        # Add the current line to the text mask
        draw.text((text_plot_x, text_plot_y), line, fill=255, font=font)
        
        text_pos_y += max_text_height  # Move down for the next line
        sum_text_plot_y += text_plot_y     # Sum the y positions

    # Calculate centers for rotation
    text_center_x = text_plot_x + max_text_width / 2
    text_center_y = sum_text_plot_y / len(text_lines)

    if rotation_options == "text center":
        rotated_text_mask = text_mask.rotate(rotation_angle, center=(text_center_x, text_center_y))
    elif rotation_options == "image center":    
        rotated_text_mask = text_mask.rotate(rotation_angle, center=(image_center_x, image_center_y))
        
    return rotated_text_mask        

def draw_text_on_image(draw, y_position, bar_width, bar_height, text, font, text_color, font_outline):

        # Calculate the width and height of the text
        text_width, text_height = get_text_size(draw, text, font)
       
        if font_outline == "thin":
            outline_thickness = text_height // 40
        elif font_outline == "thick":
            outline_thickness = text_height // 20
        elif font_outline == "extra thick":
            outline_thickness = text_height // 10            
            
        outline_color = (0, 0, 0)
        
        text_lines = text.split('\n')
        
        if len(text_lines) == 1:
            x = (bar_width - text_width) // 2
            y = y_position + (bar_height - text_height) // 2 - (bar_height * 0.10)
            if font_outline == "none":
                draw.text((x, y), text, fill=text_color, font=font)
            else:    
                draw.text((x, y), text, fill=text_color, font=font, stroke_width=outline_thickness, stroke_fill='black')
        elif len(text_lines) > 1:
            # Calculate the width and height of the text
            text_width, text_height = get_text_size(draw, text_lines[0], font)
            
            x = (bar_width - text_width) // 2
            y = y_position + (bar_height - text_height * 2) // 2 - (bar_height * 0.15)
            if font_outline == "none":
                draw.text((x, y), text_lines[0], fill=text_color, font=font)
            else:    
                draw.text((x, y), text_lines[0], fill=text_color, font=font, stroke_width=outline_thickness, stroke_fill='black')   

            # Calculate the width and height of the text
            text_width, text_height = get_text_size(draw, text_lines[1], font)          
            
            x = (bar_width - text_width) // 2
            y = y_position + (bar_height - text_height * 2) // 2 + text_height  - (bar_height * 0.00)         
            if font_outline == "none":
                draw.text((x, y), text_lines[1], fill=text_color, font=font)
            else:    
                draw.text((x, y), text_lines[1], fill=text_color, font=font, stroke_width=outline_thickness, stroke_fill='black')


def get_font_size(draw, text, max_width, max_height, font_path, max_font_size):

    # Adjust the max-width to allow for start and end padding
    max_width = max_width * 0.9
    
    # Start with the maximum font size
    font_size = max_font_size
    font = ImageFont.truetype(str(font_path), size=font_size)

     # Get the first two lines
    text_lines = text.split('\n')[:2]
    
    if len(text_lines) == 2:
        font_size = min(max_height//2, max_font_size)        
        font = ImageFont.truetype(str(font_path), size=font_size)
        
    # Calculate max text width and height with the current font
    max_text_width = 0
    longest_line = text_lines[0]
    for line in text_lines:
        # Calculate the width and height of the current line
        line_width, line_height = get_text_size(draw, line, font)
        
        if line_width > max_text_width:
            longest_line = line
        max_text_width = max(max_text_width, line_width)             
    
    # Calculate the width and height of the text
    text_width, text_height = get_text_size(draw, text, font)
    
    # Decrease the font size until it fits within the bounds
    while max_text_width > max_width or text_height > 0.88 * max_height / len(text_lines):
        font_size -= 1
        font = ImageFont.truetype(str(font_path), size=font_size)
        max_text_width, text_height = get_text_size(draw, longest_line, font)
    
    return font


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Remove the '#' character, if present
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def text_panel(image_width, image_height, text,
              font_name, font_size, font_color,
              font_outline_thickness, font_outline_color,
              background_color,
              margins, line_spacing,
              position_x, position_y,
              align, justify,
              rotation_angle, rotation_options):

    """
    Create an image with text overlaid on a background.
    
    Returns:
    PIL.Image.Image: Image with text overlaid on the background.
    """
    
    # Create PIL images for the text and background layers and text mask
    size = (image_width, image_height)
    panel = Image.new('RGB', size, background_color)

    # Draw the text on the text mask
    image_out = draw_text(panel, text,
                          font_name, font_size, font_color,
                          font_outline_thickness, font_outline_color,
                          background_color,
                          margins, line_spacing,
                          position_x, position_y,
                          align, justify,
                          rotation_angle, rotation_options)
  
    return image_out     


def draw_text(panel, text,
              font_name, font_size, font_color,
              font_outline_thickness, font_outline_color,
              bg_color,
              margins, line_spacing,
              position_x, position_y, 
              align, justify,
              rotation_angle, rotation_options):
    
    # Create the drawing context        
    draw = ImageDraw.Draw(panel)

    # Define font settings
    font_folder = "fonts"
    font_file = os.path.join(font_folder, font_name)
    resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    font = ImageFont.truetype(str(resolved_font_path), size=font_size) 

     # Split the input text into lines
    text_lines = text.split('\n')

    # Calculate the size of the text plus padding for the tallest line
    max_text_width = 0
    max_text_height = 0

    for line in text_lines:
        # Calculate the width and height of the current line
        line_width, line_height = get_text_size(draw, line, font)      
        
        line_height = line_height + line_spacing
        max_text_width = max(max_text_width, line_width)
        max_text_height = max(max_text_height, line_height)
    
    # Get the image center
    image_center_x = panel.width / 2
    image_center_y = panel.height / 2

    text_pos_y = position_y
    sum_text_plot_y = 0
    text_height = max_text_height * len(text_lines)

    for line in text_lines:
        # Calculate the width and height of the current line
        line_width, line_height = get_text_size(draw, line, font)            
                            
        # Get the text x and y positions for each line                                     
        text_plot_x = position_x + justify_text(justify, panel.width, line_width, margins)
        text_plot_y = align_text(align, panel.height, text_height, text_pos_y, margins)
        
        # Add the current line to the text mask
        draw.text((text_plot_x, text_plot_y), line, fill=font_color, font=font, stroke_width=font_outline_thickness, stroke_fill=font_outline_color)

        text_pos_y += max_text_height  # Move down for the next line
        sum_text_plot_y += text_plot_y     # Sum the y positions

    text_center_x = text_plot_x + max_text_width / 2
    text_center_y = sum_text_plot_y / len(text_lines)

    if rotation_options == "text center":
        rotated_panel = panel.rotate(rotation_angle, center=(text_center_x, text_center_y), resample=Image.BILINEAR)
    elif rotation_options == "image center":    
        rotated_panel = panel.rotate(rotation_angle, center=(image_center_x, image_center_y), resample=Image.BILINEAR)
        
    return rotated_panel


def combine_images(images, layout_direction='horizontal'):
    """
    Combine a list of PIL Image objects either horizontally or vertically.

    Args:
    images (list of PIL.Image.Image): List of PIL Image objects to combine.
    layout_direction (str): 'horizontal' for horizontal layout, 'vertical' for vertical layout.

    Returns:
    PIL.Image.Image: Combined image.
    """

    if layout_direction == 'horizontal':
        combined_width = sum(image.width for image in images)
        combined_height = max(image.height for image in images)
    else:
        combined_width = max(image.width for image in images)
        combined_height = sum(image.height for image in images)

    combined_image = Image.new('RGB', (combined_width, combined_height))

    x_offset = 0
    y_offset = 0  # Initialize y_offset for vertical layout
    for image in images:
        combined_image.paste(image, (x_offset, y_offset))
        if layout_direction == 'horizontal':
            x_offset += image.width
        else:
            y_offset += image.height

    return combined_image


def apply_outline_and_border(images, outline_thickness, outline_color, border_thickness, border_color):
    for i, image in enumerate(images):
        # Apply the outline
        if outline_thickness > 0:
            image = ImageOps.expand(image, outline_thickness, fill=outline_color)
        
        # Apply the border
        if border_thickness > 0:
            image = ImageOps.expand(image, border_thickness, fill=border_color)

        images[i] = image
    
    return images


def get_color_values(color, color_hex, color_mapping):
    
    #Get RGB values for the text and background colors.

    if color == "custom":
        color_rgb = hex_to_rgb(color_hex)
    else:
        color_rgb = color_mapping.get(color, (0, 0, 0))  # Default to black if the color is not found

    return color_rgb 


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Remove the '#' character, if present
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def crop_and_resize_image(image, target_width, target_height):
    width, height = image.size
    aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height

    if aspect_ratio > target_aspect_ratio:
        # Crop the image's width to match the target aspect ratio
        crop_width = int(height * target_aspect_ratio)
        crop_height = height
        left = (width - crop_width) // 2
        top = 0
    else:
        # Crop the image's height to match the target aspect ratio
        crop_height = int(width / target_aspect_ratio)
        crop_width = width
        left = 0
        top = (height - crop_height) // 2
        
    # Perform the center cropping
    cropped_image = image.crop((left, top, left + crop_width, top + crop_height))
    
    return cropped_image


def create_and_paste_panel(page, border_thickness, outline_thickness,
                           panel_width, panel_height, page_width,
                           panel_color, bg_color, outline_color,
                           images, i, j, k, len_images, reading_direction):
    panel = Image.new("RGB", (panel_width, panel_height), panel_color)
    if k < len_images:
        img = images[k]
        image = crop_and_resize_image(img, panel_width, panel_height)
        image.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
        panel.paste(image, (0, 0))
    panel = ImageOps.expand(panel, border=outline_thickness, fill=outline_color)
    panel = ImageOps.expand(panel, border=border_thickness, fill=bg_color)
    new_panel_width, new_panel_height = panel.size
    if reading_direction == "right to left":
        page.paste(panel, (page_width - (j + 1) * new_panel_width, i * new_panel_height))
    else:
        page.paste(panel, (j * new_panel_width, i * new_panel_height))


def reduce_opacity(img, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    else:
        img = img.copy()
    alpha = img.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    img.putalpha(alpha)
    return img
    

def random_hex_color():
    # Generate three random values for RGB
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Convert RGB to hex format
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return hex_color    


def random_rgb():
    # Generate three random values for RGB
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Format RGB as a string in the format "128,128,128"
    rgb_string = "{},{},{}".format(r, g, b)

    return rgb_string


def make_grid_panel(images, max_columns, color=0):

    # Calculate dimensions for the grid
    num_images = len(images)
    num_rows = (num_images - 1) // max_columns + 1
    combined_width = max(image.width for image in images) * min(max_columns, num_images)
    combined_height = max(image.height for image in images) * num_rows

    combined_image = Image.new('RGB', (combined_width, combined_height), color=color)

    x_offset, y_offset = 0, 0  # Initialize offsets
    for image in images:
        combined_image.paste(image, (x_offset, y_offset))
        x_offset += image.width
        if x_offset >= max_columns * image.width:
            x_offset = 0
            y_offset += image.height

    return combined_image   


def interpolate_color(color0, color1, t):
    """
    Interpolate between two colors.
    """
    return tuple(int(c0 * (1 - t) + c1 * t) for c0, c1 in zip(color0, color1))
    