import json
import csv
import os

def json_to_csv(input_folder, output_file):
    # Initialize an empty list to store data from all JSON files
    all_data = []

    # Loop through all JSON files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)

            # Read JSON data from the file
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                all_data.extend(data)

    # Create or open the CSV file for writing
    with open(output_file, "w", newline="") as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write header to CSV file
        header = ["Img_Path", "Frame_ID", "Ear_back_x", "Ear_back_y", "Ear_front_x", "Ear_front_y",
                  "Ear_bottom_x", "Ear_bottom_y", "Ear_top_x", "Ear_top_y", "Eye_back_x", "Eye_back_y",
                  "Eye_front_x", "Eye_front_y", "Eye_bottom_x", "Eye_bottom_y", "Eye_top_x", "Eye_top_y",
                  "Nose_top_x", "Nose_top_y", "Nose_bottom_x", "Nose_bottom_y", "Mouth_x", "Mouth_y"]
        csv_writer.writerow(header)

        # Write data to CSV file
        for i, entry in enumerate(all_data):
            img_path = filename.replace(".json", ".png")  # Assuming image files have a .jpg extension
            frame_id = i  # You may replace this with the actual frame ID

            keypoints = entry["keypoints"]
            ear_back_x, ear_back_y = keypoints[0]
            ear_front_x, ear_front_y = keypoints[1]
            ear_bottom_x, ear_bottom_y = keypoints[2]
            ear_top_x, ear_top_y = keypoints[3]
            eye_back_x, eye_back_y = keypoints[4]
            eye_front_x, eye_front_y = keypoints[5]
            eye_bottom_x, eye_bottom_y = keypoints[6]
            eye_top_x, eye_top_y = keypoints[7]
            nose_top_x, nose_top_y = keypoints[8]
            nose_bottom_x, nose_bottom_y = keypoints[9]
            mouth_x, mouth_y = keypoints[10]

            # Combine all data into a single row
            row = [img_path, frame_id, ear_back_x, ear_back_y, ear_front_x, ear_front_y, ear_bottom_x,
                   ear_bottom_y, ear_top_x, ear_top_y, eye_back_x, eye_back_y, eye_front_x, eye_front_y,
                   eye_bottom_x, eye_bottom_y, eye_top_x, eye_top_y, nose_top_x, nose_top_y, nose_bottom_x,
                   nose_bottom_y, mouth_x, mouth_y]

            # Write the row to the CSV file
            csv_writer.writerow(row)

if __name__ == "__main__":
    # Specify the input folder containing JSON files
    input_folder = "output_olivia/predictions"

    # Specify the output CSV file
    output_file = "output_all_points.csv"

    # Call the function to convert JSON to CSV
    json_to_csv(input_folder, output_file)
