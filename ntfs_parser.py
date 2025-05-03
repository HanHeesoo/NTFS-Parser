# main.py
import argparse
from vbr_info import *
from parse_vbr import *
from parse_vbr_bpb import *
from parse_ntfs import *
from ntfs_info import *
from parse_mft import *

vbr_size = 512
mft_size = 1024


def read_file(filename):
    with open(filename, 'rb') as f:
        file_data = f.read()  # 파일 전체를 읽어옴
    return file_data

def main():
    # 명령줄 인자 처리
    parser = argparse.ArgumentParser(description="NTFS Parser")
    parser.add_argument('-f', '--file', required=True, help='Path to NTFS image file')
    args = parser.parse_args()

    # 전체 파일 읽기
    file_data = read_file(args.file)

    ntfs_info = NTFSInfo()

    # VBR 영역만 추출 (512 bytes)
    vbr_data = file_data[:vbr_size]
    parsed_vbr_data = parse_vbr(vbr_data)
    parsed_bpb_data = parse_bpb(vbr_data, ntfs_info)

    offset_to_mft = ntfs_info.Offset_to_MFT
    
    # 반복문으로 계속해서 인자 받기
    while True:
        type_input = input("Enter structure to parse ('vbr', 'bpb', 'exit' to quit): ").strip()
        
        if type_input == 'vbr':
            for field, value in vars(parsed_vbr_data).items():
                print(f"{field}: {value}")
        elif type_input == 'bpb':
            for field, value in vars(parsed_bpb_data).items():
                if isinstance(value, dict):
                    # 'value'가 딕셔너리인 경우, 'hex'와 'dec' 값을 출력
                    print(f"{field}: Hex = {value['hex']}, Dec = {value['dec']}")
                else:
                    # 'value'가 딕셔너리가 아닌 경우, 그냥 출력 (기타 필드)
                    print(f"{field}: {value}")
        elif type_input == 'mft':
            print("[*] Parsing MFT Entry at offset:", offset_to_mft)
            parsed_mft = parse_mft(file_data, offset_to_mft)

            # ───────────── MFT Header 출력 ─────────────
            print("\n===== [ MFT Header ] =====")
            mft_header = parsed_mft["MFT_Header"]
            for field, value in mft_header.items():
                if isinstance(value, int):
                    print(f"{field}: 0x{value:X}")
                else:
                    print(f"{field}: {value}")

            # ───────────── Attributes 출력 ─────────────
            attr_headers = parsed_mft["Attribute_Headers"]
            non_res_headers = parsed_mft["Non_Resident_Headers"]
            attr_contents = parsed_mft["Attribute_Contents"]

            for i, (a_header, r_header, a_content) in enumerate(zip(attr_headers, non_res_headers, attr_contents)):
                print(f"\n--- Attribute #{i} ---")

                # Attribute Header
                print("  [ Attribute Header ]")
                for key, value in a_header.items():
                    if isinstance(value, int):
                        print(f"    {key}: 0x{value:X}")
                    else:
                        print(f"    {key}: {value}")

                # Resident Header (있을 경우)
                if r_header:
                    print("  [ Resident Header ]")
                    for key, value in r_header.items():
                        if isinstance(value, int):
                            print(f"    {key}: 0x{value:X}")
                        else:
                            print(f"    {key}: {value}")

                # Attribute Content
                if a_content:
                    print("  [ Attribute Content ]")
                    for key, value in a_content.items():
                        if isinstance(value, int):
                            print(f"    {key}: 0x{value:X}")
                        else:
                            print(f"    {key}: {value}")

        elif type_input == 'exit':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please enter 'vbr', 'bpb', or 'exit'.")

if __name__ == "__main__":
    main()
