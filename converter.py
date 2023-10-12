import os
import csv
import numpy as np

class Converter:
    
    def __init__(self, scorer="", bodyparts=[]):
        
        if bodyparts == []:
            self.bodyparts = ["Ear_back", "Ear_front", "Ear_bottom","Ear_top",
                     "Eye_back","Eye_front","Eye_bottom","Eye_top","Nose_top","Nose_bottom","Mouth"]
        else:
            self.bodyparts = bodyparts
        
        self.scorer = scorer
        
        self.csv_width = 3 + len(self.bodyparts)
    
    
    def print_csv(self,csv_path):
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            
            for row in reader:
                print(row)
                
            
                
    def write_csv(self,in_path,out_path):
        add = ['018757_frame418.jpg', '418', '848', '306', '708', '372', '770', '388',
               '762', '219', '602', '449', '548', '473', '574', '478', '569', '433', '419',
               '597', '455', '622', '557', '649']
        
        with open(in_path, 'r') as input,open(out_path, 'w') as output:
            reader = csv.reader(input)
            writer = csv.writer(output)
            
            for row in reader:
                writer.writerow(row)
            writer.writerow(add)
            
    def convert_to_dlc_format(self,in_path,out_path):
        scorer_row = ["scorer","",""] + [self.scorer]*len(self.bodyparts)*2
        body_row = ["bodyparts","",""] + list(np.repeat(self.bodyparts,2))
        coord_row = ["coords","",""] + ["x","y"] * len(self.bodyparts)
        
        with open(in_path, 'r',newline='') as input,open(out_path, 'w',newline='') as output:
            reader = csv.reader(input)
            writer = csv.writer(output)
            
            writer.writerow(scorer_row)
            writer.writerow(body_row)
            writer.writerow(coord_row)
            for row in reader:
                writer.writerow(row)
                    
if __name__ == "__main__":
    csv_path = "labeling/csv_files/018757.csv"
    out_path = "out.csv"
    
    converter = Converter(scorer="Johan")
    
    #converter.write_csv(csv_path,out_path)
    #converter.print_csv(csv_path)
    
    converter.convert_to_dlc_format(csv_path,out_path)
