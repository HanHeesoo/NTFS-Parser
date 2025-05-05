# main.py
import argparse
from vbr_info import *
from parse_vbr import *
from parse_bpb import *
from ntfs_info import *
from parse_mft import *
from initial import *

VBR_SIZE = 512
MFT_ENTRY_SIZE = 1024
MAX_MFT_SCAN = 5


def read_file(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        exit(1)


def display_object(obj):
    for field, value in vars(obj).items():
        if isinstance(value, dict):
            print(f"{field}: Hex = {value.get('hex')}, Dec = {value.get('dec')}")
        else:
            print(f"{field}: {value}")


def display_mft_entry(entry_index, entry_name, file_data, offset_to_mft):
    offset = offset_to_mft + (entry_index * MFT_ENTRY_SIZE)
    parsed_mft, attribute_cnt = parse_mft(file_data, offset)

    print(f"\n[*] Parsing MFT Entry #{entry_index} ({entry_name})")

    print("\n===== [ MFT Header ] =====")
    for field, value in parsed_mft["MFT_Header"].items():
        print(f"{field}: {value if not isinstance(value, int) else f'0x{value:X}'}")

    attr_headers = parsed_mft["Attribute_Headers"]
    non_res_headers = parsed_mft["Non_Resident_Headers"]
    attr_contents = parsed_mft["Attribute_Contents"]
    attr_labels = parsed_mft["Attribute_Labels"]

    for i in range(attribute_cnt):
        print(f"\n--- {attr_labels[i]} ---")
        #print(f"\n--- attribute {i} ---")
        # 예: Attribute Header 출력
        if i < len(attr_headers):
            attr_header_list = attr_headers[i]
            if isinstance(attr_header_list, list) and len(attr_header_list) > 0:
                print("  [ Attribute Header ]")
                for key, value in attr_header_list[0].items():
                    print(f"    {key}: {value if not isinstance(value, int) else f'0x{value:X}'}")
        # Non-Resident Header 출력
        if i < len(non_res_headers):
            r_header_list = non_res_headers[i]
            if isinstance(r_header_list, list) and len(r_header_list) > 0:
                print("  [ Resident Header ]")
                for key, value in r_header_list[0].items():
                    print(f"    {key}: {value if not isinstance(value, int) else f'0x{value:X}'}")

        # Attribute Content 출력
        if i < len(attr_contents):
            a_content_list = attr_contents[i]
            if isinstance(a_content_list, list) and len(a_content_list) > 0:
                print("  [ Attribute Content ]")
                for key, value in a_content_list[0].items():
                    print(f"    {key}: {value if not isinstance(value, int) else f'0x{value:X}'}")



def scan_special_mft_entries(file_data, offset_to_mft):
    special_entries = {}
    offset = offset_to_mft
    entry_num = 0

    print("[*] Scanning up to 5 MFT entries for special system files...")

    while offset + MFT_ENTRY_SIZE <= len(file_data) and entry_num < MAX_MFT_SCAN:
        try:
            parsed_mft, _ = parse_mft(file_data, offset)
            content_list = parsed_mft["Attribute_Contents"]

            for content in content_list[1]:
                if content and 'Filename' in content:
                    filename = content['Filename']
                    if filename.startswith('$'):
                        special_entries[filename] = entry_num
                        break
        except Exception:
            pass

        offset += MFT_ENTRY_SIZE
        entry_num += 1

    return special_entries

def main():
    parser = argparse.ArgumentParser(description="NTFS Parser")
    parser.add_argument('-f', '--file', required=True, help='Path to NTFS image file')
    args = parser.parse_args()

    file_data = read_file(args.file)
    ntfs_info = NTFSInfo()

    parsed_vbr_data, parsed_bpb_data, mft_entries, allocated_entries, entries_num = init(
        ntfs_info,
        file_data
    )
    offset_to_mft = ntfs_info.Offset_to_MFT


    while True:
        user_input = input("\nEnter structure to parse ('vbr', 'bpb', 'mft', 'exit'): ").strip().lower()

        if user_input == 'vbr':
            print("\n===== [ VBR Info ] =====")
            display_object(parsed_vbr_data)

        elif user_input == 'bpb':
            print("\n===== [ BPB Info ] =====")
            display_object(parsed_bpb_data)

        elif user_input == 'mft':
            if not mft_entries:
                print("No MFT entries found.")
                continue

            print("\n[*] Available MFT Entries:")
            for idx, _ in mft_entries:
                print(f"  Entry #{idx}")

            try:
                selected_idx = int(input("\nEnter MFT entry index to display: ").strip())
            except ValueError:
                print("Invalid index.")
                continue

            # 해당 인덱스를 가진 엔트리 찾기
            entry = next((rec for idx, rec in mft_entries if idx == selected_idx), None)
            if entry is None:
                print("Index not found.")
                continue

            display_mft_entry(selected_idx, f"Entry_{selected_idx}", file_data, offset_to_mft)


        elif user_input == 'exit':
            print("Exiting.")
            break

        else:
            print("Invalid option. Please enter 'vbr', 'bpb', 'mft', or 'exit'.")

if __name__ == '__main__':
    main()
