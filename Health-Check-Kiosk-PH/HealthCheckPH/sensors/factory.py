from config import SENSOR_MODE
from sensors.simulated import SimulatedSensorService
from sensors.real import RealSensorService


def get_sensor_service():
    if SENSOR_MODE == "real":
        return RealSensorService()

    return SimulatedSensorService()