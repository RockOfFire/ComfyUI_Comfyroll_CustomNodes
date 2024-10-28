#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import torch
import numpy as np
import os
import sys
import folder_paths
import re
import comfy.sd
import csv
import math
import random
from PIL import Image, ImageSequence
from pathlib import Path
from itertools import product
from ..categories import icons

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 

def tensor2rgba(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t.unsqueeze(3).repeat(1, 1, 1, 4)
    elif size[3] == 1:
        return t.repeat(1, 1, 1, 4)
    elif size[3] == 3:
        alpha_tensor = torch.ones((size[0], size[1], size[2], 1))
        return torch.cat((t, alpha_tensor), dim=3)
    else:
        return t

class AnyType(str):
    """A special type that can be connected to any other types. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

def get_input_folder(input_folder, input_path):
    # Set the input path
    if input_path != '' and input_path is not None:
        if not os.path.exists(input_path):
            print(f"[Warning] CR Image List: The input_path `{input_path}` does not exist")
            return ("",)  
        in_path = input_path
    else:
        input_dir = folder_paths.input_directory
        in_path = os.path.join(input_dir, input_folder)
    return in_path    

#---------------------------------------------------------------------------------------------------------------------#
# List Nodes                
#---------------------------------------------------------------------------------------------------------------------#
class CR_TextList:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {"multiline_text": ("STRING", {"multiline": True, "default": "text"}),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                             "max_rows": ("INT", {"default": 1000, "min": 1, "max": 9999}),
                            }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, multiline_text, start_index, max_rows):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-text-list"

        lines = multiline_text.split('\n')

        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(lines) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_rows, len(lines))

        # Extract the desired portion of the list
        selected_rows = lines[start_index:end_index]
          
        return (selected_rows, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_PromptList:

    @classmethod
    def INPUT_TYPES(s):
    
        return {"required": {"prepend_text": ("STRING", {"multiline": False, "default": ""}),
                             "multiline_text": ("STRING", {"multiline": True, "default": "body_text"}),
                             "append_text": ("STRING", {"multiline": False, "default": ""}),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                             "max_rows": ("INT", {"default": 1000, "min": 1, "max": 9999}),
                            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", )
    RETURN_NAMES = ("prompt", "body_text", "show_help", )
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, multiline_text, prepend_text="", append_text="", start_index=0, max_rows=9999):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-prompt-list"

        lines = multiline_text.split('\n')

        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(lines) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_rows, len(lines))

        # Extract the desired portion of the list
        selected_rows = lines[start_index:end_index]
        prompt_list_out = [prepend_text + line + append_text for line in selected_rows]
        body_list_out = selected_rows          

        return (prompt_list_out, body_list_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadImageList:

    @classmethod
    def INPUT_TYPES(s):
    
        input_dir = folder_paths.input_directory
        image_folder = [name for name in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,name))] 
    
        return {"required": {"input_folder": (sorted(image_folder), ),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                             "max_images": ("INT", {"default": 1, "min": 1, "max": 9999}),
               },
               "optional": {"input_path": ("STRING", {"default": '', "multiline": False}),     
               }
        }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("IMAGE", "show_help", )
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List/IO")

    def make_list(self, start_index, max_images, input_folder, input_path=None):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-image-list"

        # Set the input path
        if input_path != '' and input_path is not None:
            if not os.path.exists(input_path):
                print(f"[Warning] CR Image List: The input_path `{input_path}` does not exist")
                return ("",)  
            in_path = input_path
        else:
            input_dir = folder_paths.input_directory
            in_path = os.path.join(input_dir, input_folder)

        # Check if the folder is empty
        if not os.listdir(in_path):
            print(f"[Warning] CR Image List: The folder `{in_path}` is empty")
            return None

        file_list = sorted(os.listdir(in_path), key=lambda s: sum(((s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)), ()))
        
        image_list = []
        
        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(file_list) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_images, len(file_list) - 1)
                    
        for num in range(start_index, end_index):
            img = Image.open(os.path.join(in_path, file_list[num]))
            image = img.convert("RGB")
            image_list.append(pil2tensor(image))
        
        if not image_list:
            # Handle the case where the list is empty
            print("CR Load Image List: No images found.")
            return None
            
        images = torch.cat(image_list, dim=0)
        images_out = [images[i:i + 1, ...] for i in range(images.shape[0])]

        return (images_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadImageListPlus:

    @classmethod
    def INPUT_TYPES(s):
    
        input_dir = folder_paths.input_directory
        image_folder = [name for name in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,name))] 
    
        return {"required": {"input_folder": (sorted(image_folder), ),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 99999}),
                             "max_images": ("INT", {"default": 1, "min": 1, "max": 99999}),
               },
               "optional": {"input_path": ("STRING", {"default": '', "multiline": False}),     
               }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT", "STRING", "INT", "INT", "INT", "STRING", )
    RETURN_NAMES = ("IMAGE", "MASK", "index", "filename", "width", "height", "list_length", "show_help", )
    OUTPUT_IS_LIST = (True, True, True, True, False, False, False, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List/IO")

    def make_list(self, start_index, max_images, input_folder, input_path=None, vae=None):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-image-list-plus"

        # Set the input path
        if input_path != '' and input_path is not None:
            if not os.path.exists(input_path):
                print(f"[Warning] CR Image List: The input_path `{input_path}` does not exist")
                return ("",)  
            in_path = input_path
        else:
            input_dir = folder_paths.input_directory
            in_path = os.path.join(input_dir, input_folder)

        # Check if the folder is empty
        if not os.listdir(in_path):
            print(f"[Warning] CR Image List: The folder `{in_path}` is empty")
            return None

        file_list = sorted(os.listdir(in_path), key=lambda s: sum(((s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)), ()))
        
        image_list = []
        mask_list = []
        index_list = []        
        filename_list = []
        exif_list = []         
        
        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(file_list) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_images, len(file_list) - 1)
                    
        for num in range(start_index, end_index):
            filename = file_list[num]
            img_path = os.path.join(in_path, filename)
            
            img = Image.open(os.path.join(in_path, file_list[num]))            
            image_list.append(pil2tensor(img.convert("RGB")))
            
            tensor_img = pil2tensor(img)
            mask_list.append(tensor2rgba(tensor_img)[:,:,:,0])
           
            # Populate the image index
            index_list.append(num)

            # Populate the filename_list
            filename_list.append(filename)
            
        if not image_list:
            # Handle the case where the list is empty
            print("CR Load Image List: No images found.")
            return None

        width, height = Image.open(os.path.join(in_path, file_list[start_index])).size
            
        images = torch.cat(image_list, dim=0)
        images_out = [images[i:i + 1, ...] for i in range(images.shape[0])]

        masks = torch.cat(mask_list, dim=0)
        mask_out = [masks[i:i + 1, ...] for i in range(masks.shape[0])]
        
        list_length = end_index - start_index
        
        return (images_out, mask_out, index_list, filename_list, index_list, width, height, list_length, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadGIFAsList:
   
    @classmethod
    def INPUT_TYPES(cls):
    
        input_dir = folder_paths.input_directory
        image_folder = [name for name in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,name))] 
    
        return {"required": {"input_folder": (sorted(image_folder), ),
                             "gif_filename": ("STRING", {"multiline": False, "default": "text"}),
                             "start_frame": ("INT", {"default": 0, "min": 0, "max": 99999}),
                             "max_frames": ("INT", {"default": 1, "min": 1, "max": 99999}),                              
                            },                    
                "optional": {"input_path": ("STRING", {"default": '', "multiline": False}),     
                }    
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", )
    RETURN_NAMES = ("IMAGE", "MASK", "show_help", )
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "load_gif"
    CATEGORY = icons.get("Comfyroll/List/IO")
 
    def load_gif(self, input_folder, gif_filename, start_frame, max_frames, input_path=None):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-load-gif-images"
      
        # Set the input path
        if input_path != '' and input_path is not None:
            if not os.path.exists(input_path):
                print(f"[Warning] CR Image List: The input_path `{input_path}` does not exist")
                return ("",)  
            in_path = input_path
        else:
            input_dir = folder_paths.input_directory
            in_path = os.path.join(input_dir, input_folder)
  
        # Construct the GIF file path
        gif_file_path = os.path.join(in_path, gif_filename) 
  
        frames_list = []
        masks_list = []
         
        try:
            # Open the GIF file
            with Image.open(gif_file_path) as gif_image:
                   
                for i, frame in enumerate(ImageSequence.Iterator(gif_image)):
                    if i < start_frame:
                        continue  # Skip frames until reaching the start_frame

                    if max_frames is not None and i >= start_frame + max_frames:
                        break  # Stop after max_frames frames

                    # Extract frame
                    img = frame.copy()
                    width, height = img.size
                    frames_list.append(pil2tensor(img.convert("RGB")))
                        
                    tensor_img = pil2tensor(img)                   
                    masks_list.append(tensor2rgba(tensor_img)[:,:,:,0])
                        
            # Convert frames to tensor list
            images = torch.cat(frames_list, dim=0)
            images_out = [images[i:i + 1, ...] for i in range(images.shape[0])]

            # Convert masks to tensor list
            masks = torch.cat(masks_list, dim=0)
            masks_out = [masks[i:i + 1, ...] for i in range(masks.shape[0])]                        

            return (images_out, masks_out, show_help, )

        except Exception as e:
            print(f"Error: {e}")
            return (None, None, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_FontFileList:

    @classmethod
    def INPUT_TYPES(s):
    
        comfyroll_font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        comfyroll_file_list = [f for f in os.listdir(comfyroll_font_dir) if os.path.isfile(os.path.join(comfyroll_font_dir, f)) and f.lower().endswith(".ttf")]

        sources = ["system", "Comfyroll", "from folder"]
        
        return {"required": {"source_folder": (sources,),
                             "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                             "max_rows": ("INT", {"default": 1000, "min": 1, "max": 9999}),                            
                            },
                "optional": {"folder_path": ("STRING", {"default": "C:\Windows\Fonts", "multiline": False}),
                }
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("LIST", "show_help", )
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "make_list"
    CATEGORY = icons.get("Comfyroll/List/IO")

    def make_list(self, source_folder, start_index, max_rows, folder_path="C:\Windows\Fonts"):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-font-file-list"

        if source_folder == "system":
            system_root = os.environ.get('SystemRoot')
            system_font_dir = os.path.join(system_root, 'Fonts')   
            file_list = [f for f in os.listdir(system_font_dir) if os.path.isfile(os.path.join(system_font_dir, f)) and f.lower().endswith(".ttf")]
        elif source_folder == "Comfyroll":
            comfyroll_font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
            file_list = [f for f in os.listdir(comfyroll_font_dir) if os.path.isfile(os.path.join(comfyroll_font_dir, f)) and f.lower().endswith(".ttf")]
        elif source_folder == "from folder":
            if folder_path != '' and folder_path is not None:
                if not os.path.exists(folder_path):
                    print(f"[Warning] CR Font File List: The folder_path `{folder_path}` does not exist")
                    return None
                font_dir = folder_path     
                file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
            else:    
                print(f"[Warning] CR Font File List: No folder_path entered")
                return None                
        else:
            pass

        # Ensure start_index is within the bounds of the list
        start_index = max(0, min(start_index, len(file_list) - 1))

        # Calculate the end index based on max_rows
        end_index = min(start_index + max_rows, len(file_list))

        # Extract the desired portion of the list
        selected_files = file_list[start_index:end_index]

        return (selected_files, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_FloatRangeList:

    @classmethod
    def INPUT_TYPES(s):
    
        operations = ["none","sin","cos","tan"]
        
        return {"required": {"start": ("FLOAT", {"default": 0.00, "min": -99999.99, "max": 99999.99, "step": 0.01}),
                             "end": ("FLOAT", {"default": 1.00, "min": -99999.99, "max": 99999.99, "step": 0.01}),
                             "step": ("FLOAT", {"default": 1.00, "min": -99999.99, "max": 99999.99, "step": 0.01}),
                             "operation": (operations, ),
                             "decimal_places": ("INT", {"default": 2, "min": 0, "max": 10}),
                             "ignore_first_value": ("BOOLEAN", {"default": True}),
                             "max_values_per_loop": ("INT", {"default": 128, "min": 1, "max": 99999}),                              
                             "loops": ("INT", {"default": 1, "min": 1, "max": 999}),
                             "ping_pong": ("BOOLEAN", {"default": False}),
                            },
        }                        

    RETURN_TYPES = ("FLOAT", "STRING",)
    RETURN_NAMES = ("FLOAT", "show_help", )    
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = 'make_range'
    CATEGORY = icons.get("Comfyroll/List")

    def make_range(self, start, end, step, max_values_per_loop, operation, decimal_places, ignore_first_value, loops, ping_pong):
            
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-float-range-list"      
        
        range_values = list()
        
        for i in range(loops):
        
            if end < start and step > 0:
                step = -step
                
            current_range = list(np.arange(start, end + step, step))

            # Apply math operations to each value in the range
            if operation == "sin":
                current_range = [math.sin(value) for value in current_range]
            elif operation == "cos":
                current_range = [math.cos(value) for value in current_range]    
            elif operation == "tan":
                current_range = [math.tan(value) for value in current_range]  
            
            current_range = [round(value, decimal_places) for value in current_range]  
            
            if ping_pong:
                # Reverse the direction of the range on even iterations
                if i % 2 == 1:
                    if ignore_first_value:
                        current_range = current_range[:-1]
                    current_range = current_range[:max_values_per_loop]
                    range_values += reversed(current_range)
                else:
                    if ignore_first_value:
                        current_range = current_range[1:]
                    current_range = current_range[:max_values_per_loop]
                    range_values += current_range  
            else:
                if ignore_first_value:
                    current_range = current_range[1:]
                current_range = current_range[:max_values_per_loop]
                range_values += current_range
                    
        return (range_values, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_IntegerRangeList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"start": ("INT", {"default": 0, "min": -99999, "max": 99999}),
                             "end": ("INT", {"default": 0, "min": -99999, "max": 99999}),
                             "step": ("INT", {"default": 1, "min": 1, "max": 99999}),
                             "loops": ("INT", {"default": 1, "min": 1, "max": 999}),
                             "ping_pong": ("BOOLEAN", {"default": False}),
                            },
        }
        
    RETURN_TYPES = ("INT", "STRING",)
    RETURN_NAMES = ("INT", "show_help", )    
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = 'make_range'
    CATEGORY = icons.get("Comfyroll/List")

    def make_range(self, start, end, step, loops, ping_pong):
        
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-list-schedule"      
    
        range_values = list()
        for i in range(loops):
            current_range = list(range(start, end, step))
            
            if ping_pong:
                # Reverse the direction of the range on even iterations
                if i % 2 == 1:
                    range_values += reversed(current_range)
                else:
                    range_values += current_range     
            else:
                range_values += current_range           

        return (range_values, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_LoadTextList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                        "input_file_path": ("STRING", {"multiline": False, "default": ""}),
                        "file_name": ("STRING", {"multiline": False, "default": ""}),
                        "file_extension": (["txt", "csv"],),
                        }
        }
        
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("STRING", "show_help", ) 
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = 'load_list'
    CATEGORY = icons.get("Comfyroll/List")

    def load_list(self, input_file_path, file_name, file_extension):
           
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-load-value-list"      

        filepath = input_file_path + "\\" + file_name + "." + file_extension
        print(f"CR Load Values: Loading {filepath}")

        list = []
            
        if file_extension == "csv":
            with open(filepath, "r") as csv_file:
                for row in csv_file:
                    list.append(row)
                    
        elif file_extension == "txt":
            with open(filepath, "r") as txt_file:
                for row in txt_file:
                    list.append(row)
        else:
            pass
        
        return(list, show_help, )        

#---------------------------------------------------------------------------------------------------------------------#
class CR_IntertwineLists:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                            "list1": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                            "list2": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                            }              
        }
        
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("STRING", "show_help", )  
    OUTPUT_IS_LIST = (True, False)      
    FUNCTION = 'make_list'
    CATEGORY = icons.get("Comfyroll/List/Utils")

    def make_list(self, list1, list2):
           
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-intertwine-lists"      

        # Ensure both lists have the same length
        min_length = min(len(list1), len(list2))
        
         # Initialize an empty list to store the combined elements
        combined_list = []
        
        combined_element = str(list1) + ", " + str(list2)
        combined_list.append(combined_element)
        
        return(combined_list, show_help, )            

#---------------------------------------------------------------------------------------------------------------------#
class CR_BinaryToBitList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                        "bit_string": ("STRING", {"multiline": True, "default": ""}),
                        }
        }
        
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("STRING", "show_help", )  
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = 'make_list'
    CATEGORY = icons.get("Comfyroll/List")

    def make_list(self, bit_string):
           
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-binary-to-list" 
        
        list_out = [str(bit) for bit in bit_string]

        return(list_out, show_help, ) 

#---------------------------------------------------------------------------------------------------------------------#
class CR_MakeBatchFromImageList:
# based on ImageListToImageBatch by DrLtData

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"image_list": ("IMAGE", ),}}

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image_batch", "show_help", ) 
    INPUT_IS_LIST = True
    FUNCTION = "make_batch"
    CATEGORY = icons.get("Comfyroll/List/Utils")
   
    def make_batch(self, image_list):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-binary-to-list" 
    
        if len(image_list) <= 1:
            return (image_list,)
            
        batched_images = torch.cat(image_list, dim=0)    

        return (batched_images, show_help, )            

#---------------------------------------------------------------------------------------------------------------------# 
class CR_TextListToString:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                "text_list": ("STRING", {"forceInput": True}),
                    },
                }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("STRING", "show_help", )
    INPUT_IS_LIST = True    
    FUNCTION = "joinlist"
    CATEGORY = icons.get("Comfyroll/List/Utils")

    def joinlist(self, text_list):
    
        string_out = "\n".join(text_list)

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-text-list-to-string"

        return (string_out, show_help, )
 
#---------------------------------------------------------------------------------------------------------------------#
class CR_SimpleList:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "list_values": ("STRING", {"multiline": True, "default": "text"}),              
                    }
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("LIST", "show_help", ) 
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "cross_join"
    CATEGORY = icons.get("Comfyroll/List") 
    
    def cross_join(self, list_values):

        lines = list_values.split('\n')

        list_out = [i.strip() for i in lines if i.strip()]

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-simple-list"

        return (list_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_XYProduct:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "text_x": ("STRING", {"multiline": True}),              
                    "text_y": ("STRING", {"multiline": True}),
                    }
        }

    RETURN_TYPES = (any_type, any_type, "STRING", )
    RETURN_NAMES = ("x_values", "y_values", "show_help", ) 
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "cross_join"
    CATEGORY = icons.get("Comfyroll/List/Utils") 
    
    def cross_join(self, text_x, text_y):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-xy-product"
        
        list1 = text_x.strip().split('\n')
        list2 = text_y.strip().split('\n')

        cartesian_product = list(product(list1, list2))
        x_values, y_values = zip(*cartesian_product)
        
        return (list(x_values), list(y_values), show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_Repeater:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "input_data": (any_type, ),             
                    "repeats": ("INT", {"default": 1, "min": 1, "max": 99999}),
                    }
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("list", "show_help", ) 
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "repeat_list_items"
    CATEGORY = icons.get("Comfyroll/List/Utils") 
        
    def repeat_list_items(self, input_data, repeats):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-repeater"
        
        new_list = []
        
        if isinstance(input_data, list):
            new_list = []
            for item in input_data:
                new_list.extend([item] * repeats)
            return (new_list, show_help, )
        else:
            return ([input_data] * repeats, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_TextCycler:
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("STRING", {"multiline": True, "default": ""}),
            "repeats": ("INT", {"default": 1, "min": 1, "max": 99999}),
            "loops": ("INT", {"default": 1, "min": 1, "max": 99999}),
            }
        }

    RETURN_TYPES = (any_type, "STRING", )
    RETURN_NAMES = ("STRING", "show_text", )
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "cycle"
    CATEGORY = icons.get("Comfyroll/List")    

    def cycle(self, text, repeats, loops=1):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-text-cycler"
    
        lines = text.split('\n')
        list_out = []

        for i in range(loops):
            for text_item in lines:
                for _ in range(repeats):
                    list_out.append(text_item)
        
        return (list_out, show_help,)

#---------------------------------------------------------------------------------------------------------------------#
class CR_ValueCycler:
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "values": ("STRING", {"multiline": True, "default": ""}),
            "repeats": ("INT", {"default": 1, "min": 1, "max": 99999}),
            "loops": ("INT", {"default": 1, "min": 1, "max": 99999}),
            }
        }

    RETURN_TYPES = ("FLOAT", "INT", "STRING", )
    RETURN_NAMES = ("FLOAT", "INT", "show_text", )
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "cycle"
    CATEGORY = icons.get("Comfyroll/List")    

    def cycle(self, values, repeats, loops=1):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-value-cycler"
    
        lines = values.split('\n')
        float_list_out = []
        int_list_out = []

        # add check if valid number

        for i in range(loops):
            for _ in range(repeats):
                for text_item in lines:
                    if all(char.isdigit() or char == '.' for char in text_item.strip()):
                        float_list_out.append(float(text_item))
                        int_list_out.append(int(float(text_item)))  # Convert to int after parsing as float

        return (float_list_out, int_list_out, show_help, )    

#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    ### List nodes
    "CR Text List": CR_TextList,
    "CR Prompt List": CR_PromptList,   
    "CR Simple List": CR_SimpleList,    
    "CR Load Image List": CR_LoadImageList,
    "CR Load Image List Plus": CR_LoadImageListPlus,
    "CR Load GIF As List": CR_LoadGIFAsList,
    "CR Float Range List": CR_FloatRangeList,    
    "CR Integer Range List": CR_FloatRangeList,
    "CR Load Text List": CR_LoadTextList,
    "CR Font File List": CR_FontFileList,
    "CR Binary To Bit List": CR_BinaryToBitList,
    "CR Text Cycler": CR_TextCycler,
    "CR Value Cycler": CR_ValueCycler,     
    ### List Utils
    "CR Batch Images From List": CR_MakeBatchFromImageList,
    "CR Intertwine Lists" : CR_IntertwineLists,
    "CR Repeater": CR_Repeater,    
    "CR XY Product": CR_XYProduct,
    "CR Text List To String": CR_TextListToString,
}
'''
