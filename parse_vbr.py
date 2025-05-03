# parse_vbr.py
from vbr_info import *

vbr_offset = VBROffset()

def parse_vbr(vbr_data):
    parsed_vbr_data = VBRData()
    
    parsed_vbr_data.Jump_Instruction = vbr_data[vbr_offset.Jump_Instruction : vbr_offset.OEM_ID].hex()
    parsed_vbr_data.OEM_ID = vbr_data[vbr_offset.OEM_ID : vbr_offset.BPB].hex()
    parsed_vbr_data.BPB = vbr_data[vbr_offset.BPB : vbr_offset.Extended_BPB].hex()
    parsed_vbr_data.Extended_BPB = vbr_data[vbr_offset.Extended_BPB : vbr_offset.Bootstrap_Code].hex()
    parsed_vbr_data.Bootstrap_Code = vbr_data[vbr_offset.Bootstrap_Code : vbr_offset.End_of_Sector_Marker].hex()
    parsed_vbr_data.End_of_Sector_Marker = vbr_data[vbr_offset.End_of_Sector_Marker :].hex()

    return parsed_vbr_data
