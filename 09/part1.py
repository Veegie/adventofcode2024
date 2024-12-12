with open('input.txt') as file:
    disk: str = [int(c) for c in file.read()]

left: int = 1
right: int = len(disk) - 1
left_file_idx: int = 1
right_file_idx: int = right // 2
comp_disk_idx: int = disk[0]

free_blocks: int = 0
buffer: int = 0
checksum: int = 0
while left < right or buffer > 0:
    free_blocks += disk[left]
    while free_blocks > 0:
        if buffer > 0:
            file_size: int = buffer
            buffer = 0
        else:
            file_size: int = disk[right]
        if free_blocks >= file_size:
            for i in range(0, file_size):
                checksum += comp_disk_idx * right_file_idx
                comp_disk_idx += 1
                free_blocks -= 1
            right_file_idx -= 1
            right -= 2
        else:
            for i in range(0, free_blocks):
                checksum += comp_disk_idx * right_file_idx
                comp_disk_idx += 1
                free_blocks -= 1
                file_size -= 1
            buffer = file_size
    left += 1
    if left < right or (left == right and buffer == 0):
        for i in range(0, disk[left]):
            checksum += comp_disk_idx * left_file_idx
            comp_disk_idx += 1
        left_file_idx += 1
    left += 1

print(checksum)
