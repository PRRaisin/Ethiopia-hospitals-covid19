# Analysis of travel times to hospitals and health centers in Ethiopia
## A country-wide analysis to plan COVID-19 response
Forked from the [covid19 repository](https://github.com/datapartnership/covid19) from the Data Partnership authored by Bruno Sánchez-Andrade Nuño (@brunosan).
Adapted by TFE Energy. Learn more about our work on tfe.energy or write to philippe.raisin@tfe.energy.


## Donwload OSM data

Larger OSM datasets can be downloaded from Geofabrik [here](https://download.geofabrik.de/).
Select the .osm.pbf file of the country you want to study. 

## Prepare  OSRM
Once the OSM data has downloaded, navigate to the ./data folder where the .osm.pbf file is located and set up OSRM (here with the file "ethiopia-latest.osm.pbf" downloaded from Geofabrik):

    docker run -t -dv "$PWD:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/ethiopia-latest.osm.pbf
    docker run -t -v "$PWD:/data" osrm/osrm-backend osrm-contract /data/ethiopia-latest.osm.pbf
    docker run -t -i -p 5000:5000 -v $PWD:/data osrm/osrm-backend osrm-routed --algorithm ch /data/ethiopia-latest.osrm

To open the frontend, type:

    docker run -p 9966:9966 osrm/osrm-frontend
    open 'http://127.0.0.1:9966'
    
More information on how to set up OSRM can be found [here](https://github.com/Project-OSRM/osrm-backend).
    
## Facebook HRSL data
The 30m population high-resolution settlement layer for Ethiopia (in .geotiff format) can be downloaded [here](https://data.humdata.org/organization/facebook?q=ethiopia&ext_page_size=25).

## Hospital data
The dataset for the hospital dataset can be found [here](https://www.nature.com/articles/s41597-019-0142-2).
The files which were used in in this demonstration are saved in this repo under /data/ethiopia/raw. We divided the dataset
into one with all the hospitals and one with health centers.

**Important:** Some of the locations in the HRSL and hopsital data were not covered by the OSM data downloaded from the link above.
This can lead to errors from OSRM when queried. As such, the entries outside our OSM data were removed from the hospital and healthcare center dataset. 


