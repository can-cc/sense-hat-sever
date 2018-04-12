from crontabs import Cron, Tab
from sense_hat import SenseHat
from datetime import datetime
import time
import sqlite3

sense = SenseHat()
sense.clear()

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

current_data = None

def collect_pi_sense_hat_data():
    humidity = sense.get_humidity()
    temperature = sense.get_temperature()
    pressure = sense.get_pressure()
    created_at = time.time() * 1000

    current_data = {humidity: humidity, temperature: temperature, pressure: pressure}

    cursor.execute('INSERT INTO env_data (humidity, temperature, pressure, created_at) VALUES (?, ?, ?, ?)',
              (humidity, temperature, pressure, created_at))
    conn.commit()

# Will run with a 5 second interval synced to the top of the minute
Cron().schedule(
    Tab(name='run_my_job').every(minute=1).run(collect_pi_sense_hat_data)
).go()
