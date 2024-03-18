# -*- coding: utf-8 -*-
"""

@author: Brais Lorenzo Fernandez
"""

Key = "&key=" + "" #Here you insert the KEY from the API that you create on the GCP


import random as rd
import os
import json
import urllib.request
DownLoc = "" #Insert path where you want to download your images 


# =============================================================================
# Functions
# =============================================================================
def MetaParse(MetaUrl): #MetaParse returns "date" "id", "latitude" and "longitude"
    response = urllib.request.urlopen(MetaUrl)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    if jsonData['status'] == "OK":
        if 'date' in jsonData:
            return (jsonData['date'],jsonData['pano_id'],jsonData['location']['lat'],jsonData['location']['lng']) #sometimes it does not have a date!
        else:
            return (None,jsonData['pano_id'])
    else:
        return (None,None)
    
def GetStreetLL(Lat,Lon,Head,SaveLoc):  #GetStreet con return real Lat Lon
    base = r"https://maps.googleapis.com/maps/api/streetview"
    size = r"?size=640x640&fov120&location=" #max resolution , max FOV 120
    end = str(Lat) + "," + str(Lon) + "&heading=" + str(Head) + key
    MyUrl = base + size + end
    MetaUrl = base + r"/metadata" + size + end
    #print MyUrl, MetaUrl #can check out image in browser to adjust size, fov to needs
    met_lis = list(MetaParse(MetaUrl))                           #does not grab image if no date
    if len(met_lis) > 2:  
        fi = str(met_lis[2]) + "_" + str(met_lis[3]) + "_" + str(int(Head)) + ".jpg"
    else:
        fi = None       
    if (met_lis[1],Head) not in PrevImage and met_lis[0] is not None and fi is not None:   #PrevImage is global list
        urllib.request.urlretrieve(MyUrl, os.path.join(SaveLoc,fi))
        met_lis.append(fi)
        PrevImage.append((met_lis[1],Head)) #append new Pano ID to list of images
    else:
        met_lis.append(None)
    return met_lis 

# =============================================================================
# Creating the list of request points
# =============================================================================

dataList = []

entries = 50 #Put Number of desired entries here

ini_lat =  #Initial latitude (example:53.895032 )
fin_lat =  #Final latitude (example:53.991111 )

ini_lon =  #Initial longitude (example:-2.002379 )
fin_lon =  #Final longitude (example:-1.994474 )


for i in range(1,entries):
    lat_random = round(rd.uniform(ini_lat,fin_lat ), 6) #Creates latitude between point a and b, rounded to 6 decimals
    lon_random = round(rd.uniform(ini_lon,fin_lon), 6) #Createslongitude between point a and b, rounded to 6 decimals
    point_N = (lat_random,lon_random,2)
    point_E = (lat_random,lon_random,92)
    point_S = (lat_random,lon_random,182)
    point_W = (lat_random,lon_random,272)
    dataList.append(point_N)
    dataList.append(point_E)
    dataList.append(point_S)
    dataList.append(point_W)


# =============================================================================
# The iteration of the entries, The actual production
# =============================================================================
 
PrevImage = []   
image_list = [] #to stuff the resulting meta-data for images

    
for i in dataList: #Iterates over the array of lat/lon points
    temp = GetStreetLL(Lat=i[0],Lon=i[1],Head=i[2],SaveLoc=DownLoc) 
    if temp[2] is not None:
        image_list.append(temp)

# =============================================================================
# Health checks
# =============================================================================   

len(image_list)  
len(DataList) 