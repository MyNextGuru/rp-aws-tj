from awsiot import mqtt_connection_builder
from awscrt import mqtt, io
import time
import sys

# Callback when connection is successful
def on_connection_success(connection, callback_data):
    print("Connected successfully")

# Callback when connection fails
def on_connection_failure(connection, callback_data):
    print("Connection failed")

# Define parameters (replace with yours)
endpoint = "a2av9khq02vv6l-ats.iot.ap-south-1.amazonaws.com"
cert_path = "/home/gosky/rp-aws-tj/certs/373af50bd1cfcd588533332f775edfe5d381b19a6672fdf34bb45c9630fa1b48-certificate.pem.crt"
key_path = "/home/gosky/rp-aws-tj/certs/373af50bd1cfcd588533332f775edfe5d381b19a6672fdf34bb45c9630fa1b48-private.pem.key"
ca_path = "/home/gosky/rp-aws-tj/certs/AmazonRootCA1.pem"
client_id = "gstRPtest"
topic = "test/topic"

# Build the MQTT connection with mTLS
io.init_logging(getattr(io.LogLevel, 'Error'), 'stderr')
connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    cert_filepath=cert_path,
    pri_key_filepath=key_path,
    ca_filepath=ca_path,
    client_id=client_id,
    clean_session=False,
    keep_alive_secs=30,
    on_connection_success=on_connection_success,
    on_connection_failure=on_connection_failure
)

# Connect
connect_future = connection.connect()
connect_future.result()  # Wait for connection
print("Connected!")

# Subscribe to topic
subscribe_future, _ = connection.subscribe(topic=topic, qos=mqtt.QoS.AT_LEAST_ONCE, callback=lambda topic, payload, **kwargs: print(f"Received on {topic}: {payload.decode()}"))
subscribe_future.result()

# Publish a test message
connection.publish(topic=topic, payload="Hello from Raspberry Pi!".encode(), qos=mqtt.QoS.AT_LEAST_ONCE)

# Keep the connection alive
while True:
    time.sleep(1)

# To disconnect: connection.disconnect().result()
