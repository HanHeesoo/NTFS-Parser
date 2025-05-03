# parse_vbr.py
from vbr_info import *
from ntfs_info import *
import struct

bpb_offset = BPBOffset()

def parse_bpb(bpb_data, ntfs_info):
    parsed_bpb_data = BPBData()
    
    # 리틀 엔디안 변환 (예: Bytes_per_Sector)
    Bytes_per_Sector = int.from_bytes(bpb_data[bpb_offset.Bytes_per_Sector : bpb_offset.Sectors_per_Cluster], byteorder='little')
    parsed_bpb_data.Bytes_per_Sector = {
        'hex': format(Bytes_per_Sector, 'x'),  # 16진수로 출력
        'dec': Bytes_per_Sector              # 10진수로 출력
    }
    
    # Sectors_per_Cluster
    Sectors_per_Cluster = int.from_bytes(bpb_data[bpb_offset.Sectors_per_Cluster : bpb_offset.Reserved_Sectors], byteorder='little')
    parsed_bpb_data.Sectors_per_Cluster = {
        'hex': format(Sectors_per_Cluster, 'x'),
        'dec': Sectors_per_Cluster
    }

    # Reserved_Sectors
    Reserved_Sectors = int.from_bytes(bpb_data[bpb_offset.Reserved_Sectors : bpb_offset.Always0_1], byteorder='little')
    parsed_bpb_data.Reserved_Sectors = {
        'hex': format(Reserved_Sectors, 'x'),
        'dec': Reserved_Sectors
    }
    
    # Always0_1
    parsed_bpb_data.Always0_1 = bpb_data[bpb_offset.Always0_1 : bpb_offset.Not_Used_by_NTFS_1].hex()
    
    # Not_Used_by_NTFS_1
    parsed_bpb_data.Not_Used_by_NTFS_1 = bpb_data[bpb_offset.Not_Used_by_NTFS_1 : bpb_offset.Media_Descriptor].hex()
    
    # Media_Descriptor
    parsed_bpb_data.Media_Descriptor = bpb_data[bpb_offset.Media_Descriptor : bpb_offset.Always0_2].hex()
    
    # Always0_2
    parsed_bpb_data.Always0_2 = bpb_data[bpb_offset.Always0_2 : bpb_offset.Sectors_per_Track].hex()
    
    # Sectors_per_Track
    Sectors_per_Track = int.from_bytes(bpb_data[bpb_offset.Sectors_per_Track : bpb_offset.Number_of_Heads], byteorder='little')
    parsed_bpb_data.Sectors_per_Track = {
        'hex': format(Sectors_per_Track, 'x'),
        'dec': Sectors_per_Track
    }

    # Number_of_Heads
    Number_of_Heads = int.from_bytes(bpb_data[bpb_offset.Number_of_Heads : bpb_offset.Hidden_Sectors], byteorder='little')
    parsed_bpb_data.Number_of_Heads = {
        'hex': format(Number_of_Heads, 'x'),
        'dec': Number_of_Heads
    }
    
    # Hidden_Sectors
    parsed_bpb_data.Hidden_Sectors = bpb_data[bpb_offset.Hidden_Sectors : bpb_offset.Not_Used_by_NTFS_2].hex()

    
    # Not_Used_by_NTFS_2
    parsed_bpb_data.Not_Used_by_NTFS_2 = bpb_data[bpb_offset.Not_Used_by_NTFS_2 : bpb_offset.Not_Used_by_NTFS_3].hex()
    
    # Not_Used_by_NTFS_3
    parsed_bpb_data.Not_Used_by_NTFS_3 = bpb_data[bpb_offset.Not_Used_by_NTFS_3 : bpb_offset.Total_Sectors].hex()
    
    # Total_Sectors
    Total_Sectors = int.from_bytes(bpb_data[bpb_offset.Total_Sectors : bpb_offset.Logical_Cluster_Number_for_the_File_MFT], byteorder='little')
    parsed_bpb_data.Total_Sectors = {
        'hex': format(Total_Sectors, 'x'),
        'dec': Total_Sectors
    }
    
    # Logical_Cluster_Number_for_the_File_MFT
    Logical_Cluster_Number_for_the_File_MFT = int.from_bytes(bpb_data[bpb_offset.Logical_Cluster_Number_for_the_File_MFT : bpb_offset.Logical_Cluster_Number_for_the_File_MFTMirr], byteorder='little')
    parsed_bpb_data.Logical_Cluster_Number_for_the_File_MFT = {
        'hex': format(Logical_Cluster_Number_for_the_File_MFT, 'x'),
        'dec': Logical_Cluster_Number_for_the_File_MFT
    }
    
    # Logical_Cluster_Number_for_the_File_MFTMirr
    Logical_Cluster_Number_for_the_File_MFTMirr = int.from_bytes(bpb_data[bpb_offset.Logical_Cluster_Number_for_the_File_MFTMirr : bpb_offset.Clusters_per_File_Record_Segment], byteorder='little')
    parsed_bpb_data.Logical_Cluster_Number_for_the_File_MFTMirr = {
        'hex': format(Logical_Cluster_Number_for_the_File_MFTMirr, 'x'),
        'dec': Logical_Cluster_Number_for_the_File_MFTMirr
    }
    
    # Clusters_per_File_Record_Segment
    Clusters_per_File_Record_Segment = int.from_bytes(bpb_data[bpb_offset.Clusters_per_File_Record_Segment : bpb_offset.Clusters_per_Index_Buffer], byteorder='little')
    parsed_bpb_data.Clusters_per_File_Record_Segment = {
        'hex': format(Clusters_per_File_Record_Segment, 'x'),
        'dec': Clusters_per_File_Record_Segment
    }
    
    # Clusters_per_Index_Buffer
    Clusters_per_Index_Buffer = int.from_bytes(bpb_data[bpb_offset.Clusters_per_Index_Buffer : bpb_offset.Not_Used_by_NTFS_4], byteorder='little')
    parsed_bpb_data.Clusters_per_Index_Buffer = {
        'hex': format(Clusters_per_Index_Buffer, 'x'),
        'dec': Clusters_per_Index_Buffer
    }
    
    # Not_Used_by_NTFS_4
    parsed_bpb_data.Not_Used_by_NTFS_4 = bpb_data[bpb_offset.Not_Used_by_NTFS_4 : bpb_offset.Volume_Serial_Number].hex()

    
    # Volume_Serial_Number
    Volume_Serial_Number = int.from_bytes(bpb_data[bpb_offset.Volume_Serial_Number : bpb_offset.Checksum], byteorder='little')
    parsed_bpb_data.Volume_Serial_Number = {
        'hex': format(Volume_Serial_Number, 'x'),
        'dec': Volume_Serial_Number
    }
    
    # Checksum
    parsed_bpb_data.Checksum = bpb_data[bpb_offset.Checksum : bpb_offset.Checksum + 4].hex()

    # NTFS 정보 계산 및 출력
    ntfs_info.calculate_ntfs_info(parsed_bpb_data)
    ntfs_info.display_ntfs_info()  # 정상 출력되도록 확인

    return parsed_bpb_data
