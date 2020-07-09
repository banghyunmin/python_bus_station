# geocoding
import requests
# json
import json
# sqr
import math
# K-Means
import pandas as pd
from sklearn.cluster import KMeans
# visual x-y
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
###############################
#####USER FUNCTION LIBRARY#####
###############################

url = "https://us1.locationiq.com/v1/search.php"

#FUNC#
# get address to geocoding
def adrsTogeo(address):
  adrs_data = {
          'key': 'pk.b3db7890aed8df517be541bc1faeabb4',
          'q': address,
          'format': 'json'
      }
  adrs_response = requests.get(url, params=adrs_data)
  adrs_res_json = json.loads(adrs_response.text)
  return adrs_res_json

# FUNC #
# dot to dot distance
def findDistance(sx, sy, dx, dy) :
    xGap = sx - dx
    yGap = sy - dy
    distance = math.sqrt((xGap*xGap) + (yGap*yGap))
    return distance

# FUNC #
# convert ndarray to number
def ndaToNum(a, point):
  return list(a)[point]

# FUNC #
# convert dataFrame to list by kmeans index
def dfToListByIndex(df, index):
  dflist = df.values.tolist()
  res = []
  for i, val in enumerate(dflist) :
    if val[2] == index :
      res.append(val)
  return res

# FUNC #
# run keans algorithm
def kmeansAlgo(arr, number):
  df = pd.DataFrame(columns=('x', 'y'))
  for index, val in enumerate(arr) :
    df.loc[index] = [float(val[0]), float(val[1])]
  # clustering
  data_points = df.values
  res = KMeans(n_clusters = number).fit(data_points)
  df['cluster_id'] = res.labels_
  return res.cluster_centers_

# FUNC #
# get node to node distance
def getDistanceNTON(data, sx, sy):
  listKmean = []
  for var in data:
    listKmean.append(
      findDistance(var[0], var[1],  sx, sy)
    )
  return listKmean

# FUNC #
# connect graph
def connectGraph(G, data, x, y):
  RES = []
  RES.append([])
  init = len(G) + 1
  pre_index = 0
  sx = x
  sy = y
  pre_x = x
  pre_y = y
  lum = []
  for var in data:
    lum.append(var)
  for i in range(4):
    lam = getDistanceNTON(
      lum,
      sx,
      sy
    )
    idx = np.array(lam)

    sx = list(lum[idx.argmin()])[0]
    sy = list(lum[idx.argmin()])[1]
    lam[idx.argmin()] = 10
    lum[idx.argmin()] = [ 0, 0]
    index = init + idx.argmin()

    G.append(
      (
        index,
        pre_index,
        findDistance(
          pre_x,
          pre_y,
          sx,
          sy
        )
      )
    )
    RES.append([sx, sy])
    pre_x = sx
    pre_y = sy
    pre_index = index
  return RES











  