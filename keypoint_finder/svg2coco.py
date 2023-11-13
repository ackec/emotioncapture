import os
import csv
import json
import random


csv_folder = "dataset/csv_files/"
categories = [{"id": 1, "name": "mouse", "supercategory": "animal"}]
keypoints = [
    "Ear_back",
    "Ear_front",
    "Ear_bottom",
    "Ear_top",
    "Eye_back",
    "Eye_front",
    "Eye_bottom",
    "Eye_top",
    "Nose_top",
    "Nose_bottom",
    "Mouth",
]

# Specify the folder containing CSV files
output_json_file = "dataset/combined_annotations.json"


data = []
images = []
max_image_id = 0  # Track the maximum image ID

for csv_file in os.listdir(csv_folder):
    if csv_file.endswith(".csv"):
        csv_file_path = os.path.join(csv_folder, csv_file)
        
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                image_path = row['Img_Path']
                frame_id = max_image_id
                max_image_id += 1
                keypoints_list = []
                for keypoint_name in keypoints:
                    x = int(row[keypoint_name + '_x'])
                    y = int(row[keypoint_name + '_y'])
                    keypoints_list.extend([x, y, 2])  # Add 2 for visibility, assuming all keypoints are visible

                # Calculate the bounding box coordinates
                min_x = min(keypoints_list[0::3])
                max_x = max(keypoints_list[0::3])
                min_y = min(keypoints_list[1::3])
                max_y = max(keypoints_list[1::3])
                bbox = [min_x, min_y, max_x - min_x, max_y - min_y]

                annotation = {
                    "image_id": frame_id,
                    "id": frame_id,

                    "category_id": 1,  # Assuming all keypoints belong to the "person" category
                    "keypoints": keypoints_list,
                    'iscrowd': 0,
                    "score": 1.0,  # You can adjust the score as needed
                    "bbox": bbox,  # Bounding box coordinates (x0, y0, width, height)
                    "area": bbox[2]*bbox[3],
                    "num_keypoints": len(keypoints_list) // 3  # Number of keypoints in the annotations
                }
                data.append(annotation)

                # Save image paths
                images.append({"id": frame_id, "file_name": image_path,'height': 1080,'width': 1920,})

# Create the COCO format dictionary
coco_data = {
    "images": images,
    "annotations": data,
    "categories": categories
}

# Save as a single JSON file
with open(output_json_file, "w") as json_file:
    json.dump(coco_data, json_file)

print(f"Saved combined COCO JSON annotations to {output_json_file}")


# Load the combined JSON file
combined_json_file = "dataset/combined_annotations.json"  # Replace with your combined JSON file
with open(combined_json_file, "r") as json_file:
    combined_data = json.load(json_file)

# Define the desired proportions for train, val, and test sets
train_proportion = 0.7  # 70% for training
val_proportion = 0.15  # 15% for validation
test_proportion = 0.15  # 15% for testing

# Randomly shuffle the images and annotations
random.shuffle(combined_data["images"])

# Split the data into sets
total_images = len(combined_data["images"])
train_end = int(train_proportion * total_images)
val_end = train_end + int(val_proportion * total_images)

train_data = {
    "images": combined_data["images"][:train_end],
    "annotations": [],
    "categories": combined_data["categories"]
}

val_data = {
    "images": combined_data["images"][train_end:val_end],
    "annotations": [],
    "categories": combined_data["categories"]
}

test_data = {
    "images": combined_data["images"][val_end:],
    "annotations": [],
    "categories": combined_data["categories"]
}

# Filter annotations based on image IDs
for annotation in combined_data["annotations"]:
    image_id = annotation["image_id"]
    if image_id in [img["id"] for img in train_data["images"]]:
        train_data["annotations"].append(annotation)
    elif image_id in [img["id"] for img in val_data["images"]]:
        val_data["annotations"].append(annotation)
    elif image_id in [img["id"] for img in test_data["images"]]:
        test_data["annotations"].append(annotation)

# Save the three JSON files
train_json_file = "dataset/train_annotations.json"
val_json_file = "dataset/val_annotations.json"
test_json_file = "dataset/test_annotations.json"

with open(train_json_file, "w") as train_file:
    json.dump(train_data, train_file)

with open(val_json_file, "w") as val_file:
    json.dump(val_data, val_file)

with open(test_json_file, "w") as test_file:
    json.dump(test_data, test_file)

print(f"Saved train annotations to {train_json_file}")
print(f"Saved val annotations to {val_json_file}")
print(f"Saved test annotations to {test_json_file}")