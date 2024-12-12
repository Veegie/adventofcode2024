with open('input.txt') as file:
    disk: list[int] = [int(c) for c in file.read()]

free_blocks: dict[int, int] = dict()
moved_files: dict[int, list[tuple[int, int]]] = dict()

for disk_index in range(1, len(disk), 2):
    free_blocks[disk_index] = disk[disk_index]

checksum: int = 0

for disk_index in range(len(disk) - 1, 1, -2):
    file_size = disk[disk_index]
    file_id = disk_index // 2
    move_to: int = -1
    for i, (free_block_index, block_size) in enumerate(free_blocks.items()):
        if free_block_index > disk_index:
            break
        if block_size >= file_size:
            if free_block_index not in moved_files:
                moved_files[free_block_index] = []
            moved_files[free_block_index].append((file_size, file_id))
            move_to = free_block_index
            break
    if move_to != -1:
        if free_blocks[move_to] == file_size:
            del free_blocks[move_to]
        else:
            free_blocks[move_to] -= file_size

processed_file_ids: dict[int, bool] = dict()
comp_disk_idx = disk[0]
for idx in range(1, len(disk)):
    if idx in moved_files:
        free_space = disk[idx]
        for moved in moved_files[idx]:
            free_space -= moved[0]
            for i in range(0, moved[0]):
                checksum += comp_disk_idx * moved[1]
                comp_disk_idx += 1
            processed_file_ids[moved[1]] = True
        comp_disk_idx += free_space
    elif idx % 2 == 1:
        # free space with no moved files
        comp_disk_idx += disk[idx]
    else:
        file_id = idx // 2
        if file_id in processed_file_ids:
            comp_disk_idx += disk[idx]
        else:
            for i in range(0, disk[idx]):
                checksum += comp_disk_idx * file_id
                comp_disk_idx += 1

print(checksum)
