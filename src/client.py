import asyncio
from bleak import BleakScanner, BleakClient
from pynput.mouse import Button,Controller
mouse = Controller()

# UUID of the service and characteristic to interact with
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

#variables
rigthbutton = 0
leftbutton = 0
x,xvalue = 0
y =0
scroll =0
scrolllength =0

# Discovering and finding the device
async def scan_for_device():
    devices = await BleakScanner.discover()
    if len(devices) == 0:
        print("No Devices found")
        return None
    
    for device in devices:
        if device.name is None:
            print("Device name is None")
            continue

        if "GCVM_Server" in device.name:
            print("Device found")
            print(f"Device is {device}")
            return device
    return None

# Callback function to handle data received by notifications
def notification_callback(sender: int, data: bytearray):
    feed = data.hex()
    print(f"Notification received {feed}")
    print(data)

    



    mouse.move(x,y)

    if(scroll == 0):
        # click the mouse
        time = 1         # time the button clicks
        if(rigthbutton == 1):
            mouse.click(Button.right, time)
        elif(leftbutton == 1):
            mouse.click(Button.left, time)

    elif(scroll == 1):
        scrolllength = x
        mouse.scroll(0,scrolllength)
    

'''
    time_count = 0

    while time_count < 10:
        #take the position of the mouse
        pos = mouse.position
        print(pos)
        
        time_count += 1
'''                


async def interact_with_device(device):
    async with BleakClient(device) as client:
        # Check if the service with the specified UUID is available
        service = None
        for s in client.services:
            if s.uuid.lower() == SERVICE_UUID.lower():
                service = s
                print("Service Matchd")
                break
            
        if service is None:
            await client.disconnect()
            print("No matching service found. Client Disconnected")
        
        else:
            # Check if the characteristic with the specified UUID is available in the service
            for c in service.characteristics:
                if c.uuid.lower() == CHARACTERISTIC_UUID.lower():
                    characteristic = c
                    print("Characteristic Matchd")

                # Enable notifications for the characteristic
                await client.start_notify(characteristic, notification_callback)

                # Receive characteristic value as the device notifies for 10 seconds
                time_count = 0
                while time_count < 10:
                    await asyncio.sleep(1)
                    time_count += 1

                # Disconnect from the device after 10 seconds
                await client.disconnect()
                print("Client Disconnected")

async def main():
    print("Discovering...")
    device = await scan_for_device()
    if device:
        await interact_with_device(device)
    else:
        print("ESP32 device not found.")

asyncio.run(main())

# is this edit was in my branch