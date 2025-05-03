class NTFSInfo:
    def __init__(self):
        self.VBR_Size = 0x200
        self.MFT_Size = 0x400
        self.MFT_Header_Size = 0x30
        self.Bytes_per_Sector = None
        self.Sectors_per_Cluster = None
        self.Total_Sectors = None
        self.Logical_Cluster_Number_for_the_File_MFT = None
        self.Logical_Cluster_Number_for_the_File_MFTMirr = None
        self.Offset_to_MFT = None

    def calculate_ntfs_info(self, bpb_data):
        self.Bytes_per_Sector = bpb_data.Bytes_per_Sector['dec']
        self.Sectors_per_Cluster = bpb_data.Sectors_per_Cluster['dec']
        self.Total_Sectors = bpb_data.Total_Sectors['dec']
        self.Logical_Cluster_Number_for_the_File_MFT = bpb_data.Logical_Cluster_Number_for_the_File_MFT['dec']
        self.Logical_Cluster_Number_for_the_File_MFTMirr = bpb_data.Logical_Cluster_Number_for_the_File_MFTMirr['dec']
        
        # MFT_Offset 계산
        self.Offset_to_MFT = self.Logical_Cluster_Number_for_the_File_MFT * self.Bytes_per_Sector * self.Sectors_per_Cluster

    def display_ntfs_info(self):
        print(f"Bytes per Sector: {self.Bytes_per_Sector}")
        print(f"Sectors per Cluster: {self.Sectors_per_Cluster}")
        print(f"Total Sectors: {self.Total_Sectors}")
        print(f"Logical Cluster Number for MFT: {self.Logical_Cluster_Number_for_the_File_MFT}")
        print(f"Logical Cluster Number for MFTMirr: {self.Logical_Cluster_Number_for_the_File_MFTMirr}")
        print(f"MFT Offset: 0x{format(self.Offset_to_MFT, 'x')}")
