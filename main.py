# json
import json
# K-Means
import pandas as pd
from sklearn.cluster import KMeans
# visual x-y
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
# Dijkstra Algorithm
import dijkstraExample as dks
# user func library
import funcs as bang
# save map html
import folium

# open geocoding text json
f = open("./address.json", 'r')
readBuffer = f.read()
f.close()
# convert text to json
addressJson = json.loads(readBuffer)

# K-Means
# addressJson is arg1
df = pd.DataFrame(columns=('x', 'y'))
for index, val in enumerate(addressJson) :
  df.loc[index] = [float(val["lat"]), float(val["lon"])]

# clustering
number = 3 # arg2
data_points = df.values
kmeans = KMeans(n_clusters = number).fit(data_points)
df['cluster_id'] = kmeans.labels_

# cluster's center point arr
station = kmeans.cluster_centers_ # result

# make 3clusters's 4station
resLine = []
for i in range(3) :
  resLine.append(bang.dfToListByIndex(df, i))
#print(resLine) # TEST PRINT
# run kmeans 3Line list
kmeansStation = []
for i in range(3) :
  kmeansStation.append(bang.kmeansAlgo(resLine[i], 4))

# geocoding university
stationRes = []
res_json = bang.adrsTogeo("한국산업기술대학교")

RES = []
# connect Graph
for i in range(3) :
  RES.append(
    bang.connectGraph(
      stationRes,
      kmeansStation[i],
      float(res_json[0]["lat"]),
      float(res_json[0]["lon"])
    )
  )
for i in range(3) :
  RES[i][0] = [
    float(res_json[0]["lat"]),
    float(res_json[0]["lon"])
    ]

# make graph
graph = dks.Graph(stationRes)

# save map html
m = folium.Map(
    location=[37.29720011, 127.03965907],
    zoom_start=9
)
indx = 1
colorL = ["green", "yellow", "orange"]
for i in range(3) :
  folium.PolyLine(RES[i], color=colorL[i], weight=2.5, opacity=1).add_to(m)
  folium.Marker(
    location=[station[i][0],station[i][1]],
    popup= str(i),
    icon=folium.Icon(color='blue',icon='star')
  ).add_to(m)
  for j in range(4) :
    folium.Marker(
      location=[kmeansStation[i][j][0],kmeansStation[i][j][1]],
      popup=str(indx),
      icon=folium.Icon(color='red',icon='star')
    ).add_to(m)
    indx += 1
m.save('./map.html')

###########################
###vvvv###PROGRAM###vvvv###
###########################

while True:
  # input
  print("주소를 입력하세요(종료하려면 exit)")
  user = input()
  if user == "exit":
    break
  # geocoding
  RES_json = bang.adrsTogeo(user)
  user_x = float(RES_json[0]["lat"])
  user_y = float(RES_json[0]["lon"])
  # find close station
  distancecmp = []
  for i in range(3):
    for index, var in enumerate(kmeansStation[i]) :
      #print(var)
      distancecmp.append(
        bang.findDistance(user_x, user_y, var[0], var[1])
      )
  idx = np.array(distancecmp) 
  root = graph.dijkstra(idx.argmin() + 1, 0)
  loop = len(root)

  # find distance home to station
  totalRes = 0

  # to station
  print(root)
  totalRes += (min(distancecmp) * 111) / 40
  print("집에서 정류장까지")
  print(str(int(totalRes)) + "시간 "
  + str(int(60 * (totalRes % 1))) + "분" )

  # move station
  rootDistance = []
  for i in range(loop - 1) :
    row = int((root[i] - 1) / 4)
    col = int(root[i] - 1) % 4
    if root[i] == 0 :
      sx = float(res_json[0]["lat"])
      sy = float(res_json[0]["lon"])
    else :
      sx = kmeansStation[row][col][0]
      sy = kmeansStation[row][col][1]
    row = int((root[i + 1] - 1) / 4)
    col = int(root[i + 1] - 1) % 4
    if root[i + 1] == 0 :
      sx = float(res_json[0]["lat"])
      sy = float(res_json[0]["lon"])
    else :
      dx = kmeansStation[row][col][0]
      dy = kmeansStation[row][col][1]
    rootDistance.append(
      bang.findDistance(
        sx, sy, dx, dy
      )
    )

  # to university
  totalRes += (sum(rootDistance) * 111) / 40
  print("집에서 학교까지")
  print(str(int(totalRes)) + "시간 "
  + str(int(60 * (totalRes % 1))) + "분" )


#print(addressJson)
#print(station)
#print(kmeansStation)
#print(root)
#print(stationRes)











