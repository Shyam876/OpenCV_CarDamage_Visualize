import numpy as np
import cv2
import matplotlib.pyplot as plt
import json

colors = [[51, 51, 204],[255, 0, 0],[255, 51, 153],[204, 255, 255],[153, 255, 51],[255, 255, 0],[0, 153, 204],[230, 0, 230],[255, 255, 255],[204, 51, 255],[255, 179, 153],[0, 204, 255],[230, 230, 0],[51, 204, 255],[102, 255, 102],[204, 102, 153],[57, 115, 172],[255, 51, 0],[51, 51, 204],[255, 0, 0],[255, 51, 153],[204, 255, 255],[153, 255, 51],[255, 255, 0],[0, 153, 204],[230, 0, 230],[255, 255, 255],[204, 51, 255],[255, 179, 153],[0, 204, 255],[230, 230, 0],[51, 204, 255],[102, 255, 102],[204, 102, 153],[57, 115, 172],[255, 51, 0]]

def main():
    print("inside main")
    car_number = input("Enter Car number : ")
    for i in range(1, 3):
        img = define_parts(i, int(car_number))
        out_img = np.copy(img)
        out_img = cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB)
        cv2.imshow("image"+str(i),out_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def define_parts(index, car_number):
    print(car_number)
    image = cv2.imread('images/'+str(car_number)+".jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    car_image = image
    if(index==1):
        f = open("data/"+str(car_number)+"-car-parts.json")
        
    else:
        f = open("data/"+str(car_number)+"-damages.json")
    
    data = json.load(f)

    #to add coordinate data and part labels
    values = []
    labels = []
    i = 0

    for dicts in data:
        if("points" in dicts["value"]):
            values.append(dicts["value"]["points"])  #extracting coordinate values from json
            labels.append(dicts["value"]["polygonlabels"][0])  #extracting label for everypart
    
    shape = np.zeros(car_image.shape, np.uint8)

    #for each pair of coordinates of everypart
    for value in values:
        height, width, _ = car_image.shape
        min_x, min_y = width, height
        max_x = max_y = 0
        r,g,b = getColor(i)
        rectLength = len(str(labels[i]))
        car_part = str(labels[i])
        
        for points in value:
            #conversion from normalized xy coordinates to original xy coordinates
            points[0] = (points[0]*width)/100
            points[1] = (points[1]*height)/100
            min_x,max_x = min(min_x, points[0]),max(max_x, points[0]) 
            min_y,max_y = min(min_y, points[1]),max(max_y, points[1]) 

        cv2.fillPoly(shape, np.int32([value]), color =(r,g,b)) #creates a polygon Shape according to coordinates provided
        cv2.polylines(car_image, np.int32([value]), True ,(r,g,b),1) #outline for polygon
        cv2.rectangle(car_image, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (r,g,b), 2) #rectangle arround polygon
        cv2.rectangle(car_image, (int(min_x), int(min_y)), (int(min_x)+(rectLength*8), int(min_y+15)), (0,0,0), -1) #background for part label
        cv2.putText(car_image, car_part, (int(min_x), int(min_y+10)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255)) #inserts label for each part
        out = cv2.addWeighted(car_image, 1.0, shape, 0.35, 1)  # adds all the things created above
        
        i = i+1

    return out

def getColor(index):
    color = colors[index]
    return color[0],color[1],color[2]

    
if __name__ == "__main__":
    main()