import paho.mqtt.client as mqtt
import ssl
import threading, queue
from influxdb import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

#Global variables
working = False
data_queue = queue.Queue()

#Setting up
#----InfluxDB----
INFLUXDB_HOST = {
    'address': 'localhost',
    'port': 8086,
    'token': 'LXaxLj4KBb99d1cJcSKf23nIYcj-MedXa86d3R7muUa_3SFPj6A8GYIRKJidanVS6-JZ5BRRpSdx2c-tnJnvew==',
    'org': 'IFE',
    'bucket': 'biolab'
}

# Function to save data to InfluxDB
def influxdb_writer():
    client = InfluxDBClient(host=INFLUXDB_HOST['address'], 
                            port=INFLUXDB_HOST['port'], 
                            token=INFLUXDB_HOST['token'],
                            org=INFLUXDB_HOST['org'])
    write_api = client.write_api(write_options=SYNCHRONOUS)

    global working
    while (working or not data_queue.empty()):
        data = data_queue.get()
        #write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)


#----MQTT----
# Define the broker address, port, username, and password
MQTT_BROKER = {
    'address': "v8517e16.ala.us-east-1.emqxsl.com",
    'port': 8883,  # TLS/SSL port
    'username': "ife",  # Replace with your MQTT username
    'password': "ife",  # Replace with your MQTT password
}

MQTT_METADATA = {
    'namespace': 'org.ife.biolab',
    'gyrotopic': 'org.ife.biolab/gyroscope',
    'motiontopic': 'org.ife.biolab/motion',
}
# Function to listen to MQTT messages
def mqtt_listener():
    def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(MQTT_METADATA['gyrotopic'])
        client.subscribe(MQTT_METADATA['motiontopic'])

    def on_message(client, userdata, message):
        data = message.payload.decode()
        print("I got a data ", data)
        #data_queue.put(data)

    # Create a client instance
    client = mqtt.Client()

    # Set up the client to use SSL/TLS
    context = ssl.create_default_context(cafile='emqxsl-ca.crt')
    client.tls_set_context(context)
    client.username_pw_set(MQTT_BROKER['username'], MQTT_BROKER['password'])

    # Set up the client callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect
    client.connect(MQTT_BROKER['address'], MQTT_BROKER['port'], 60)  # 60 is waiting interval

    client.loop_forever()

if __name__ == '__main__':
    working = True
    mqtt_thread = threading.Thread(target=mqtt_listener)
    #influxdb_thread = threading.Thread(target=influxdb_writer)
    mqtt_thread.start()
    #influxdb_thread.start()
