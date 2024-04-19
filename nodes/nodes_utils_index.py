#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Studio custom nodes by RockOfFire and Akatsuzi    https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                                 https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

from ..categories import icons

#---------------------------------------------------------------------------------------------------------------------#
class CR_Trigger: 

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"index": ("INT", {"default": 0.0, "min": 0.0, "max": 9999.0, "step": 1.0,}),
                             "trigger_value": ("INT", {"default": 1, "min": 0, "max": 10000}),        
                },
        }

    RETURN_TYPES = ("INT", "BOOLEAN", "STRING", )
    RETURN_NAMES = ("index", "trigger", "show_help", )
    FUNCTION = "trigger"
    CATEGORY = icons.get("Comfyroll/Utils/Index")

    def trigger(self, index, trigger_value):
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Utils-Index-Nodes#cr-trigger"
        return (index, index == trigger_value, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_Index: 

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"index": ("INT", {"default": 1, "min": 0, "max": 10000}),
                             "print_to_console": (["Yes","No"],),        
                },
        }

    RETURN_TYPES = ("INT", "STRING", )
    RETURN_NAMES = ("INT", "show_help", )
    FUNCTION = "index"
    CATEGORY = icons.get("Comfyroll/Utils/Index")

    def index(self, index, print_to_console):
    
        if print_to_console == "Yes":
            print(f"[Info] CR Index:{index}")

        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Index-Nodes#cr-index"
        return (index, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_IncrementIndex:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "index": ("INT", {"default": 1, "min": -10000, "max": 10000, "forceInput": True}),
                    "interval": ("INT", {"default": 1, "min": -10000, "max": 10000}),
                    }
        }

    RETURN_TYPES = ("INT", "INT", "STRING", )
    RETURN_NAMES = ("index", "interval", "show_help", )
    FUNCTION = "increment"
    CATEGORY = icons.get("Comfyroll/Utils/Index")
    
    def increment(self, index, interval):
        index+=interval
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Index-Nodes#cr-index-increment"
        return (index, show_help, )

#---------------------------------------------------------------------------------------------------------------------#   
class CR_MultiplyIndex:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "index": ("INT", {"default": 1, "min": 0, "max": 10000, "forceInput": True}),
                    "factor": ("INT", {"default": 1, "min": 0, "max": 10000}),
                    }
        }


    RETURN_TYPES = ("INT", "INT", "STRING", )
    RETURN_NAMES = ("index", "factor", "show_help", )
    FUNCTION = "multiply"
    CATEGORY = icons.get("Comfyroll/Utils/Index")
    
    def multiply(self, index, factor):
        index = index * factor
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Index-Nodes#cr-index-multiply"
        return (index, factor, show_help, ) 

#---------------------------------------------------------------------------------------------------------------------#   
class CR_IndexReset:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "index": ("INT", {"default": 1, "min": 0, "max": 10000, "forceInput": True}),
                    "reset_to": ("INT", {"default": 1, "min": 0, "max": 10000}),
                    }
        }


    RETURN_TYPES = ("INT", "INT", "STRING", )
    RETURN_NAMES = ("index", "reset_to", "show_help", )
    FUNCTION = "reset"
    CATEGORY = icons.get("Comfyroll/Utils/Index")
    
    def reset(self, index, reset_to):
        index = reset_to
        show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Index-Nodes#cr-index-reset"
        return (index, reset_to, show_help, )   
     
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    # Index
    "CR Index":CR_Index,    
    "CR Index Increment":CR_IncrementIndex,
    "CR Index Multiply":CR_MultiplyIndex,
    "CR Index Reset":CR_IndexReset,
    "CR Trigger":CR_Trigger,    
}
'''    
     
