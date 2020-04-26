
import numpy as np
import rasterio
import logging
import os
import pandas as pd
from rasterio.windows import Window
from matplotlib import pyplot
import matplotlib.pyplot as plt
import geopandas as gdp
from shapely.geometry import Point
from shapely.geometry import box
import requests #http framework to make mhvpl requests for routes
import json # handle response as json
from geopy.distance import vincenty
import pickle


def get_population_data(map_file,left_x,top_y,window,plot=False):

    right_x,bottom_y = left_x + window, top_y + window

    with rasterio.open(map_file) as src:
        left_lon, top_lat = src.xy(top_y,left_x)
        right_lon, bottom_lat = src.xy(bottom_y, right_x )
        center_lon , center_lat = (right_lon + left_lon)/2., (top_lat+bottom_lat)/2.
        #Window(col_off, row_off, width, height)
        w = src.read(1, window=Window(left_x, top_y, window, window))
        if plot:
            pyplot.imshow(w, cmap='pink')
            pyplot.show()
        nancount=np.count_nonzero(~np.isnan(w))
        count = np.size(w)
        tot_pop=np.nansum(w)
    if count == 0:
        return {} #Out of bounds
    if tot_pop == 0 or window < 1: #Mark the window no further split.
        split=False
    else:
        split=True
    out={'window':window,
         'left_x':left_x,
         'right_x':right_x,
         'top_y':top_y,
         'bottom_y':bottom_y,
         'left_lon':left_lon,
         'top_lat':top_lat,
         'right_lon':right_lon,
         'bottom_lat':bottom_lat,
         'center_lon':center_lon ,
         'center_lat':center_lat,
         'count': count,
         'nancount':nancount,
         'tot_pop':tot_pop,
         'split': split}
    return out

def split(map_file,origin,plot=False):
    """
    Split a window row in 4 parts, and return new rows results
    """
    origins=pd.DataFrame()
    window=int(origin.window/2)
    for left_x in np.arange(origin.left_x,origin.right_x,window):
        for top_y in np.arange(origin.top_y,origin.bottom_y,window):
            out=get_population_data(map_file,left_x,top_y,window,plot=plot)
            if out != {}:
                origins=origins.append([out])
    return origins

def n_closest_geodetic(destinations,origins,n_keep,verbose=False):
    """
    Given a list of origins and destinations, return the "keep" number
    of destinations that are closest geodetically to each origin.

    Input: destinations,origins <Geopandas>
    Output: destinations filtered <Geopandas>
    """
    #destinations=destinations.to_crs(origins.crs)
    filtered=gdp.GeoDataFrame()

    if verbose:
        i=0
        l=len(origins.index)
    for index in origins.index:
        if verbose:
            i=i+1
            print("Doing %i of %i\r"%(i,l),end="")
        distances = destinations.distance(origins.loc[index].geometry)
        if len(distances) < n_keep:
            n_keep = len(distances)
        indices=np.argsort(distances.values)[:n_keep]
        values=np.sort(distances.values)[:n_keep]
        d_indices=distances.index[indices]
        filtered = filtered.append(destinations.iloc[indices])

    if verbose:
        print('done')
    return filtered.append(filtered).drop_duplicates(inplace=False)
