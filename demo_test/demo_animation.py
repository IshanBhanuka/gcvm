import pygame
import random
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

port = "COM16"
baud_rate = 9600

# ser = serial.Serial(port, baud_rate)
# period = 100

file_name = "trial2_data.txt"
fh = open(file_name)

pygame.init()

WIDTH = 1000
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Animation")
clock = pygame.time.Clock()

centerX = WIDTH // 2
centerY = HEIGHT // 2

x_data = [centerX, centerX, centerX, centerX]
y_data = [centerY, centerY, centerY, centerY]

color = (255, 0, 0)

running = True
end = False
count = 0
acc = []
accAng = []
gyroAcc = []
gyroAng = []

while running and end == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill((0, 0, 0))


    try:
        # data = ser.readline().decode().rstrip()  # Read a line of serial data
        data = fh.readline().rstrip()   # Read a line from text data file
        vals = data.split(" : ")[1:]
        count+=1
        if len(data) < 1:
            end = True

    except:
        continue

    time.sleep(0.01)   
    # Update the position and color of the animated object based on input values
    try: 
        # X-Y Acceleration - Approaches Steady state
        y_data[0] = centerY - float(vals[0])*50
        x_data[0] = centerX + float(vals[1])*50

        # X-Y Acceleration Angle - Approaches Steady state
        x_data[1] = centerX + float(vals[6])    
        y_data[1] = centerY + (float(vals[7]))

        # Gyro acceleration (X-Y)
        # x_data[2] += float(vals[3])*0.5
        # y_data[2] += float(vals[4])*0.5
        
        # Gyro Angles
        x_data[3] = centerX + float(vals[8])
        y_data[3] = centerY + float(vals[9])

        # color = (255*(0.5 + float(vals[-1])/2), 250*(float(vals[-3])), 250*(float(vals[-2])))
        # print(vals[8:11])
    except:
        continue

    print(x_data, y_data, "Count: ", count)

    acc.append((x_data[0], y_data[0]))
    accAng.append((x_data[1], y_data[1]))
    gyroAcc.append((float(vals[3]), float(vals[4])))
    gyroAng.append((x_data[3], y_data[3]))

    # Draw the animated object
    if count < 5:
        x_data[2] = centerX
        y_data[2] = centerY
        pass
    else:
        x_data[0] = 0.25*(acc[count-1][0] + acc[count-2][0] + acc[count-3][0] + acc[count-4][0])
        y_data[0] = 0.25*(acc[count-1][1] + acc[count-2][1] + acc[count-3][1] + acc[count-4][1])
        
        x_data[1] = 0.25*(accAng[count-1][0] + accAng[count-2][0] + accAng[count-3][0] + accAng[count-4][0])
        y_data[1] = 0.25*(accAng[count-1][1] + accAng[count-2][1] + accAng[count-3][1] + accAng[count-4][1])

        x_data[3] = 0.25*(gyroAng[count-1][0] + gyroAng[count-2][0] + gyroAng[count-3][0] + gyroAng[count-4][0])
        y_data[3] = 0.25*(gyroAng[count-1][1] + gyroAng[count-2][1] + gyroAng[count-3][1] + gyroAng[count-4][1])

        x_data[2] = x_data[2] + (gyroAcc[count-1][0] - gyroAcc[count-2][0])
        y_data[2] = y_data[2] + (gyroAcc[count-1][1] - gyroAcc[count-2][1])

        x = x_data[0]*0.5 + x_data[1]*0.1 + x_data[2]*0.1 + x_data[3]*0.2
        y = y_data[0]*0.5 + y_data[1]*0.1 + y_data[2]*0.1 + y_data[3]*0.2
        
    pygame.draw.circle(window, (255, 255, 255), (x, y), 10)

    pygame.draw.circle(window, (100, 0, 0), (x_data[0], y_data[0]), 10)
    pygame.draw.circle(window, (0, 100, 0), (x_data[1], y_data[1]), 10)
    pygame.draw.circle(window, (100, 100, 100), (x_data[2], y_data[2]), 10)
    pygame.draw.circle(window, (0, 0, 100), (x_data[3], y_data[3]), 10)

    # Update the display
    pygame.display.flip()

    # Control the y_data rate
    clock.tick(60)

    # Quiting Mechanism (Tap all three touches)
    # if int(vals[-3]) == 1 and float(vals[-2]) == 1 and float(vals[-1]) == 1:
    #     running = False

# Quit pygame
pygame.quit()

fh.close()

print('\n')
print("Count ", count)