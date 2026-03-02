import os

# Unified class list
final_classes = ['fight', 'fire', 'helmet', 'objects', 'person', 'vehicle', 'weapon', 'overcrowded', 'robbery']

# Dataset-specific original class names (some have inconsistent cases or variations)
dataset_mappings = {
    "dataset1": ['fight', 'fire', 'helmet', 'objects', 'person', 'vehicle', 'weapon'],
    "dataset2": ['Fire', 'Helmet', 'Person', 'Weapon', 'objects', 'overcrowded'],
    "dataset3": ['fight', 'fire', 'helmet', 'person', 'weapon'],
    "dataset4": ['helmet', 'person', 'weapon'],
    "dataset5": ['Fighting', 'Fire', 'Helmet', 'Person', 'Robbery', 'Weapon']
}

# Optional alias mapping for normalizing class names
alias_map = {
    "fighting": "fight",
    "fire": "fire",
    "helmet": "helmet",
    "person": "person",
    "robbery": "robbery",
    "weapon": "weapon",
    "objects": "objects",
    "overcrowded": "overcrowded",
    "vehicle": "vehicle"
}

# Builds a remapping dictionary from dataset-specific class indices to final class indices
def build_id_map(original_list, final_list):
    fixed_list = [alias_map.get(c.lower(), c.lower()) for c in original_list]
    return {i: final_list.index(c) for i, c in enumerate(fixed_list)}

# Remaps labels in YOLO .txt files using the ID mapping
def remap_labels(label_dir, id_map):
    for filename in os.listdir(label_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(label_dir, filename)
            with open(file_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts: continue
                old_id = int(parts[0])
                if old_id in id_map:
                    new_id = id_map[old_id]
                    parts[0] = str(new_id)
                    new_lines.append(" ".join(parts) + "\n")

            with open(file_path, 'w') as f:
                f.writelines(new_lines)

# Paths to dataset label folders
dataset_paths = {
    "dataset1": "dataset/annotated_dataset.yolov89(small_name/train/labels",
    "dataset2": "dataset/ai cctv.v2i.yolov8/train/labels",
    "dataset3": "dataset/cctv.v1i.yolov8 (1)small/train/labels",
    "dataset4": "dataset/CCTV.v1i.yolov8small/train/labels",
    "dataset5": "dataset/AICCTV.v1i.yolov8/train/labels"
}

# Run the remapping for each dataset
for name, path in dataset_paths.items():
    print(f"Processing {name}...")
    id_map = build_id_map(dataset_mappings[name], final_classes)
    remap_labels(path, id_map)

print("✅ All datasets processed and label IDs remapped to unified class list.")
