from mft_info import *
from datetime import datetime, timedelta

def filetime_to_datetime(filetime_int):
    """Windows FILETIME (100ns 단위, 1601년 기준) → datetime 문자열"""
    if filetime_int == 0:
        return "N/A"
    return (datetime(1601, 1, 1) + timedelta(microseconds=filetime_int // 10)).strftime('%Y-%m-%d %H:%M:%S')

def parse_mft(file_data, offset_to_mft):
    result = {}

    # ─────────────── 1. MFT Header ───────────────
    mft_header = MFTHeader(offset_to_mft)
    mft_header_info = {
        "Signature": file_data[mft_header.Signature : mft_header.Signature + 4].decode(errors="ignore"),
        "Offset_to_Fixup_Array": int.from_bytes(file_data[mft_header.Offset_to_Fixup_Array : mft_header.Offset_to_Fixup_Array + 2], "little"),
        "Number_of_Entries_in_Fixup_Array": int.from_bytes(file_data[mft_header.Number_of_Entries_in_Fixup_Array : mft_header.Number_of_Entries_in_Fixup_Array + 2], "little"),
        "LogFile_Sequence_Number": int.from_bytes(file_data[mft_header.LogFile_Sequence_Number : mft_header.LogFile_Sequence_Number + 8], "little"),
        "Sequence_Number": int.from_bytes(file_data[mft_header.Sequence_Number : mft_header.Sequence_Number + 2], "little"),
        "Link_Count": int.from_bytes(file_data[mft_header.Link_Count : mft_header.Link_Count + 2], "little"),
        "Offset_to_First_Attribute": int.from_bytes(file_data[mft_header.Offset_to_First_Attribute : mft_header.Offset_to_First_Attribute + 2], "little"),
        "Flags": int.from_bytes(file_data[mft_header.Flags : mft_header.Flags + 2], "little"),
        "Used_Size_of_MFT_Entry": int.from_bytes(file_data[mft_header.Used_Size_of_MFT_Entry : mft_header.Used_Size_of_MFT_Entry + 4], "little"),
        "Allocated_Size_of_MFT_Entry": int.from_bytes(file_data[mft_header.Allocated_Size_of_MFT_Entry : mft_header.Allocated_Size_of_MFT_Entry + 4], "little"),
        "File_Reference_to_Base_Record": int.from_bytes(file_data[mft_header.File_Reference_to_Base_Record : mft_header.File_Reference_to_Base_Record + 8], "little"),
        "Next_Attribute_ID": int.from_bytes(file_data[mft_header.Next_Attribute_ID : mft_header.Next_Attribute_ID + 2], "little"),
        "Align_to_4B_Boundary": int.from_bytes(file_data[mft_header.Align_to_4B_Boundary : mft_header.Align_to_4B_Boundary + 2], "little"),
        "Number_of_This_MFT_Entry": int.from_bytes(file_data[mft_header.Number_of_This_MFT_Entry : mft_header.Number_of_This_MFT_Entry + 4], "little"),
    }
    result["MFT_Header"] = mft_header_info

    cluster_size = 0x1000

    # ─────────────── 2. Offset to First Attribute ───────────────
    offset_to_first_attr = int.from_bytes(
        file_data[mft_header.Offset_to_First_Attribute : mft_header.Offset_to_First_Attribute + 2],
        byteorder="little"
    )
    offset_to_attribute = offset_to_mft + offset_to_first_attr

    # ─────────────── 3. Attributes 반복 파싱 ───────────────
    attribute_headers = []
    non_resident_headers = []
    attribute_contents = []
    attribute_labels = []

    i = 0

    while True:
        attr_header = MFTOffset(offset_to_mft, offset_to_attribute, 0).AttributesHeader

        attribute_type = int.from_bytes(file_data[attr_header.Attribute_Type_ID : attr_header.Attribute_Type_ID + 4], "little")
        if attribute_type == 0xFFFFFFFF:
            break

        attribute_length = int.from_bytes(file_data[attr_header.Length_of_Attribute : attr_header.Length_of_Attribute + 4], "little")
        non_resident_flag = file_data[attr_header.Non_Resident_Flag]
        attribute_id = int.from_bytes(file_data[attr_header.Attribute_ID : attr_header.Attribute_ID + 2], "little")

        # 배열이 비어있으면 새로 추가
        while len(attribute_headers) <= i:
            attribute_headers.append([])
            non_resident_headers.append([])
            attribute_contents.append([])

        # Add attribute header
        attr_header_info = {
            "Attribute_Type_ID": int.from_bytes(file_data[attr_header.Attribute_Type_ID : attr_header.Attribute_Type_ID + 4], "little"),
            "Length_of_Attribute": int.from_bytes(file_data[attr_header.Length_of_Attribute : attr_header.Length_of_Attribute + 4], "little"),
            "Non_Resident_Flag": file_data[attr_header.Non_Resident_Flag],
            "Length_of_Name": file_data[attr_header.Length_of_Name],
            "Offset_to_Name": int.from_bytes(file_data[attr_header.Offset_to_Name : attr_header.Offset_to_Name + 2], "little"),
            "Flag": int.from_bytes(file_data[attr_header.Flag : attr_header.Flag + 2], "little"),
            "Attribute_ID": int.from_bytes(file_data[attr_header.Attribute_ID : attr_header.Attribute_ID + 2], "little"),
        }
        attribute_headers[i].append(attr_header_info)

        # ─────────── 4. Attribute Content ───────────
        attr_content_info = {"Attribute_Type_ID": hex(attribute_type)}

        # Resident Header
        if non_resident_flag == 0:
            res_header = MFTOffset(offset_to_mft, offset_to_attribute, 0).ResidentHeader
            content_size = int.from_bytes(file_data[res_header.Size_of_Content : res_header.Size_of_Content + 4], "little")
            content_offset = int.from_bytes(file_data[res_header.Offset_to_Content : res_header.Offset_to_Content + 2], "little")
            absolute_content_offset = offset_to_attribute + content_offset
            content = file_data[absolute_content_offset : absolute_content_offset + content_size]

            if attribute_type == 0x10:  # Standard_Information
                attribute_labels.append("Standard Information")
                std_info = Standard_Information(absolute_content_offset)
                create_time = int.from_bytes(file_data[std_info.Create_Time : std_info.Create_Time + 8], "little")
                modified_time = int.from_bytes(file_data[std_info.Modified_Time : std_info.Modified_Time + 8], "little")
                accessed_time = int.from_bytes(file_data[std_info.Last_Accessed_Time : std_info.Last_Accessed_Time + 8], "little")

                attr_content_info["Create_Time"] = filetime_to_datetime(create_time)
                attr_content_info["Modified_Time"] = filetime_to_datetime(modified_time)
                attr_content_info["Last_Accessed_Time"] = filetime_to_datetime(accessed_time)

            elif attribute_type == 0x30:  # File_Name
                attribute_labels.append("FILE NAME")
                fn = File_Name(absolute_content_offset)
                fn_create = int.from_bytes(file_data[fn.Create_Time : fn.Create_Time + 8], "little")
                fn_modified = int.from_bytes(file_data[fn.Modified_Time : fn.Modified_Time + 8], "little")
                fn_real_size = int.from_bytes(file_data[fn.Real_Size_of_File : fn.Real_Size_of_File + 8], "little")
                fn_flags = int.from_bytes(file_data[fn.Flags : fn.Flags + 4], "little")

                name_length = file_data[fn.Length_of_Name]
                name_bytes = file_data[fn.Name : fn.Name + name_length * 2]
                filename = name_bytes.decode("utf-16le", errors="ignore")

                attr_content_info["Filename_Create_Time"] = filetime_to_datetime(fn_create)
                attr_content_info["Filename_Modified_Time"] = filetime_to_datetime(fn_modified)
                attr_content_info["Filename_Real_Size"] = fn_real_size
                attr_content_info["Filename_Flags"] = fn_flags
                attr_content_info["Filename"] = filename

            elif attribute_type == 0x40:  # VOLUME VERSION
                attribute_labels.append("VOLUME VERSION")
            elif attribute_type == 0x80:  # Data
                attribute_labels.append("DATA")
                try:
                    text_content = content.decode('utf-8', errors='replace')
                    attr_content_info['Data Content'] = text_content
                except UnicodeError:
                    attr_content_info['daData Content'] = content

            elif attribute_type == 0xB0:  # Bitmap
                attribute_labels.append("BITMAP")

        else:
            if attribute_type == 0x80:  # Data
                attribute_labels.append("DATA")
                # Non-resident
                nr = NonResidentHeader(offset_to_attribute)
                off = int.from_bytes(
                    file_data[nr.Offset_to_RunList:nr.Offset_to_RunList+2], 'little'
                )
                rl = file_data[offset_to_attribute+off:offset_to_attribute+attribute_length]
                runs = parse_runlist(rl)

                data_bytes = b""
                for lcn, count in runs:
                    start = lcn * cluster_size
                    end = start + (count * cluster_size)
                    data_bytes += file_data[start:end]
                
                try:
                    text_content = data_bytes.decode('utf-8', errors='replace')
                    attr_content_info['Data Content'] = text_content
                except UnicodeError:
                    attr_content_info['daData Content'] = data_bytes
            elif attribute_type == 0xB0:  # Bitmap
                attribute_labels.append("BITMAP")
                

        attribute_contents[i].append(attr_content_info)
        offset_to_attribute += attribute_length

        i += 1

    result["Attribute_Headers"] = attribute_headers
    if non_resident_headers:
        result["Non_Resident_Headers"] = non_resident_headers
    result["Attribute_Contents"] = attribute_contents
    result["Attribute_Labels"] = attribute_labels

    return result, i

def parse_runlist(runlist: bytes) -> list[tuple[int, int]]:
    """
    NTFS RunList 파싱
    반환: [(start_lcn, cluster_count), ...]
    """
    runs = []
    prev_lcn = 0
    i = 0
    while i < len(runlist):
        header = runlist[i]
        i += 1
        if header == 0:
            break
        length_size = header & 0x0F
        offset_size = (header >> 4) & 0x0F
        length = int.from_bytes(runlist[i:i+length_size], 'little')
        i += length_size
        raw_offset = int.from_bytes(
            runlist[i:i+offset_size], 'little', signed=True
        )
        i += offset_size
        lcn = prev_lcn + raw_offset
        runs.append((lcn, length))
        prev_lcn = lcn
    return runs


def read_bitmap_attribute(
    file_data: bytes,
    offset_to_mft: int,
    cluster_size: int
) -> bytes | list[tuple[int, int]] | None:
    """
    첫 번째 B0(Bitmap) 속성 찾기 및 바이트 위치 계산

    Resident: 비트맵 바이트 반환
    Non-resident: [(start_byte, byte_length), ...] 반환
    없으면 None
    """
    mft_header = MFTHeader(offset_to_mft)
    rel = int.from_bytes(
        file_data[
            mft_header.Offset_to_First_Attribute : 
            mft_header.Offset_to_First_Attribute + 2
        ],
        'little'
    )
    cursor = offset_to_mft + rel

    while True:
        typ = int.from_bytes(file_data[cursor:cursor+4], 'little')
        if typ == 0xFFFFFFFF:
            return None
        length = int.from_bytes(file_data[cursor+4:cursor+8], 'little')
        nonres = file_data[cursor+8]

        if typ == 0xB0:
            if nonres == 0:
                # Resident
                hdr = ResidentHeader(cursor)
                sz = int.from_bytes(
                    file_data[hdr.Size_of_Content:hdr.Size_of_Content+4], 'little'
                )
                off = int.from_bytes(
                    file_data[hdr.Offset_to_Content:hdr.Offset_to_Content+2], 'little'
                )
                start = cursor + off
                return file_data[start:start+sz]
            else:
                # Non-resident
                nr = NonResidentHeader(cursor)
                off = int.from_bytes(
                    file_data[nr.Offset_to_RunList:nr.Offset_to_RunList+2], 'little'
                )
                rl = file_data[cursor+off:cursor+length]
                runs = parse_runlist(rl)
                # 클러스터→바이트 범위 변환
                return [
                    (lcn * cluster_size, count * cluster_size)
                    for lcn, count in runs
                ]

        cursor += length