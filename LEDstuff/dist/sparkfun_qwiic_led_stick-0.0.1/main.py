import qwiic_led_stick as q, time

if __name__ == "__main__":
    LED = q.QwiicLEDStick()
    if LED.is_connected():
        LED.begin()
        LED.set_all_LED_color(0, 0, 255)    #blue
        percentage = 0                      #incoming data from weight sensor?
        while percentage <= 100:
            LED.set_single_LED_brightness(percentage/10, 31)
            #!!replace next two lines with updating percentage!!
            percentage += 1
            time.sleep(0.1)
        #blink LED's to signal done
        for i in range(0, 5):
            LED.LED_off()
            time.sleep(0.5)
            LED.set_all_LED_brightness(31)
            time.sleep(0.5)
        LED.set_all_LED_brightness(0)