# import lcd

# lcd.init()
# lcd.draw_string(100, 100, "hello", lcd.RED, lcd.BLACK)

import sensor
import image
import lcd

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
while True:
    img=sensor.snapshot()
    lcd.display(img)

