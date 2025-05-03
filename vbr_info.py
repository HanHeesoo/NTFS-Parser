# vbr_info.py
# NTFS VBR (Volume Boot Record) 구조 관련 정보를 저장하는 파일

class VBROffset:
    def __init__(self):
        self.Jump_Instruction = 0x00
        self.OEM_ID = 0x03
        self.BPB = 0x0B
        self.Extended_BPB = 0x24
        self.Bootstrap_Code = 0x54
        self.End_of_Sector_Marker = 0x1FE


class VBRData:
    def __init__(self):
        self.Jump_Instruction = None
        self.OEM_ID = None
        self.BPB = None
        self.Extended_BPB = None
        self.Bootstrap_Code = None
        self.End_of_Sector_Marker = None


class BPBOffset:
    def __init__(self):
        self.Bytes_per_Sector = 0x0B
        self.Sectors_per_Cluster = 0x0D
        self.Reserved_Sectors = 0x0E
        self.Always0_1 = 0x10
        self.Not_Used_by_NTFS_1 = 0x13
        self.Media_Descriptor = 0x15
        self.Always0_2 = 0x16
        self.Sectors_per_Track = 0x18
        self.Number_of_Heads = 0x1A
        self.Hidden_Sectors = 0x1C
        self.Not_Used_by_NTFS_2 = 0x20
        self.Not_Used_by_NTFS_3 = 0x24
        self.Total_Sectors = 0x28
        self.Logical_Cluster_Number_for_the_File_MFT = 0x30
        self.Logical_Cluster_Number_for_the_File_MFTMirr = 0x38
        self.Clusters_per_File_Record_Segment = 0x40
        self.Clusters_per_Index_Buffer = 0x44
        self.Not_Used_by_NTFS_4 = 0x45
        self.Volume_Serial_Number = 0x48
        self.Checksum = 0x50

class BPBData:
    def __init__(self):
        self.Bytes_per_Sector = None
        self.Sectors_per_Cluster = None
        self.Reserved_Sectors = None
        self.Always0_1 = None
        self.Not_Used_by_NTFS_1 = None
        self.Media_Descriptor = None
        self.Always0_2 = None
        self.Sectors_per_Track = None
        self.Number_of_Heads = None
        self.Hidden_Sectors = None
        self.Not_Used_by_NTFS_2 = None
        self.Not_Used_by_NTFS_3 = None
        self.Total_Sectors = None
        self.Logical_Cluster_Number_for_the_File_MFT = None
        self.Logical_Cluster_Number_for_the_File_MFTMirr = None
        self.Clusters_per_File_Record_Segment = None
        self.Clusters_per_Index_Buffer = None
        self.Not_Used_by_NTFS_4 = None
        self.Volume_Serial_Number = None
        self.Checksum = None