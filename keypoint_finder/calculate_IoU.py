import json
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
json_folder_path = 'testdata/predictions'
coco_file_path = 'testdata/test_annotation.json'

def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, x3, y3 = box2
    w2 = x3-x2
    h2 = y3-y2

    # Calculate intersection area
    x_inter = max(x1, x2)
    y_inter = max(y1, y2)
    w_inter = max(0, min(x1 + w1, x2 + w2) - x_inter)
    h_inter = max(0, min(y1 + h1, y2 + h2) - y_inter)
    area_inter = w_inter * h_inter

    # Calculate union area
    area_box1 = w1 * h1
    area_box2 = w2 * h2
    area_union = area_box1 + area_box2 - area_inter

    # Calculate IoU
    iou = area_inter / area_union if area_union > 0 else 0
    return iou

total_iou = 0
num_images = 0
# Load COCO annotations
with open(coco_file_path, 'r') as file:
    coco_data = json.load(file)

x =  []
# Load JSON files with keypoints
for annotation in coco_data['annotations']:
    image_id = annotation['image_id']
    file_name = next((img['file_name'] for img in coco_data['images'] if img['id'] == image_id), None)

    if file_name:
        # Load JSON file with keypoints
        json_file_path = f'{json_folder_path}/{file_name.replace(".jpg", ".json")}'
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)

        # Extract bounding box coordinates from COCO annotation
        bbox_coco = annotation['bbox']
        
        # Extract bounding box coordinates from JSON file
        bbox_json = json_data[0]['bbox'][0]
        
        # Calculate IoU
        iou = calculate_iou(bbox_coco, bbox_json)
        x.append(iou)

        total_iou += iou
        num_images += 1
        
        print(f"IoU for {file_name}: {iou}")

    else:
        print(f"Image with id {image_id} not found in the COCO dataset.")

# Calculate mean IoU
mean_iou = total_iou / num_images if num_images > 0 else 0
print(f"Mean IoU for all images: {mean_iou}")

plt.hist(x, bins = 100)
plt.xlabel("IoU")
plt.ylabel("Samples")

plt.savefig("hist.pdf", bbox_inches='tight')