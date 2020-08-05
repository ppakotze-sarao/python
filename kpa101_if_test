import clr # provided by pythonnet, .NET interface layer
import sys
import time

# this is seriously nasty.  Points for a better way of fixing this!
sys.path.append(r"C:\Program Files\Thorlabs\Kinesis")

# NB the
#ppak addition
clr.AddReference("Thorlabs.MotionControl.KCube.PositionAlignerCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("System")

#ppak addition
#from Thorlabs.MotionControl.KCube.PositionAlignerCLI import PositionAlignerCLI
from Thorlabs.MotionControl.KCube.PositionAlignerCLI import KCubePositionAligner
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from System import Decimal

def list_devices():
    """Return a list of Kinesis serial numbers"""
    DeviceManagerCLI.BuildDeviceList()
    return DeviceManagerCLI.GetDeviceList()

#help(KCubePositionAligner)
print(list_devices())
serial=str(69250950)
#serial=str(69000001)
kpa101 = KCubePositionAligner.CreateKCubePositionAligner(serial)
kpa101.Connect(serial)

time.sleep(0.5) # ThorLabs have this in their example...

#kpa101.StartPolling(250);
#kpa101.EnableDevice();

print(kpa101.get_DeviceName())
print(kpa101.get_Status())
print("Closed Number X: %3.5f"%kpa101.GetClosedLoopPosition().X)
print("Closed Number Y: %3.5f"%kpa101.GetClosedLoopPosition().Y)
print("Demand Number X: %3.5f"%kpa101.GetDemandedPosition().X)
print("Demand Number Y: %3.5f"%kpa101.GetDemandedPosition().Y)
print("Difference Number X: %3.5f"%kpa101.get_Status().PositionDifference.X)
print("Difference Number Y: %3.5f"%kpa101.get_Status().PositionDifference.Y)
print("Difference Number X: %3.5f"%kpa101.Status.PositionDifference.X)
print("Difference Number Y: %3.5f"%kpa101.Status.PositionDifference.Y)
#kpa101.Disconnect()

