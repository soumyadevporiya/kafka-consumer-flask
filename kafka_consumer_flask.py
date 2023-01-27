import urllib.request
from flask import Flask
from flask import jsonify
import json
from kafka import KafkaConsumer

# Required for Kubernetes
import os
import pint
import kubernetes
from kubernetes import client, config, watch

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' %name

#Model
@app.route('/linearregression')
def model_serving():
    consumer = KafkaConsumer('my-topic', bootstrap_servers=['34.28.118.32:9094'], auto_offset_reset='latest')
    i=0
    dict = {}
    for message in consumer:
        message_1 = message.value
        #print byte-stream
        print(message_1)

        #print the json equivalent
        my_json = message_1.decode('utf8')
        #print(my_json)

        #extract values of individual fields; first convert json string into dictionary
        v1 = json.loads(my_json)["v1"]
        v2 = json.loads(my_json)["v2"]
        v3 = json.loads(my_json)["v3"]
        v4 = json.loads(my_json)["v4"]
        print(v1)
        print(v2)
        print(v3)
        print(v4)

        prediction = 0.3 + float(v1)*0.1 + float(v2)*0.2 + float(v3)*0.3 + float(v4)*0.4

        my_json_dict = json.loads(my_json)

        my_json_dict["prediction"] = prediction
        print(my_json_dict)

        # Updating Dictionary Values
        dict[str(i)]  = my_json_dict
        #dict.append(my_json_dict)

        i=i+1
        if i==10:
            break

    consumer.close()
    return dict
    #return 'hello'



# K8 Pod Details
@app.route('/hello/pods')
def get_pod_details():
    config.load_incluster_config()
    v1 = kubernetes.client.CoreV1Api()
    #ret = v1.list_node()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    #details = " " + ret
    details = " "
    for i in ret.items:
        details = details + " " + i.status.pod_ip+ " " + i.metadata.namespace + " " + i.metadata.name + "\n"

    return jsonify({"message":"POD Details ", "Information: ": details})


#Page 1
@app.route('/hello/gen_msg/1')
def generate_message_1():
    return jsonify({'message': "This is from Page 1"})

@app.route('/hello/get_msg/1')
def get_msg_1():
    content = urllib.request.urlopen('http://127.0.0.1:60/hello/gen_msg/1').read().decode('utf-8')
    return jsonify({'message': 'Delivered', 'Value': json.loads(content)['message'] })

#Page 2
@app.route('/hello/gen_msg/2')
def generate_message_2():
    return jsonify({'message': "This is from Page 2"})

@app.route('/hello/get_msg/2')
def get_msg_2():
    content = urllib.request.urlopen('http://127.0.0.1:60/hello/gen_msg/2').read().decode('utf-8')
    return jsonify({'message': 'Delivered', 'Value': json.loads(content)['message'] })


#Page 3
@app.route('/hello/gen_msg/3')
def generate_message_3():

    return jsonify({'message': "This is from Page 3"})

@app.route('/hello/get_msg/3')
def get_msg_3():
    content = urllib.request.urlopen('http://127.0.0.1:60/hello/gen_msg/3').read().decode('utf-8')
    return jsonify({'message': 'Delivered', 'Value': json.loads(content)['message'] })

#Page 4
@app.route('/hello/gen_msg/4')
def generate_message_4():
    return jsonify({'message': "This is from Page 4"})

@app.route('/hello/get_msg/4')
def get_msg_4():
    content = urllib.request.urlopen('http://127.0.0.1:60/hello/gen_msg/4').read().decode('utf-8')
    return jsonify({'message': 'Delivered', 'Value': json.loads(content)['message'] })

#Page 5
@app.route('/hello/gen_msg/5')
def generate_message_5():
    return jsonify({'message': "This is from Page 5"})

@app.route('/hello/get_msg/5')
def get_msg_5():
    content = urllib.request.urlopen('http://127.0.0.1:60/hello/gen_msg/5').read().decode('utf-8')
    return jsonify({'message': 'Delivered', 'Value': json.loads(content)['message'] })

#Page 6
@app.route('/hello/gen_msg/6')
def generate_message_6():
    return jsonify({'message': "This is from Page 6"})

@app.route('/hello/get_msg/6')
def get_msg_6():
    content = urllib.request.urlopen('http://127.0.0.1:60/hello/gen_msg/6').read().decode('utf-8')
    return jsonify({'message': 'Delivered', 'Value': json.loads(content)['message'] })

#Page 7
@app.route('/hello/gen_msg/7')
def generate_message_7():
    return jsonify({'message': "This is from Page 7"})

@app.route('/hello/get_msg/7')
def get_msg_7():
    content = urllib.request.urlopen('http://127.0.0.1:60/hello/gen_msg/7').read().decode('utf-8')
    return jsonify({'message': 'Delivered', 'Value': json.loads(content)['message'] })



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=60, threaded=True)
