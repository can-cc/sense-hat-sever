import logging
from sense_hat import SenseHat
from datetime import datetime
from flask import Flask, jsonify
import time
import sqlite3
from flask_apscheduler import APScheduler

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

sense = SenseHat()
sense.clear()

class Store(object):
    env_data = {}
    def get(self):
        return self.env_data
    def set(self, env_data):
        self.env_data = env_data

def collect_pi_sense_hat_data(store):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    humidity = sense.get_humidity()
    temperature = sense.get_temperature()
    pressure = sense.get_pressure()
    created_at = time.time() * 1000

    current_data = {'humidity': humidity, 'temperature': temperature, 'pressure': pressure}

    cursor.execute('INSERT INTO env_data (humidity, temperature, pressure, created_at) VALUES (?, ?, ?, ?)',
              (humidity, temperature, pressure, created_at))
    logging.info(current_data)
    store.set(current_data)
    conn.commit()
    conn.close()


class Config(object):
    def __init__(self, store):
        self.store = store
        self.JOBS = [
            {
                'id': 'job1',
                'func': 'main:collect_pi_sense_hat_data',
                'args': ([store]),
                'trigger': 'cron',
                'second': 0
            }
        ]
    SCHEDULER_API_ENABLED = True

if __name__ == '__main__':
    app = Flask(__name__)
    store = Store()
    app.config.from_object(Config(store))

    @app.route('/hello')
    def route_hello_world():
        return 'Hello, World!'

    @app.route('/env')
    def route_env():
        current_data = store.get()
        logging.info(current_data)
        return jsonify(current_data)

    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run(host='0.0.0.0', port=6000)
