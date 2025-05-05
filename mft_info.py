mft_header_size = 0x2f
attribute_header_size = 0x0f

class MFTHeader:
    def __init__(self, offset_to_mft):
        self.Signature = offset_to_mft + 0x00
        self.Offset_to_Fixup_Array = offset_to_mft + 0x04
        self.Number_of_Entries_in_Fixup_Array = offset_to_mft + 0x06
        self.LogFile_Sequence_Number = offset_to_mft + 0x08
        self.Sequence_Number = offset_to_mft + 0x10
        self.Link_Count = offset_to_mft + 0x12
        self.Offset_to_First_Attribute = offset_to_mft + 0x14
        self.Flags = offset_to_mft + 0x16
        self.Used_Size_of_MFT_Entry = offset_to_mft + 0x18
        self.Allocated_Size_of_MFT_Entry = offset_to_mft + 0x1C
        self.File_Reference_to_Base_Record = offset_to_mft + 0x20
        self.Next_Attribute_ID = offset_to_mft + 0x28
        self.Align_to_4B_Boundary = offset_to_mft + 0x2A
        self.Number_of_This_MFT_Entry = offset_to_mft + 0x2C

class AttributesHeader:
    def __init__(self, offset_to_attribute):
        self.Attribute_Type_ID = offset_to_attribute + 0x00
        self.Length_of_Attribute = offset_to_attribute + 0x04
        self.Non_Resident_Flag = offset_to_attribute + 0x08
        self.Length_of_Name = offset_to_attribute + 0x09
        self.Offset_to_Name = offset_to_attribute + 0x0A
        self.Flag = offset_to_attribute + 0x0C
        self.Attribute_ID = offset_to_attribute + 0x0E

class ResidentHeader:
    def __init__(self, offset_to_attribute):
        self.Size_of_Content = offset_to_attribute + 0x10
        self.Offset_to_Content = offset_to_attribute + 0x14
        self.Indexed_Flag = offset_to_attribute + 0x16
        self.Unused = offset_to_attribute + 0x17
        self.Attribute_Name = offset_to_attribute + 0x18

class NonResidentHeader:
    def __init__(self, offset_to_attribute):
        self.Start_VCN = offset_to_attribute + 0x10
        self.End_VCN = offset_to_attribute + 0x18
        self.Offset_to_RunList = offset_to_attribute + 0x20
        self.Compression_Unit_Size = offset_to_attribute + 0x22
        self.Unused = offset_to_attribute + 0x24
        self.Allocated_Size_of_Attribute_Content = offset_to_attribute + 0x28
        self.Real_Size_of_Attribute_Content = offset_to_attribute + 0x30
        self.Initialized_State_of_Attribute_Content = offset_to_attribute + 0x38
        self.Attribute_Name = offset_to_attribute + 0x40

class Standard_Information:
    def __init__(self, offset_to_content):
        self.Create_Time = offset_to_content + 0x00
        self.Modified_Time = offset_to_content + 0x08
        self.MFT_Modified_Time = offset_to_content + 0x10
        self.Last_Accessed_Time = offset_to_content + 0x18
        self.Flag = offset_to_content + 0x20
        self.Maximum_Number_of_Version = offset_to_content + 0x24
        self.Version_Number = offset_to_content + 0x28
        self.Class_ID = offset_to_content + 0x2C
        self.Owner_ID = offset_to_content + 0x30
        self.Security_ID = offset_to_content + 0x34
        self.Quota_Charged = offset_to_content + 0x38
        self.Update_Sequence = offset_to_content + 0x40

class File_Name:
    def __init__(self, offset_to_content):
        self.File_Reference_of_Parent_Directory = offset_to_content + 0x00
        self.Create_Time = offset_to_content + 0x08
        self.Modified_Time = offset_to_content + 0x10
        self.MFT_Modified_Time = offset_to_content + 0x18
        self.Last_Accessed_Time = offset_to_content + 0x20
        self.Allocated_Size_of_File = offset_to_content + 0x28
        self.Real_Size_of_File = offset_to_content + 0x30
        self.Flags = offset_to_content + 0x38
        self.Reparse_Value = offset_to_content + 0x3C
        self.Length_of_Name = offset_to_content + 0x40
        self.Namespace = offset_to_content + 0x41
        self.Name = offset_to_content + 0x42


class MFTOffset:
    def __init__(self, offset_to_mft, offset_to_attribute, offset_to_content):
        self.MFTHeader = MFTHeader(offset_to_mft)
        self.AttributesHeader = AttributesHeader(offset_to_attribute)
        self.ResidentHeader = ResidentHeader(offset_to_attribute)
        self.StandardInformation = Standard_Information(offset_to_content)
        self.FileName = File_Name(offset_to_content)
