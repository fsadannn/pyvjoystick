import my_pyvjoy
import my_pyvjoy._sdk as sdk
from my_pyvjoy.constants import HID_USAGE

rID = 1

devive = my_pyvjoy.VJoyDevice(rID)

res = sdk.GetNumberExistingVJD()
print(type(res))
print(res)

# for i in HID_USAGE:
#     res = sdk.GetVJDAxisMax(rID, i.value)
#     print(type(res))
#     print(res)
#     res = sdk.GetVJDAxisMin(rID, i.value)
#     print(res)
