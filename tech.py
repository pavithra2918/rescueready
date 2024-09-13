

import asyncio
from bleak import BleakClient, BleakScanner

# UUIDs for the services and characteristics (replace with actual UUIDs)
HEART_RATE_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HEART_RATE_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
OXYGEN_SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
OXYGEN_CHAR_UUID = "00002a38-0000-1000-8000-00805f9b34fb"

# Threshold values for alerts
HEART_RATE_MAX = 100
HEART_RATE_MIN = 60
OXYGEN_MIN = 90

# Simulated alert function
def send_alert(message):
    print(f"ALERT: {message}")

# Callback function to handle notifications from the BLE device
def handle_vitals_data(sender, data):
    # Parse heart rate and oxygen data (example parsing, adjust as per device format)
    heart_rate = int.from_bytes(data[:1], byteorder="little") # Example: first byte for heart rate
    oxygen_level = int.from_bytes(data[1:2], byteorder="little") # Example: second byte for oxygen

    print(f"Heart Rate: {heart_rate} BPM, Oxygen Level: {oxygen_level}%")

    # Check for abnormalities
    if heart_rate > HEART_RATE_MAX or heart_rate < HEART_RATE_MIN:
        send_alert(f"Abnormal heart rate detected: {heart_rate} BPM")
    if oxygen_level < OXYGEN_MIN:
        send_alert(f"Low oxygen level detected: {oxygen_level}%")

async def monitor_vitals(device_address):
    async with BleakClient(device_address) as client:
        # Check connection
        connected = await client.is_connected()
        if not connected:
            print(f"Failed to connect to device: {device_address}")
            return
        print(f"Connected to {device_address}")

        # Start notifications for heart rate and oxygen levels
        await client.start_notify(HEART_RATE_CHAR_UUID, handle_vitals_data)
        await client.start_notify(OXYGEN_CHAR_UUID, handle_vitals_data)

        # Keep the connection alive for monitoring (e.g., 60 seconds)
        await asyncio.sleep(60)

        # Stop notifications
        await client.stop_notify(HEART_RATE_CHAR_UUID)
        await client.stop_notify(OXYGEN_CHAR_UUID)

async def main():
    # Scan for BLE devices
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    
    for device in devices:
        print(f"Device found: {device.name}, {device.address}")
        # Assuming you know the device's name or address
        if "WearableDevice" in device.name: # Replace with actual device name
            print(f"Connecting to {device.name} ({device.address})")
            await monitor_vitals(device.address)
            break
    else:
        print("Device not found")

if __name__ == "__main__":
    asyncio.run(main())