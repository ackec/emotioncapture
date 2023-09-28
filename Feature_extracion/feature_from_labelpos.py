#import poses
#image top left
import numpy as np
from pandas import read_csv

import pandas as pd 

#Extract points from CSV
myFile = pd.read_csv('Feature_extracion/018757.csv', sep=',')

back_ear = np.array(myFile[["Point_1_X", "Point_1_Y"]])
front_ear = np.array(myFile[["Point_2_X", "Point_2_Y"]])

ear_length = np.linalg.norm(back_ear - front_ear, 2, 1)

ear_angle = np.arctan2(*(back_ear - front_ear).T)


# back_ear = [myFile["Point_1_X"].values, myFile["Point_1_Y"].values]
# front_ear = [myFile["Point_2_X"].values, myFile["Point_2_Y"].values]
# top_ear = [myFile["Point_3_X"].values, myFile["Point_3_Y"].values]
# bottom_ear = [myFile["Point_4_X"].values, myFile["Point_4_Y"].values]
# back_eye = [myFile["Point_5_X"].values, myFile["Point_5_Y"].values]
# front_eye = [myFile["Point_6_X"].values, myFile["Point_6_Y"].values]
# top_eye = [myFile["Point_7_X"].values, myFile["Point_7_Y"].values]
# bottom_eye = [myFile["Point_8_X"].values, myFile["Point_8_Y"].values]
# top_nose = [myFile["Point_9_X"].values, myFile["Point_9_Y"].values]
# bottom_nose = [myFile["Point_10_X"].values, myFile["Point_10_Y"].values]
# mouth = [myFile["Point_11_X"].values, myFile["Point_11_Y"].values]
# #Need to fix case for negative values, maybe NOT
# middle_ear = [front_ear[0] + abs(front_ear[0]-back_ear[0]), front_ear[1] + abs(front_ear[1]-back_ear[1])]
# feature_vec = []

# def calc_features(back_ear, front_ear, top_ear, bottom_ear, back_eye, front_eye, top_eye, bottom_eye, top_nose, bottom_nose, mouth, middle_ear):
#     eye_length = (abs(bottom_eye[0] - top_eye[0]), abs(bottom_eye[1] - top_eye[1]))
#     eye_width = (abs(back_eye[0] - front_eye[0]), abs(back_eye[1] - front_eye[1]))
#     ear_length = (abs(bottom_ear[0] - top_ear[0]), abs(bottom_ear[1] - top_ear[1]))
#     ear_width = (abs(back_ear[0] - front_ear[0]), abs(back_ear[1] - front_ear[1]))
    
#     eye_oppening = []
#     ear_oppening = []
#     for i in range(len(eye_length[0])):
#         vector_eye_1 = [eye_width[0][i], eye_width[1][i]]
#         vector_eye_2 = [eye_length[0][i], eye_length[1][i]]
#         norm_vector_eye_1 = np.linalg.norm(vector_eye_1)
#         norm_vector_eye_2 = np.linalg.norm(vector_eye_2)
#         eye_oppening.append(np.divide(norm_vector_eye_1, norm_vector_eye_2))
#         vector_ear_1 = [ear_width[0][i], ear_width[1][i]]
#         vector_ear_2 = [ear_length[0][i], ear_length[1][i]]
#         norm_vector_ear_1 = np.linalg.norm(vector_ear_1)
#         norm_vector_ear_2 = np.linalg.norm(vector_ear_2)
#         ear_oppening.append(np.divide(norm_vector_ear_1, norm_vector_ear_2))
    
    
#     #ear pos
#     front_eye_bottom_ear = (bottom_ear[0] - front_eye[0], bottom_ear[1] - front_eye[1])
#     bottom_ear_top_ear = (bottom_ear[0] - top_ear[0], bottom_ear[1] - top_ear[1])
#     ear_pos_deg = (np.arctan2(front_eye_bottom_ear[0], front_eye_bottom_ear[1]) - np.arctan2(bottom_ear_top_ear[0], bottom_ear_top_ear[1])) * 180 / np.pi
#     #print(ear_pos_deg)
    
#     #ear angle
#     bottom_ear_middle_ear = (bottom_ear[0] - middle_ear[0], bottom_ear[1]-middle_ear[0])
#     middle_ear_top_ear = (middle_ear[0] - top_ear[0], middle_ear[1] - top_ear[1])
#     ear_angle_deg = (np.arctan2(bottom_ear_middle_ear[0], bottom_ear_middle_ear[1]) - np.arctan2(middle_ear_top_ear[0], middle_ear_top_ear[1]))* 180 / np.pi
#     #print(ear_angle_deg)
    
#     #snout position
#     top_nose_front_eye = (top_nose[0] - front_eye[0], top_nose[1] - front_eye[1])
#     top_nose_bottom_nose = (top_nose[0] - bottom_nose[0], top_nose[1] - bottom_nose[1])
#     snout_pos_deg = (np.arctan2(top_nose_front_eye[0], top_nose_front_eye[1]) - np.arctan2(top_nose_bottom_nose[0], top_nose_bottom_nose[1]))* 180 / np.pi
#     #print(snout_pos_deg)

#     #mouth position
#     front_eye_bottom_nose = (front_eye[0] - bottom_nose[0], front_eye[1] - bottom_nose[1])
#     front_eye_mouth = (front_eye[0] - mouth[0], front_eye[1] - mouth[1])
#     mouth_pos_deg = (np.arctan2(front_eye_bottom_nose[0], front_eye_bottom_nose[1]) - np.arctan2(front_eye_mouth[0], front_eye_mouth[1]))* 180 / np.pi
#     #print(mouth_pos_deg)
    
#     #Face inclination
#     face_incl_deg = ((np.arctan2(front_eye_bottom_nose[0], front_eye_bottom_nose[1]) - np.arctan2(front_eye_bottom_ear[0], front_eye_bottom_ear[1])) - np.pi/2) * 180 / np.pi
#     #print(face_incl_deg)
#     feature_vec = [eye_oppening, ear_oppening, ear_pos_deg, ear_angle_deg, snout_pos_deg, mouth_pos_deg, face_incl_deg]

#     print("eye opening:\n", feature_vec[0])
#     print("ear opening:\n", feature_vec[1])
#     print("ear position:\n", feature_vec[2])
#     print("ear angle:\n", feature_vec[3])
#     print("snout position:\n", feature_vec[4])
#     print("mouth position:\n", feature_vec[5])
#     print("face inclination:\n", feature_vec[6])
    
#     return feature_vec

    

# #genomsnitt baseline



# calc_features(back_ear, front_ear, top_ear, bottom_ear, back_eye, front_eye, top_eye, bottom_eye, top_nose, bottom_nose, mouth, middle_ear)
# #print(middle_ear)