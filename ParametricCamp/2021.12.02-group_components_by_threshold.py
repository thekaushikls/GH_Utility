"""
    Inputs:
        threshold (int) : Threshold in milliseconds
        message (str)   : Group name (NickName)
        runscript (bool): Boolean to run script component
"""

# - - - - - - - - RHINO / GRASSHOPPER IMPORTS

import Grasshopper
from System.Drawing import Color

# - - - - - - - - GLOBALS

GrasshopperDocument = ghenv.Component.OnPingDocument()

# - - - - - - - - RUNSCRIPT

def get_heavy_components(threshold=5):
    return [component.InstanceGuid for component in GrasshopperDocument.ActiveObjects() if component.ProcessorTime.Milliseconds > threshold]

def create_new_group(color, nickname, guid_list):
    # Instantiate new GH_Group object
    new_group_object = Grasshopper.Kernel.Special.GH_Group()
    # Create default attributes for the group
    new_group_object.CreateAttributes()
    # Add NickName to group
    new_group_object.NickName = nickname
    # Set group color
    new_group_object.Colour = color
    # Add objects into group.
    for component_guid in guid_list:
        new_group_object.AddObject(component_guid)
    # Add group to Grasshopper canvas and return result
    return GrasshopperDocument.AddObject(new_group_object, False) 


if runscript:

    groupColor = Color.Tomato
    heavy_components = get_heavy_components(threshold)
    print(create_new_group(groupColor, message, heavy_components))
    

