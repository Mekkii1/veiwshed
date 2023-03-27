import numpy as np
import rasterio
from fastapi import FastAPI, HTTPException, status
import uvicorn
import json

app=FastAPI()


def viewshed(dem, observer_loc, radius):
        # Load DEM data
        with rasterio.open(dem) as src:
            demx = src.read(1, out_shape=(src.height // 2, src.width // 2))

        # Define variables
        nrows, ncols = demx.shape
        observer_row, observer_col = int(observer_loc[0]), int(observer_loc[1])
        
        # Define empty array to store visibility values
        visibility = np.zeros_like(demx)
        
        # Iterate over cells within radius of observer
        for row in range(max(0, int(observer_row-radius)), min(nrows, int(observer_row+radius+1))):
            for col in range(max(0, int(observer_col-radius)), min(ncols, int(observer_col+radius+1))):
                # Calculate distance and slope to observer
                dx = col - observer_col
                dy = row - observer_row
                distance = np.sqrt(dx*dx + dy*dy)
                slope = (demx[observer_row, observer_col] - demx[row, col]) / distance
                
                # Check line-of-sight to observer
                visible = True
                step = np.sign(dy) if dy != 0 else 1
                for r in range(observer_row, row, step):
                    c = int(observer_col + (r-observer_row)*dx/dy)
                    if demx[r, c] - demx[observer_row, observer_col] > slope*(distance - np.sqrt((c-observer_col)*(c-observer_col) + (r-observer_row)*(r-observer_row))):
                        visible = False
                        break
                
                # Set visibility value in array
                visibility[row, col] = visible
           
        return visibility

      

@app.get("/viewshedo", status_code=status.HTTP_200_OK)

# Define function for Viewshed analysis
async def viewsheds( observer_loc, radius):

    with rasterio.open(r"D:\work\line-of-sight\alos.tif") as src:
     demx = src.read(1, out_shape=(src.height // 2, src.width // 2))
    
    visibility = viewshed(demx, observer_loc, radius)

    return json.dumps(visibility) 


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1' , port=8000)