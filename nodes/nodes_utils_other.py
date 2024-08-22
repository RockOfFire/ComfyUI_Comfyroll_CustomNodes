#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import math
from ..categories import icons

class AnyType(str):
    # Credit to pythongosssss    

    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

#---------------------------------------------------------------------------------------------------------------------#
# Maths Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_ClampValue:
       
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
                "range_min": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
                "range_max": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
            }
        }
    
    RETURN_TYPES =("FLOAT", "STRING", )
    RETURN_NAMES =("a", "show_help", )
    FUNCTION = "clamp_value"    
    CATEGORY = icons.get("Comfyroll/Utils/Other")
    
    def clamp_value(self, a, range_min, range_max):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-clamp-value"

        a = max(range_min, min(a, range_max))        
        
        return (a, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_IntegerMultipleOf:
       
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "integer": ("INT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
                "multiple": ("FLOAT", {"default": 8, "min": 1, "max": 18446744073709551615}),
            }
        }
    
    RETURN_TYPES =("INT", "STRING", )
    RETURN_NAMES =("INT", "show_help", )
    FUNCTION = "int_multiple_of"    
    CATEGORY = icons.get("Comfyroll/Utils/Other")
    
    def int_multiple_of(self, integer, multiple=8):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-integer-multiple"
        
        if multiple == 0:
            return (int(integer), show_help, )
        integer = integer * multiple   
        
        return (int(integer), show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_Value:

    @classmethod
    def INPUT_TYPES(cls):  
        return {"required": {"value": ("FLOAT", {"default": 1.0,},)}}

    RETURN_TYPES = ("FLOAT", "INT", "STRING", )
    RETURN_NAMES = ("FLOAT", "INT", "show_help", )
    CATEGORY = icons.get("Comfyroll/Utils/Other")
    FUNCTION = "get_value"

    def get_value(self, value):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-value"
        
        return (float(value), int(value), show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_MathOperation:

    @classmethod
    def INPUT_TYPES(cls):
    
        operations = ["sin", "cos", "tan", "sqrt", "exp", "log", "neg", "abs"]
        
        return {
            "required": {
                "a": ("FLOAT", {"default": 1.0},), 
                "operation": (operations, ),
                "decimal_places": ("INT", {"default": 2, "min": 0, "max": 10}),
            }
        }
    
    RETURN_TYPES =("FLOAT", "STRING", )
    RETURN_NAMES =("a", "show_help", )
    FUNCTION = "do_math"    
    CATEGORY = icons.get("Comfyroll/Utils/Other")

    def do_math(self, a, operation, decimal_places):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-math-operation"    

        #Apply the specified operation on the input value 'a'.
        if operation == 'sin':
            result = math.sin(a)
        elif operation == 'cos':
            result = math.cos(a)
        elif operation == 'tan':
            result = math.tan(a)        
        elif operation == 'sqrt':
            result = math.sqrt(a)
        elif operation == 'exp':
            result = math.exp(a)
        elif operation == 'log':
            result = math.log(a)            
        elif operation == 'neg':
            result = -a
        elif operation == 'abs':
            result = abs(a)
        else:
            raise ValueError("CR Math Operation: Unsupported operation.")
            
        result = round(result, decimal_places)   
            
        return (result, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_GetParameterFromPrompt:

    @classmethod
    def INPUT_TYPES(cls):
           
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "prompt", "forceInput": True}),
                "search_string": ("STRING", {"multiline": False, "default": "!findme"}),
            }
        }
    
    RETURN_TYPES =("STRING", any_type, "FLOAT", "BOOLEAN", "STRING", )
    RETURN_NAMES =("prompt",  "text", "float", "boolean", "show_help", )
    FUNCTION = "get_string"    
    CATEGORY = icons.get("Comfyroll/Utils/Other")

    def get_string(self, prompt, search_string):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-find-string-in-prompt"    

        return_string = ""
        return_value = 0
        return_boolean = False
        return_prompt = prompt
        
        index = prompt.find(search_string)
        if index != -1:
            # Check if there is a quote after the search_string
            if prompt[index + len(search_string)] == '=':
                if prompt[index + len(search_string) + 1] == '"':
                    # Extract text between quotes
                    start_quote = index + len(search_string) + 2
                    end_quote = prompt.find('"', start_quote + 1)
                    if end_quote != -1:
                        return_string = prompt[start_quote:end_quote]
                        print(return_string)
                else:        
                    # Find the next space after the search_string
                    space_index = prompt.find(" ", index + len(search_string))
                    if space_index != -1:
                        return_string = prompt[index + len(search_string):space_index]
                    else:
                        return_string = prompt[index + len(search_string):]
            else:
                return_string = search_string[1:]

        if return_string == "":
            return (return_prompt, return_string, return_value, return_boolean, show_help, )
        
        if return_string.startswith("="):
            return_string = return_string[1:]
 
        return_boolean = return_string.lower() == "true"    

        # Check if return_string is an integer or a float
        try:
            return_value = int(return_string)
        except ValueError:
            try:
                return_value = float(return_string)
            except ValueError:
                return_value = 0

        remove_string = " " + search_string + "=" + return_string
        
        # The return_prompt should have the search_string and the return_text removed
        return_prompt = prompt.replace(remove_string, "")
         
        return (return_prompt, return_string, return_value, return_boolean, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SelectResizeMethod:

    @classmethod
    def INPUT_TYPES(cls):
    
        methods = ["Fit", "Crop"]
        
        return {
            "required": {
                "method": (methods, ),
            }
        }
    
    RETURN_TYPES =(any_type, "STRING", )
    RETURN_NAMES =("method", "show_help", )
    FUNCTION = "set_switch"    
    CATEGORY = icons.get("Comfyroll/Utils/Other")

    def set_switch(self, method):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-select-resize-method"    
      
        return (method, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
# Conditional Nodes
#---------------------------------------------------------------------------------------------------------------------#
class CR_SetValueOnBinary:
       
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "binary": ("INT", {"default": 1, "min": 0, "max": 1, "forceInput": True}),
                "value_if_1": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),   
                "value_if_0": ("FLOAT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),   
            }
        }
    
    RETURN_TYPES =("INT", "FLOAT", "STRING", )
    RETURN_NAMES =("INT", "FLOAT", "show_help", )
    FUNCTION = "set_value"    
    CATEGORY = icons.get("Comfyroll/Utils/Conditional")
    
    def set_value(self, binary, value_if_1, value_if_0):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-set-value-on-boolean"

        if binary == 1:
            return (int(value_if_1), value_if_1, show_help, )   
        else:
            return (int(value_if_0), value_if_0, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SetValueOnBoolean:
       
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "boolean": ("BOOLEAN", {"default": True, "forceInput": True}),
                "value_if_true": ("FLOAT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),   
                "value_if_false": ("FLOAT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),   
            }
        }
    
    RETURN_TYPES =("INT", "FLOAT", "STRING", )
    RETURN_NAMES =("INT", "FLOAT", "show_help", )
    FUNCTION = "set_value"    
    CATEGORY = icons.get("Comfyroll/Utils/Conditional")
    
    def set_value(self, boolean, value_if_true, value_if_false):

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-set-value-on-boolean"

        if boolean == True:
            return (int(value_if_true), value_if_true, show_help, )   
        else:
            return (int(value_if_false), value_if_false, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_SetValueOnString:

    @ classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": False, "default": "", "forceInput": True}),            
                },
            "optional": {
                "test_string": ("STRING", {"multiline": False, "default": ""}),
                "value_if_true": ("STRING", {"multiline": False, "default": ""}),
                "value_if_false": ("STRING", {"multiline": False, "default": ""}), 
            },
        }

    RETURN_TYPES = (any_type, "BOOLEAN", "STRING", )
    RETURN_NAMES = ("STRING", "BOOLEAN","show_help", )
    FUNCTION = "replace_text"
    CATEGORY = icons.get("Comfyroll/Utils/Conditional")

    def replace_text(self, text, test_string, value_if_true, value_if_false):
    
        show_help =  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/List-Nodes#cr-set-value-on-string" 
        
        if test_string in text:
            # Test condition is true, replace with value_if_true
            text_out = value_if_true
            bool_out = True
        else:
            # Test condition is false, replace with value_if_false
            text_out = value_if_false
            bool_out = False
        
        return (text_out, bool_out, show_help)

