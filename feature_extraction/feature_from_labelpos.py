import numpy as np
import pandas as pd
import umap


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
    sin_ang_deg = sin_arg*180/np.pi
    return sin_ang_deg


# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    return (C[:,1]-A[:,1]) * (B[:,0]-A[:,0]) > (B[:,1]-A[:,1]) * (C[:,0]-A[:,0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return np.logical_and(ccw(A,C,D) != ccw(B,C,D), ccw(A,B,C) != ccw(A,B,D))


def points_to_features(points):
    back_ear = points[:,0]
    front_ear = points[:,1]
    bot_ear = points[:,2]
    top_ear = points[:,3]
    back_eye = points[:,4]
    front_eye = points[:,5]
    top_eye = points[:,6] ## TODO check if bug
    bot_eye = points[:,7]
    top_nose = points[:,8]
    bot_nose = points[:,9]
    mouth = points[:,10]

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

    return eye_opening, ear_opening, ear_angle, ear_pos_vec, snout_pos, mouth_pos, face_incl

def add_features_to_csv(in_csv_file):
    myFile = pd.read_csv(in_csv_file)

    back_ear = np.array(myFile[["Ear_back_x", "Ear_back_y"]])
    front_ear = np.array(myFile[["Ear_front_x", "Ear_front_y"]])
    bot_ear = np.array(myFile[["Ear_bottom_x", "Ear_bottom_y"]])
    top_ear = np.array(myFile[["Ear_top_x", "Ear_top_y"]])
    back_eye = np.array(myFile[["Eye_back_x", "Eye_back_y"]])
    front_eye = np.array(myFile[["Eye_front_x", "Eye_front_y"]])
    bot_eye = np.array(myFile[["Eye_bottom_x", "Eye_bottom_y"]])
    top_eye = np.array(myFile[["Eye_top_x", "Eye_top_y"]])
    top_nose = np.array(myFile[["Nose_top_x", "Nose_top_y"]])
    bot_nose = np.array(myFile[["Nose_bottom_x", "Nose_bottom_y"]])
    mouth = np.array(myFile[["Mouth_x", "Mouth_y"]])

    columns = ["Ear_back_x", "Ear_back_y", "Ear_front_x", "Ear_front_y","Ear_bottom_x", "Ear_bottom_y", "Ear_top_x", "Ear_top_y", "Eye_back_x", "Eye_back_y", "Eye_front_x", "Eye_front_y", "Eye_bottom_x", "Eye_bottom_y", "Eye_top_x", "Eye_top_y", "Nose_top_x", "Nose_top_y", "Nose_bottom_x", "Nose_bottom_y", "Mouth_x", "Mouth_y"]
    eye_opening, ear_opening, ear_angle, ear_pos_vec, snout_pos, mouth_pos, face_incl = points_to_features(myFile[columns].values.reshape(-1, 11,2))
    mapping_vectors = np.array([eye_opening, ear_opening, ear_angle, ear_pos_vec, snout_pos, mouth_pos, face_incl])
    average_values = np.array([np.mean(eye_opening), np.mean(ear_opening), np.mean(ear_angle), np.mean(ear_pos_vec), np.mean(snout_pos), np.mean(mouth_pos), np.mean(face_incl)])
    print(average_values)

    myFile["eye_opening"] = eye_opening
    myFile["ear_opening"] = ear_opening
    myFile["ear_angle"] = ear_angle
    myFile["ear_pos_vec"] = ear_pos_vec
    myFile["snout_pos"] = snout_pos
    myFile["mouth_pos"] = mouth_pos
    myFile["face_incl"] = face_incl


    feature_col = ["eye_opening", "ear_opening", "ear_angle", "ear_pos_vec", "snout_pos", "mouth_pos", "face_incl"]
    myFile = myFile.replace([np.inf, -np.inf], np.nan)
    myFile = myFile.dropna()

    # data = pd.read_csv(keypoints_csv)
    # standard_embedding = umap.UMAP(random_state=10).fit_transform(myFile[feature_col].values)
    # myFile["umap_x"]=standard_embedding[:,0]
    # myFile["umap_y"]=standard_embedding[:,1]
    # data.to_csv(keypoints_csv)
    # return standard_embedding

    # df[["Img_Path", "Frame_ID"]] = myFile[["Img_Path", "Frame_ID"]]

    myFile.to_csv(in_csv_file, index=False)
    # do_umap_projection(out_csv_file)

if __name__ == "__main__":
    add_features_to_csv('detected_keypoints.csv')