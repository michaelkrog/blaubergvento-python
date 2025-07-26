import asyncio

from src.blauberg_vento.client.client import Client
from src.blauberg_vento.client.speed import Speed


async def main():
    resource = Client()

    # 1. List devices (first page, 20 per page)
    devices = await resource.find_all(page=0, size=20)
    print(f"Total devices returned: {len(devices)}")
    for device in devices:

        print(f"Device ID: {device.id}, IP: Do-no, Mode: {device.mode}, Speed: {device.speed}")

    # 2. Find a specific device by ID
    device_id = devices[0].id if devices else None
    if device_id:
        device = await resource.find_by_id(device_id)
        print(f"\nDetails of device {device_id}: Mode={device.mode}, Speed={device.speed}")

        # 3. Modify device properties and save
        device.speed = Speed.HIGH
        updated_device = await resource.save(device)
        print(f"Updated device speed: {updated_device.speed}")

if __name__ == "__main__":
    asyncio.run(main())
