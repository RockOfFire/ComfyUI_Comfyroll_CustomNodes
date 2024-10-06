# 🧩 Comfyroll Studio

****** Simple update ***********
Add the node "CR Aspect Ratio PH", to include some smartphones screen resolutions
********************************

Co-authored by Suzie1 and RockOfFire

Current version: 1.76

# Wiki

Please use our new wiki for info on the custom nodes, and lots of examples of their use.

https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki

# Installation

1. cd custom_nodes
2. git clone https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes.git
3. Restart ComfyUI

You can also install the nodes using the following methods:
* install using [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
* download from [CivitAI](https://civitai.com/models/87609/comfyroll-custom-nodes-for-comfyui)

# Patch Notes

https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/blob/main/Patch_Notes.md

# List of Custom Nodes
  
## Core Nodes
__📦 Essential Nodes__
* CR Image Output (changed 18/12/2023)
* CR Latent Batch Size
* CR Prompt Text
* CR Combine Prompt
* CR Seed
* CR Conditioning Mixer
* CR Select Model (new 24/1/2024)
* CR VAE Decode (new 24/1/2024)

__🔳 Aspect Ratio__
* CR Aspect Ratio
              * CR Aspect Ratio PH - to include smartphones screen resolutions
* CR SDXL Aspect Ratio
* CR SD1.5 Aspect Ratio
* CR Aspect Ratio Banners (new 18/12/2023)
* CR Aspect Ratio Social Media (new 15/1/2024)
* CR Aspect Ratio For Print (new 18/1/2024)

__📜 List Nodes__
* CR Text List (new 19/12/2023)
* CR Prompt List (new 1/1/2024)
* CR Float Range List (new 25/12/2023)
* CR Integer Range List (new 25/12/2023)
* CR Load Text List (new 27/12/2023)
* CR Binary To List (new 29/12/2023)
* CR Text List To String (updated 30/12/2023)
* CR Text Cycler (new 4/1/2024)
* CR Value Cycler (new 4/1/2024)

__📜 List IO__
* CR Load Image List (new 23/12/2023)
* CR Load Image List Plus (new 23/12/2023)
* CR Load GIF As List (new 6/1/2024)
* CR Font File List (new 18/12/2023)

__📜 List Utils__
* CR Batch Images From List (new 29/12/2023)    
* CR Intertwine_Lists (new 29/12/2023)
* CR Repeater (new 15/1/2024)   
* CR XY Product (new 2/1/2024)
* CR Text List To String (updated 30/12/2023)

__🌟 SDXL__
* CR SDXL Prompt Mix Presets
* CR SDXL Style Text
* CR SDXL Base Prompt Encoder

__💊 LoRA__
* CR Load LoRA
* CR LoRA Stack
* CR Apply LoRA Stack
* CR Random LoRA Stack (new 18/12/2023)
* CR Random Weight LoRA (new 18/12/2023)

__🕹️ ControlNet__
* CR Apply ControlNet
* CR Multi-ControlNet Stack
* CR Apply Multi-ControlNet Stack

__🚌 Bus__
* CR Data Bus In (new 12/1/2024)
* CR Data Bus Out (new 12/1/2024)
* CR 8 Channel In (new 12/1/2024)
* CR 8 Channel Out (new 12/1/2024)

__✈️ Module__
* CR Module Pipe Loader
* CR Module Input
* CR Module Output

__🛩️ Pipe__
* CR Image Pipe In
* CR Image Pipe Edit
* CR Image Pipe Out
* CR Pipe Switch

__⛏️ Model Merge__
* CR Model Stack
* CR Apply Model Merge

__🔍 Upscale__
* CR Multi Upscale Stack
* CR Upscale Image
* CR Apply Multi Upscale

__📉 XY Grid__
* CR XY List
* CR XY Interpolate   
* CR XY Index
* CR XY From Folder
* CR XY Save Grid Image
* CR Image Output

## 👾 Graphics Nodes

__👓 Graphics - Filter__
* CR Color Tint
* CR Halftone Filter
* CR Vignette Filter (new 21/12/2023)

__🌈 Graphics - Pattern__
* CR Halftone Grid
* CR Color Bars
* CR Style Bars   
* CR Checker Pattern
* CR Polygons
* CR Color Gradient
* CR Radial Gradiant
* CR Starburst Lines
* CR Starburst Colors
* CR Simple Binary Pattern
* CR Binary Pattern

__🟡 Graphics - Pattern__
* CR Draw Shape (new 24/12/2023)
* CR Draw Pie" (new 25/12/2023)  
* CR Random Shape Pattern" (new 25/12/2023)   

__🔤 Graphics - Text__
* CR Overlay Text
* CR Draw Text
* CR Mask Text
* CR Composite Text
* CR Select Font

__👽 Graphics - Template__
* CR Simple Meme Template
* CR Simple Banner
* CR Comic Panel Templates
* CR Simple Banner (new 18/12/2023)
* CR Simple Image Compare (new 18/12/2023)
* CR Thumbnail Preview (new 26/12/2023)
* CR Seamless Checker (new 18/1/2023)

__🌁 Graphics - Layout__
* CR Image Panel
* CR Page Layout
* CR Image Grid Panel
* CR Image Border
* CR Feathered Border (new 21/12/2023)
* CR Color Panel
* CR Simple Text Panel
* CR Half Drop Panel (new 23/1/2024)
* CR Diamond Panel (new 24/1/2024)
* CR Overlay Transparent Image
* CR Select ISO Size (new 18/1/2023)

## 🎥 Animation

__📋 Schedules__
* CR Simple Schedule
* CR Central Schedule
* CR Combine Schedules
* CR Output Schedule To File
* CR Load Schedule From File
* CR Schedule Input Switch

__📑 Schedulers__
* CR Simple Value Scheduler
* CR Simple Text Scheduler
* CR Value Scheduler
* CR Text Scheduler
* CR Load Scheduled Models
* CR Load Scheduled LoRAs
* CR Prompt Scheduler
* CR Simple Prompt Scheduler

__📝 Prompt__
* CR Keyframe List
* CR Load Prompt Style
* CR Encode Scheduled Prompts

__🔢 Interpolation__
* CR Gradient Float
* CR Gradient Integer
* CR Increment Float
* CR Increment Integer
* CR Interpolate Latents

__🛠️ Utils__
* CR Debatch Frames
* CR Current Frame

__⌨️ IO__
* CR Load Animation Frames
* CR Load Flow Frames
* CR Output Flow Frames

## 🛠️ Utility Nodes

__🔢 Utils Index__
* CR Index
* CR Index Increment
* CR Index Multiply
* CR Index Reset
* CR Trigger

__🔧 Utils Conversion__    
* CR String To Number (changed 18/12/2023)
* CR String To Combo    
* CR Float To String
* CR Float To Integer
* CR Integer To String  
* CR String To Boolean (new 17/1/2024)  

__🔀 Utils Logic__
* CR Image Input Switch
* CR Image Input Switch (4 way)
* CR Latent Input Switch
* CR Conditioning Input Switch
* CR Clip Input Switch
* CR Model Input Switch
* CR ControlNet Input Switch
* CR VAE Input Switch
* CR Text Input Switch
* CR Text Input Switch (4 way)
* CR Switch Model and CLIP

__🔂 Utils Process__
* CR Img2Img Process Switch
* CR Hires Fix Process Switch
* CR Batch Process Switch

__🎲 Utils Random__
* CR Random Hex Color
* CR Random RGB
* CR Random Multiline Values (updated 28/12/2023)
* CR Random Multiline Colors (new 28/12/2023)
* CR Random RGB Gradient
* CR Random Panel Code (new 26/12/2023)

__🔤 Utils Text__
* CR Text (new 3/1/2024)
* CR Multiline Text (new 24/12/2023)
* CR Split String
* CR Text Concatenate (new 2/1/2024)
* CR Text Replace (new 8/1/2024)
* CR Text Blacklist (new 13/1/2024)
* CR Text Length (new 10/1/2024)    
* CR Text Operation (new 10/1/2024)
* CR Save Text To File (new 27/12/2023)

__⚙️ Conditional__
* CR Set Value On Boolean (new 29/12/2023)
* CR Set Value On Binary (new 3/1/2024)
* CR Set Value On String (new 9/1/2024)
* CR Set Switch From String (new 17/1/2024)

__⚙️ Utils Other__
* CR Value
* CR Integer Multiple
* CR Clamp Value (new 29/12/2023)
* CR Math Operation (new 31/12/2023)  
* CR Get Parameter From Prompt (new 5/1/2024)
* CR Select Resize Method (new 16/1/2024)

## Legacy
__💀 Legacy Nodes__
* CR Seed to Int
* CR Aspect Ratio SDXL, replaced by CR SDXL Aspect Ratio
* CR Image Size, replaced by CR Aspect Ratio
* CR SDXL Prompt Mixer, replaced by CR SDXL Prompt Mix Presets

# Comfyroll Workflow Templates

The nodes were originally made for use in the Comfyroll Template Workflows.

[Comfyroll Template Workflows](https://civitai.com/models/59806/comfyroll-template-workflows)

[Comfyroll Pro Templates](https://civitai.com/models/85619/comfyroll-pro-template)

[Comfyroll SDXL Workflow Templates](https://civitai.com/models/118005/comfyroll-sdxl-workflow-templates)

[SDXL Workflow for ComfyUI with Multi-ControlNet](https://civitai.com/models/129858/sdxl-workflow-for-comfyui-with-multi-controlnet)

[SDXL and SD1.5 Model Merge Templates for ComfyUI](https://civitai.com/models/123125/sdxl-and-sd15-model-merge-templates-for-comfyui)

# Credits

comfyanonymous/[ComfyUI](https://github.com/comfyanonymous/ComfyUI) - A powerful and modular stable diffusion GUI.

WASasquatch/[was-node-suite-comfyui](https://github.com/WASasquatch/was-node-suite-comfyui) - A powerful custom node extensions of ComfyUI.

TinyTerra/[ComfyUI_tinyterraNodes](https://github.com/TinyTerra/ComfyUI_tinyterraNodes) - A selection of nodes for Stable Diffusion ComfyUI

hnmr293/[ComfyUI-nodes-hnmr](https://github.com/hnmr293/ComfyUI-nodes-hnmr) - ComfyUI custom nodes - merge, grid (aka xyz-plot) and others

SeargeDP/[SeargeSDXL](https://github.com/SeargeDP) - ComfyUI custom nodes - Prompt nodes and Conditioning nodes

LucianoCirino/[efficiency-nodes-comfyui](https://github.com/LucianoCirino/efficiency-nodes-comfyui) - A collection of ComfyUI custom nodes.

SLAPaper/[ComfyUI-Image-Selector](https://github.com/SLAPaper/ComfyUI-Image-Selector) - Select one or some of images from a batch

pythongosssss/[ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts) - Enhancements & experiments for ComfyUI, mostly focusing on UI features

bash-j/[mikey_nodes](https://github.com/bash-j/mikey_nodes) - comfy nodes from mikey

ltdrdata/[ComfyUI-Impact-Pack](https://github.com/ltdrdata/ComfyUI-Impact-Pack) - 
