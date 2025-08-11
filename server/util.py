import json, pickle
import numpy as np

__locations = None
__model = None
__data_columns = None

def load_saved_artifacts():
    global __data_columns 
    global __locations
    
    print("Loading saved artifacts")
    
    with open('server/artifacts/columns.json','r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
        
    with open('server/artifacts/bengaluru_house_prices_model.pickle','rb') as f:
        global __model
        __model = pickle.load(f)
        
    print("Artifacts loaded !")


def get_location_names():
    return __locations

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
        
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    
    if(loc_index>=0):
        x[loc_index] = 1
        
    result = round(__model.predict([x])[0],2)
        
    return result

if __name__ == "__main__":
    print("Loading saved artifacts...")