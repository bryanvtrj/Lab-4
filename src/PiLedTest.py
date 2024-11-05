import RPi.GPIO as GPIO
import time
from hal import hal_led as led
from hal import hal_input_switch as switch

# Initialize the pins for the LED and switch
LED_PIN = 24
SWITCH_PIN = 22

def blink_led(frequency, duration):
    """Blink the LED at a specified frequency for a certain duration."""
    led.init()  # Ensure the LED is initialized
    delay = 1 / (2 * frequency)  # Calculate the delay for the given frequency
    end_time = time.time() + duration  # Calculate the end time

    while time.time() < end_time:
        led.set_output(LED_PIN, 1)  # Turn the LED on
        time.sleep(delay)           # Wait for the on duration
        led.set_output(LED_PIN, 0)  # Turn the LED off
        time.sleep(delay)           # Wait for the off duration

    # After blinking, ensure the LED is off
    led.set_output(LED_PIN, 0)  

def main():
    # Initialize the input switch
    switch.init()  # Set up the switch
    led.init()     # Set up the LED

    try:
        while True:
            switch_position = switch.read_slide_switch()  # Read the switch state
            
            if switch_position == 1:  # Assuming 1 means left position
                blink_led(5, 1)  # Blink the LED at 5 Hz for 1 second
            elif switch_position == 0:  # Assuming 0 means right position
                print("Switch is to the right. Blinking LED at 10 Hz for 5 seconds.")
                blink_led(10, 5)  # Blink the LED at 10 Hz for 5 seconds
                time.sleep(1)  # Add a small delay to prevent immediate re-detection
            else:  # If switch is not in a valid state
                led.set_output(LED_PIN, 0)  # Turn the LED off
                time.sleep(0.1)  # Small delay to prevent busy looping

    except KeyboardInterrupt:
        # Clean up on exit
        led.set_output(LED_PIN, 0)  # Turn off the LED
        GPIO.cleanup()  # Reset GPIO settings
        print("Program stopped.")

# Main entry point
if __name__ == "__main__":
    main()
