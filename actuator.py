import RPi.GPIO as GPIO
import time

# Konfigurasi pin
motor_in1 = 12
motor_in2 = 13
motor_en = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_en, GPIO.OUT)

pwm = GPIO.PWM(motor_en, 1000)  # Frekuensi PWM

# Fungsi untuk menggerakkan aktuator ke atas
def move_up(distance):
    # Ubah nilai ini sesuai dengan konversi ke duty cycle yang diperlukan
    # untuk menggerakkan aktuator sejauh 5cm, 10cm, 15cm, dan 20cm.
    if distance == 5:
        duty_cycle = 25
    elif distance == 10:
        duty_cycle = 50
    elif distance == 15:
        duty_cycle = 75
    elif distance == 20:
        duty_cycle = 100
    else:
        print("Jarak tidak valid")
        return
    
    GPIO.output(motor_in1, GPIO.HIGH)
    GPIO.output(motor_in2, GPIO.LOW)
    pwm.start(duty_cycle)
    time.sleep(5)  # Ubah durasi ini sesuai dengan kecepatan aktuator
    
    pwm.stop()
    GPIO.output(motor_in1, GPIO.LOW)

def move_down(distance):
    # Ubah nilai ini sesuai dengan konversi ke duty cycle yang diperlukan
    # untuk menggerakkan aktuator sejauh 5cm, 10cm, 15cm, dan 20cm.
    if distance == 5:
        duty_cycle = 25
    elif distance == 10:
        duty_cycle = 50
    elif distance == 15:
        duty_cycle = 75
    elif distance == 20:
        duty_cycle = 100
    else:
        print("Jarak tidak valid")
        return
    
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.HIGH)
    pwm.start(duty_cycle)
    time.sleep(5)  # Ubah durasi ini sesuai dengan kecepatan aktuator
    
    pwm.stop()
    GPIO.output(motor_in1, GPIO.LOW)

try:
    while True:
	print("Pilih naik atau turun : ")
	menu = str(input())
	if(menu=="naik"):
  		print("Pilih jarak naik (5/10/15/20 cm): ")
  		distance = int(input())
		move_up(distance)
  		print(f"Aktuator naik : {distance} cm")
	elif(menu=="turun"):
  		print("Pilih jarak turun (5/10/15/20 cm): ")
 	 	distance = int(input())
  		move_down(distance)
  		print(f"Aktuator turun : {distance} cm")
	else:
		print("Salah memasukkan perintah")	
	
        
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
