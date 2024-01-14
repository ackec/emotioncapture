import numpy as np
import pandas as pd
import umap
import csv

file_path = "feature_extraction\output\mouse_features.csv"

#mouth_pos1 
def calc_features_cos(point_arr1, point_arr2, point_arr3):
    vec1 = (point_arr2 - point_arr1)
    vec2 = (point_arr3 - point_arr1)
    len_vec1 = np.linalg.norm(vec1, 2, 1)
    len_vec2 = np.linalg.norm(vec2, 2, 1)
    dot_prod = (vec1*vec2).sum(1)
    len_prod = len_vec1*len_vec2
    cos_theta = np.divide(dot_prod, len_prod)
    cross_prod = vec1[:,0] * vec2[:,1] - vec2[:,0] * vec1[:,1]
    sin_theta = np.divide(cross_prod, len_prod)
    angle = np.arctan2(cos_theta, sin_theta)
    angle = angle*180/np.pi
    return angle

def calc_features_sin(point_arr1, point_arr2, point_arr3):
    vec1 = (point_arr2 - point_arr1)
    vec2 = (point_arr3 - point_arr1)
    len_vec1 = np.linalg.norm(vec1, 2, 1)
    len_vec2 = np.linalg.norm(vec2, 2, 1)
    cross_prod = vec1[:,0] * vec2[:,1] - vec2[:,0] * vec1[:,1]
    len_prod = len_vec1*len_vec2
    division = np.divide(cross_prod, len_prod)
    division[np.isnan(division)] = 0

    sin_arg = np.arcsin(division)

    #sin_arg = np.arcsin(np.divide(cross_prod, len_prod))
    sin_ang_deg = sin_arg*180/np.pi
    return sin_ang_deg


# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    return (C[:,1]-A[:,1]) * (B[:,0]-A[:,0]) > (B[:,1]-A[:,1]) * (C[:,0]-A[:,0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return np.logical_and(ccw(A,C,D) != ccw(B,C,D), ccw(A,B,C) != ccw(A,B,D))

def  create_subcsv(in_csv_file):
    df = pd.read_csv(in_csv_file)
    split_column = 'Video_Name'

    #video_list = []
    video_names = []
    for video_name in df[split_column].unique():
    # Create a new DataFrame containing only rows with the current unique value
        subset_df = df[df[split_column] == video_name]

    # Write the subset DataFrame to a new CSV file
        subset_df.to_csv(f'feature_extraction\subcsv/subset_{video_name}.csv', index=False)
        video_names.append("feature_extraction\subcsv/subset_" + str(video_name) + ".csv")
    
    print(video_names)
    for i in range(0, len(video_names)):
        points_to_features(str(video_names[i]), "feature_extraction\output\mouse_features.csv")

def add_row_to_csv(file_path, average_values):
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(average_values)


