import geopy
import geopy.distance
import mgrs
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import uvicorn

app=FastAPI()

class Location(BaseModel):
    location:str
    dist:float
    bearing:float

@app.post("/calculate_distination", status_code=status.HTTP_200_OK)

def calculate_distination(request:Location,response:Response):  
    try:  
        mgrs_object = mgrs.MGRS()

        # mgrsto latlon
        start = mgrs_object.toLatLon(request.location)
        # calculate geodesic distance between the two points
        distance_geodesic= geopy.distance.geodesic(meters = request.dist)
        # measure the distance point usinge the gedesic distance
        # return distance_geodesic.destination(point=start, bearing=bearing)
        distination_point= distance_geodesic.destination((start[0], start[1]), bearing=request.bearing)
        #return the result in MGRS 
        return {"distination": mgrs_object.toMGRS(distination_point[0],distination_point[1])}
    except:
        # response.status_code=status.HTTP_101_SWITCHING_PROTOCOLS

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1' , port=8000)