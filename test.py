"""Sample script to use the Python API client for Glances."""
import asyncio
from glances_api import Glances
import re

HOST = "192.168.1.200"
VERSION = 4


async def main():
    """The main part of the example script."""
    # data = Glances(version=VERSION)
    data = Glances(host=HOST, version=VERSION)
    print("Data got")
   
    print("Output to use with Home Assistant")
    print(await data.get_ha_sensor_data())


if __name__ == "__main__":
    asyncio.run(main())