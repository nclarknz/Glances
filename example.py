"""Sample script to use the Python API client for Glances."""
import asyncio

# from glances_api import Glances
from glances2_api import Glances
import re

HOST = "192.168.1.200"
VERSION = 4


async def main():
    """The main part of the example script."""
    # data = Glances(version=VERSION)
    data = Glances(host=HOST, version=VERSION)
    print("Data got")
   
    
    # await data.get_data("all")
    # Get the metrics for the memory
    await data.get_metrics("amps")

    # Print the values
    print("Container values:", data.values)
    print("Now just the apt")
    aptresult = list(filter(lambda x:x["name"]=="Apt",data.values))[0]["result"]
    print(aptresult)
    noupdates = re.findall("^\d+",aptresult)
    print("Num Updates",int(noupdates[0]))

    # aptanswer = aptresult[0]["result"]
    # print(aptanswer)
    
    # # Get the metrics about the disks
    # await data.get_metrics("diskio")

    # # Print the values
    # print("Disk values:", data.values)

    # Get the data for Home Assistant
    print("Output to use with Home Assistant")
    print(await data.get_ha_sensor_data())


if __name__ == "__main__":
    asyncio.run(main())