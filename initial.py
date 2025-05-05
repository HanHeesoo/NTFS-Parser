import argparse
from vbr_info import *
from parse_vbr import *
from parse_bpb import *
from ntfs_info import *
from parse_mft import *

VBR_SIZE = 512  # VBR 크기


def dump_mft_entries(file_data: bytes, offset_to_mft: int, entries_num: int, record_size: int = 0x400) -> list[tuple[int, bytes]]:
    """
    MFT 영역을 record_size 단위로 분할하여
    최소 entries_num 만큼 순회 후, 이후 'FILE' 시그니처가 아닌 경우 종료

    반환: [(entry_index, raw_bytes), ...]
    """
    entries: list[tuple[int, bytes]] = []
    idx = 0
    while idx < entries_num:
        off = offset_to_mft + idx * record_size
        rec = file_data[off: off + record_size]
        if len(rec) < 4 or rec[:4] != b"FILE":
            idx += 1
            continue
        entries.append((idx, rec))
        idx += 1
        

    # entries_num 이후에는 시그니처가 맞는 경우에만 계속
    while True:
        off = offset_to_mft + idx * record_size
        rec = file_data[off: off + record_size]
        if len(rec) < 4 or rec[:4] != b"FILE":
            break
        entries.append((idx, rec))
        idx += 1
    return entries

def init(
    ntfs_info: NTFSInfo,
    file_data: bytes,
    record_size: int = 0x400
) -> tuple[dict, dict, list[tuple[int, bytes]], list[int], int]:
    """
    초기화 및 데이터 분할 함수

    반환:
      parsed_vbr, parsed_bpb,
      mft_entries: 리스트 of (index, raw_bytes),
      allocated_entries: 할당된 엔트리 번호 리스트,
      entries_num: 할당된 엔트리 총 개수
    """
    # 1) VBR 파싱
    vbr = file_data[:VBR_SIZE]
    parsed_vbr = parse_vbr(vbr)

    # 2) BPB 파싱
    parsed_bpb = parse_bpb(vbr, ntfs_info)

    # 3) 비트맵에서 할당된 엔트리 계산
    offset_to_mft = ntfs_info.Offset_to_MFT
    cluster_size = ntfs_info.Bytes_per_Sector * ntfs_info.Sectors_per_Cluster
    bmp = read_bitmap_attribute(file_data, offset_to_mft, cluster_size)
    allocated_entries: list[int] = []
    if bmp is None:
        print("B0 속성(비트맵)을 찾지 못함")
    elif isinstance(bmp, bytes):
        for byte_idx, b in enumerate(bmp):
            for bit in range(8):
                if b & (1 << bit):
                    allocated_entries.append(byte_idx * 8 + bit)
    else:
        start, length = bmp[0]
        segment = file_data[start:start+length]
        for byte_idx, b in enumerate(segment):
            for bit in range(8):
                if b & (1 << bit):
                    allocated_entries.append(byte_idx * 8 + bit)

    allocated_entries_len = len(allocated_entries)
    entries_num = allocated_entries[allocated_entries_len - 1] + 1

    # 4) MFT 엔트리 분할
    mft_entries = dump_mft_entries(
        file_data,
        offset_to_mft,
        entries_num=entries_num,
        record_size=record_size
    )

    return parsed_vbr, parsed_bpb, mft_entries, allocated_entries, entries_num