#---------------------------------------------------------------------------------------------------------------------#        
class CR_SetSwitchFromString:

    @classmethod
    def INPUT_TYPES(cls):
    
        methods = ["Fit", "Crop"]
        
        return {
            "required": {
                "text": ("STRING", {"multiline": False, "default": "", "forceInput": True}),
            },
            "optional": {
                "switch_1": ("STRING", {"multiline": False, "default": ""}),
                "switch_2": ("STRING", {"multiline": False, "default": ""}),
                "switch_3": ("STRING", {"multiline": False, "default": ""}),
                "switch_4": ("STRING", {"multiline": False, "default": ""}),                
            },            
        }
    
    RETURN_TYPES =("INT", "STRING", )
    RETURN_NAMES =("switch", "show_help", )
    FUNCTION = "set_switch"
    CATEGORY = icons.get("Comfyroll/Utils/Conditional")

    def set_switch(self, text, switch_1="", switch_2="", switch_3="", switch_4=""):
    
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Other-Nodes#cr-set-switch-from-string"    
      
        if text == switch_1:
            switch = 1
        elif text == switch_2:
            switch = 2
        elif text == switch_3:
            switch = 3
        elif text == switch_4:
            switch = 4
        else:
            pass
        
        return (switch, show_help, )        
        
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    ### Utility Other
    "CR Value": CR_Value,    
    "CR Clamp Value": CR_ClampValue,   
    "CR Integer Multiple": CR_IntegerMultipleOf,
    "CR Math Operation": CR_MathOperation,
    "CR Get Parameter From Prompt": CR_GetParameterFromPrompt,
    "CR Select Resize Method": CR_SelectResizeMethod,
    ### Conditional Nodes
    "CR Set Value On Boolean": CR_SetValueOnBoolean,
    "CR Set Value On Binary": CR_SetValueOnBinary,
    "CR Set Value on String": CR_SetValueOnString,      
    "CR Set Switch From String": CR_SetSwitchFromString,
}
'''

