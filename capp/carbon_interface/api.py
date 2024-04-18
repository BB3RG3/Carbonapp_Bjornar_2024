import requests
import json

url = 'https://www.carboninterface.com/api'
headers = {'Authorization': 'Bearer Q6eGoxxENeS3vpIoXkKOw'}


class CarbonAPI:
    def __init__(self):
        req = requests.get(url + "/v1/auth", headers=headers)
        reqJson = req.json()
        ## If 404, throw error
        if (req.status_code == 404):
            print("Error: 404")
        else:
            print("API is working")
            print(reqJson)

    def allVehicleMakes(self):
        req = requests.get(url + "/v1/vehicle_makes", headers=headers)
        #print(req.json())
        return req.json()
    
    def getVehicleMake(self, id):
        if id is None:
            print("ID is required")

        req = requests.get(url + "/v1/vehicle_makes/" + id + "/vehicle_models", headers=headers)
        vehicle_models = req.json()

        unique_models = {}

        for model in vehicle_models:
            name = model["data"]["attributes"]["name"]
            year = model["data"]["attributes"]["year"]
            if name not in unique_models or unique_models[name]["year"] < year:
                unique_models[name] = {"year": year, "model": model}

        unique_vehicle_models = [model["model"] for model in unique_models.values()]

        return unique_vehicle_models
    
    def getEstimate(self, id, distance):
        if id is None:
            print("ID is required")

        data = {
            "vehicle_model_id": id,
            "type": "vehicle",
            "distance_unit": "km",
            "distance_value": int(distance)
        }

        formatedUrl = url + "/v1/estimates"

        req = requests.post(url=formatedUrl, json=data, headers=headers)
        return req.json()