def points_to_features(in_csv_file, out_csv_file):
    myFile = pd.read_csv(in_csv_file)

    back_ear = np.array(myFile[["Ear_back_x", "Ear_back_y"]])
    front_ear = np.array(myFile[["Ear_front_x", "Ear_front_y"]])
    bot_ear = np.array(myFile[["Ear_bottom_x", "Ear_bottom_y"]])
    top_ear = np.array(myFile[["Ear_top_x", "Ear_top_y"]])
    back_eye = np.array(myFile[["Eye_back_x", "Eye_back_y"]])
    front_eye = np.array(myFile[["Eye_front_x", "Eye_front_y"]])
    top_eye = np.array(myFile[["Eye_top_x", "Eye_top_y"]])
    bot_eye = np.array(myFile[["Eye_bottom_x", "Eye_bottom_y"]])
    top_nose = np.array(myFile[["Nose_top_x", "Nose_top_y"]])
    bot_nose = np.array(myFile[["Nose_bottom_x", "Nose_bottom_y"]])
    mouth = np.array(myFile[["Mouth_x", "Mouth_y"]])
    ear_diff = (top_ear - bot_ear)/2
    middle_ear = top_ear - ear_diff
    ear_width = np.linalg.norm(top_ear - bot_ear, 2, 1)
    ear_length = np.linalg.norm(back_ear - front_ear, 2, 1)
    ear_opening = np.divide(ear_width,ear_length)
    eye_width = np.linalg.norm(top_eye - bot_eye, 2, 1)
    eye_length = np.linalg.norm(back_eye - front_eye, 2, 1)
    eye_opening = np.divide(eye_width,eye_length)


    ear_pos_sin = np.abs(calc_features_sin(front_ear, front_eye, back_ear))
    ear_pos_cos = np.abs(calc_features_cos(front_ear, front_eye, back_ear))
    mask = ear_pos_sin > ear_pos_cos
    new_ear_pos = np.copy(ear_pos_sin)
    new_ear_pos[mask] = ear_pos_cos[mask]
    #print("Ear position: \n", 180 - new_ear_pos)

    ear_angle_sin = np.abs(calc_features_sin(middle_ear, back_ear, front_ear))
    ear_angle_cos = np.abs(calc_features_cos(middle_ear, front_ear, back_ear))

    #print("Ear angle: \n", 90 + np.abs(ear_angle_sin))

    snout_pos = calc_features_sin(top_nose, front_eye, bot_nose)
    #print("Snout position: \n", np.abs(snout_pos))

    mouth_pos = calc_features_sin(front_eye, mouth, bot_nose)
    #print("Mouth position: \n", np.abs(mouth_pos))

    face_incl = calc_features_sin(front_eye, front_ear, bot_nose)
    #print("Face inclination: \n", 90 - np.abs(face_incl))

    ear_pos_vec = 180 - new_ear_pos
    ear_angle = 180 - np.abs(ear_angle_sin)
    #print(ear_angle)
    # Set all ear_angle to 180 degrees where back_ear-front_ear line intersects bot_ear-top_ear line.
    mask = intersect(back_ear,front_ear,bot_ear,top_ear)
    ear_angle[mask] = 180

    snout_pos = np.abs(snout_pos)
    mouth_pos = np.abs(mouth_pos)
    face_incl = 90 - np.abs(face_incl)

    mapping_vectors = np.array([eye_opening, ear_opening, ear_angle, ear_pos_vec, snout_pos, mouth_pos, face_incl])
    average_values = np.array([np.mean(eye_opening), np.mean(ear_opening), np.mean(ear_angle), np.mean(ear_pos_vec), np.mean(snout_pos), np.mean(mouth_pos), np.mean(face_incl)])
    append_str = [str(myFile["Video_Name"][0]), str(myFile["Stimuli"][0])]
    final_array = np.append(average_values, append_str)
    #print(mapping_vectors.T)
    #print([average_values.T])
    print(str(myFile["Video_Name"][0]))

    df = [average_values.T]
    #df.columns = ['eye_opening', 'ear_opening', 'ear_angle', 'ear_pos_vec', 'snout_pos', 'mouth_pos', 'face_incl']
    #print(myFile["Img_Path"])
    

    # data = pd.read_csv(keypoints_csv)
    #standard_embedding = umap.UMAP(random_state=10).fit_transform(average_values)
    #df["umap_x"]=standard_embedding[:,0]
    #df["umap_y"]=standard_embedding[:,1]
    # data.to_csv(keypoints_csv)
    # return standard_embedding

    #df[["Img_Path", "Frame_ID", "Video_Name"]] = myFile[["Img_Path", "Frame_ID", "Video_Name"]]

    #df.to_csv(out_csv_file, index=False)
    # do_umap_projection(out_csv_file)
    with open(out_csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(final_array)

if __name__ == "__main__":
    #points_to_features('output/all_training_data.csv', "output/mouse_features.csv")
    create_subcsv('feature_extraction\output\detected_keypoints.csv')
