import os
import random
import shutil

# Paths to your dataset images and labels
dataset_paths = {
    "dataset1": {"images": "dataset/annotated_dataset.yolov89(small_name/train/images", "labels": "dataset/annotated_dataset.yolov89(small_name/train/labels"},
    "dataset2": {"images": "dataset/ai cctv.v2i.yolov8/train/images", "labels": "dataset/ai cctv.v2i.yolov8/train/labels"},
    "dataset3": {"images": "dataset/cctv.v1i.yolov8 (1)small/train/images", "labels": "dataset/cctv.v1i.yolov8 (1)small/train/labels"},
    "dataset4": {"images": "dataset/CCTV.v1i.yolov8small/train/images", "labels": "dataset/CCTV.v1i.yolov8small/train/labels"},
    "dataset5": {"images": "dataset/AICCTV.v1i.yolov8/train/images", "labels": "dataset/AICCTV.v1i.yolov8/train/labels"}
}

# Directories where the final train/val data will be stored
train_dir = "project_folder/train"
val_dir = "project_folder/val"

# Create directories if they don't exist
os.makedirs(os.path.join(train_dir, "images"), exist_ok=True)
os.makedirs(os.path.join(train_dir, "labels"), exist_ok=True)
os.makedirs(os.path.join(val_dir, "images"), exist_ok=True)
os.makedirs(os.path.join(val_dir, "labels"), exist_ok=True)

# Split ratio (80% train, 20% val)
split_ratio = 0.8

# Helper function to copy files to the target directory
def copy_files(src_image_dir, src_label_dir, target_image_dir, target_label_dir, filenames):
    for filename in filenames:
        image_path = os.path.join(src_image_dir, filename)
        label_path = os.path.join(src_label_dir, filename.replace('.jpg', '.txt'))
        if os.path.exists(image_path) and os.path.exists(label_path):
            shutil.copy(image_path, target_image_dir)
            shutil.copy(label_path, target_label_dir)

# Shuffle and split the dataset
for dataset_name, paths in dataset_paths.items():
    image_dir = paths["images"]
    label_dir = paths["labels"]
    
    # Get a list of all image files (assuming .jpg extension, modify if needed)
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    random.shuffle(image_files)
    
    # Split data into train and val
    split_index = int(len(image_files) * split_ratio)
    train_files = image_files[:split_index]
    val_files = image_files[split_index:]
    
    # Copy train and val data into the appropriate directories
    print(f"Processing {dataset_name}...")
    copy_files(image_dir, label_dir, os.path.join(train_dir, "images"), os.path.join(train_dir, "labels"), train_files)
    copy_files(image_dir, label_dir, os.path.join(val_dir, "images"), os.path.join(val_dir, "labels"), val_files)

print("✅ Dataset is now split into 'train' and 'val' directories!")
