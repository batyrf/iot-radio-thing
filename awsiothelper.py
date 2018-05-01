from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time, json

class helper():
    def __init__(self, customCallback, **kwargs):
        self.host = kwargs.get("e")
        self.rootCAPath = kwargs.get("r")
        self.certificatePath = kwargs.get("c")
        self.privateKeyPath = kwargs.get("k")

        self.useWebsocket = kwargs.get("w") if kwargs.get('w') else False
        self.clientId = kwargs.get("id") if kwargs.get("id") else 'basicPubSub'
        self.topic = kwargs.get("t") if kwargs.get("t") else "sdk/test/Python"
        self.mode = kwargs.get('m') if kwargs.get('m') else "both"
        self.message = kwargs.get("M") if kwargs.get("M") else "Hello World!"

        self.client = None
        if self.useWebsocket:
            self.client = AWSIoTMQTTClient(self.clientId, useWebsocket=True)
            self.client.configureEndpoint(self.host, 443)
            self.client.configureCredentials(self.rootCAPath)
        else:
            self.client = AWSIoTMQTTClient(self.clientId)
            self.client.configureEndpoint(self.host, 8883)
            self.client.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

        self.client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec

        self.client.connect()
        if self.mode == 'both' or self.mode == 'subscribe':
            self.client.subscribe(self.topic, 1, customCallback)
        time.sleep(2)

    def unsubscribe(self):
        self.client.unsubscribe(self.topic)

    def publish(self, message):
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 1)

def customCallback(client, userdata, message):
    tp = str(message.topic)
    msg = str(message.payload)
    print(tp+":"+msg+'\n')

if __name__ == "__main__":
    h = helper(customCallback, e='data.iot.us-east-2.amazonaws.com', r='root-CA.crt', c='iot0.cert.pem', k='iot0.private.key')
    sMsg=''
    while sMsg != 'q':
        sMsg = input('send:')
        m = {}
        m['message'] = sMsg
        h.publish(m)
        sMsg = None