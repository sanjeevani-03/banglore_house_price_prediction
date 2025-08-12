import json, pickle, os
import numpy as np

__locations = None
__model = None
__data_columns = None

# def load_saved_artifacts():
#     global __data_columns 
#     global __locations
    
#     print("Loading saved artifacts")
    
#     with open('server/artifacts/columns.json','r') as f:
#         __data_columns = json.load(f)['data_columns']
#         __locations = __data_columns[3:]
        
#     with open('server/artifacts/bengaluru_house_prices_model.pickle','rb') as f:
#         global __model
#         __model = pickle.load(f)
        
#     print("Artifacts loaded !")


def load_saved_artifacts():
    """
    Loads the saved artifacts (model and columns) from the file system.
    This function is called once when the server starts.
    """
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Get the absolute path of the directory where this file (util.py) is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct absolute paths to the artifact files
    columns_path = os.path.join(current_dir, "artifacts", "columns.json")
    model_path = os.path.join(current_dir, "artifacts", "bengaluru_house_prices_model.pickle")

    # Load the columns.json file
    with open(columns_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # The first 3 columns are sqft, bath, bhk

    # Load the pickle model file
    with open(model_path, 'rb') as f:
        __model = pickle.load(f)
        
    print("Artifacts loaded successfully!")

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