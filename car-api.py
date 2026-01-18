import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
car_api_key = os.getenv('CAR_API_KEY')
print(f"API Key loaded: {car_api_key is not None}")

CAR_API_URL = "https://carapi.app/api"

def get_car_years():
    try:
        response = requests.get(f"{CAR_API_URL}/years/v2", headers={ 'accept': 'text/plain', 'content-type': 'application/json' })
        response.raise_for_status()
        years_data = response.json()
        print(years_data)
        return years_data
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_car_makes(year):
    try:
        response = requests.get(f"{CAR_API_URL}/makes/v2/?year={year}", headers={ 'accept': 'text/plain', 'content-type': 'application/json' })
        response.raise_for_status()
        makes_data = response.json().get('data', {})
        # for each name in makes_data, store the name in a list
        makes_list = [make.get('name') for make in makes_data]
        print(makes_list)
        return makes_list
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_car_models(year, make):
    try:
        response = requests.get(f"{CAR_API_URL}/models/v2/?year={year}&make={make}", headers={ 'accept': 'text/plain', 'content-type': 'application/json' })
        response.raise_for_status()
        models_data = response.json().get('data', {})
        models_list = [model.get('name') for model in models_data]
        print(models_list)
        return models_list
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_car_submodels(year, make, model):
    try:
        response = requests.get(f"{CAR_API_URL}/submodels/v2/?year={year}&make={make}&model={model}", headers={ 'accept': 'text/plain', 'content-type': 'application/json' })
        response.raise_for_status()
        submodels_data = response.json().get('data', {})
        submodels_list = [submodel.get('submodel') for submodel in submodels_data]
        print(submodels_list)
        return submodels_list
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    years = get_car_years()
    makes = get_car_makes(2020)
    models = get_car_models(2020, "Toyota")
    submodels = get_car_submodels(2020, "Toyota", "Camry")