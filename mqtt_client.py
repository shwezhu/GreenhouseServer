from datetime import datetime
import paho.mqtt.client as mqtt
import logging


# Message is an object and the payload property contains the message data which is binary data.
# The actual message payload is a binary buffer.
# In order to decode this payload you need to know what type of data was sent.
# If it is JSON formatted data then you decode it as a string and then decode the JSON string as follows:
# decoded_message=str(message.payload.decode("utf-8")))
# msg=json.loads(decoded_message)
class MQTTClient:
    def __init__(self, database_connection):
        self._db = database_connection

        self._client = mqtt.Client('greenhouse_server')
        self._client.message_callback_add('greenhouse/temperature', self.__on_message)
        self._client.message_callback_add('greenhouse/humidity', self.__on_message)

        # IP address of your MQTT broker, using ipconfig to look up it
        self._client.connect('localhost', 1883)

    def start_monitor(self):
        # paho.mqtt has threading built in, calling a loop start (instead of a loop forever)
        # will spin it off into its own thread, and it won't interfere with the while loop.
        self._client.loop_start()
        self._client.subscribe("greenhouse/#")

    def __on_message(self, _client, _userdata, msg):
        if str(msg.topic) == 'greenhouse/temperature':
            sql = "insert into temperature (temperature, time) values (%s, %s)"
        else:
            sql = "insert into humidity (humidity, time) values (%s, %s)"
        raw_data = msg.payload.decode('utf-8')
        try:
            data = float(raw_data)
        except ValueError as err:
            logging.error(str(err) + ' The data was %s from topic: %s', raw_data, msg.topic)
            return None

        value = (data, datetime.now().strftime('%Y-%m-%d %H:%M'))
        self._db.execute(sql=sql, params=value)
