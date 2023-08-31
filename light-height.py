import RPi.GPIO as GPIO
import time
import requests

# Konfigurasi pin GPIO untuk LDR, Relay, dan Sensor Ultrasonik
LDR_PIN = 18
RELAY_PIN = 17
TRIG_PIN = 23
ECHO_PIN = 24

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBFF-ZYy5X8YNWMGNwaTX4nhqo4RgeydRhB"
DEVICE_LABEL = "sic157"
LDR_VARIABLE_LABEL = "LEDLDR"
ULTRASONIC_VARIABLE_LABEL = "ultrasonic"
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"

GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def read_ldr():
    return GPIO.input(LDR_PIN)

def control_led(state):
    GPIO.output(RELAY_PIN, state)

def get_distance():
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.2)

    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def send_to_ubidots(ldr_value, ultrasonic_value):
    payload = {
        LDR_VARIABLE_LABEL: ldr_value,
        ULTRASONIC_VARIABLE_LABEL: ultrasonic_value
    }
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(UBIDOTS_URL, json=payload, headers=headers)
    print("Data sent to Ubidots:", response.status_code)

try:
    while True:
        ldr_value = read_ldr()
        if ldr_value == 1:
            control_led(GPIO.HIGH)
        else:
            control_led(GPIO.LOW)

        distance = get_distance()
        print(f"Distance: {distance} cm")

        send_to_ubidots(ldr_value, distance)

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
