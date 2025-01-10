
import pandas as pd
import math

data=pd.read_csv("forestdata.csv")
features=data
# Euclidean distance
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 +(point1[1]-point2[1])**2)


# k-Nearest Neighbors Classifier
def knn(test_berry,features=features,k=3):
    #print(test_berry)
    distances=[]
    food_counter=0
    poison_counter=0
    for index,row in features.iterrows():
        #print("testberry", test_berry)
        dist=round(math.sqrt((row[0]-test_berry.sepal_length)**2 + (row[1]-test_berry.sepal_width)**2 ),5)
        distances.append((dist,row[2]))
 
    #k_indices = np.argsort(distances)[:k]
    neighbours=sorted(distances)[:k]
    for n in neighbours:
        if n[1]=='food':
            food_counter+=1
        elif n[1]=='poison':
            poison_counter+=1
            
    return 'food' if food_counter>poison_counter else 'poison' 
