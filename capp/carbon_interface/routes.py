from capp.carbon_interface.api import CarbonAPI
from flask import Blueprint

api = CarbonAPI()

carbon_interface = Blueprint('carbon_interface',__name__)

#API
@carbon_interface.route('/carbon_interface/cars')
def allV():
    return api.allVehicleMakes()

@carbon_interface.route('/carbon_interface/models/<id>')
def getMakes(id):
    return api.getVehicleMake(id)
