import asyncio
from client import ProtocolClient

async def main():
    print("Searching for Blauberg Vento devices on the network...")

    client = ProtocolClient(timeout=2.0)  # Increase timeout if needed
    devices = await client.find_devices()

    if not devices:
        print("No devices found.")
    else:
        print(f"Found {len(devices)} device(s):")
        for idx, device in enumerate(devices, start=1):
            print(f"{idx}. ID: {device.id}, IP: {device.ip}")

if __name__ == "__main__":
    asyncio.run(main())
