#!/usr/bin/env pybricks-micropython
from umqtt.robust import MQTTClient
from threading import Thread
from pybricks.tools import wait
import json

SERVER = "127.0.0.1"
ev3 = b"ev3"
state = b"state"
value = {}
pvalue = {}


def check_message(client):
    while True:           
        client.check_msg()
        wait(100)


def on_message(topic, msg):    
    global value
    try:
        new_str = msg.decode('utf-8')
        message = json.loads(new_str)
        print(message)

        if(message.get('state')):
            send_state()
        else:
            value = message
    except Exception as ex:
        print(ex)

def send_state():
    client = MQTTClient('state', SERVER)
    client.connect()
    client.set_callback(on_message)
    client.publish(state, '2')

def connect():
    global value
    global pvalue

    value = {}
    pvalue = {}

    client = MQTTClient('ev3', SERVER)
    client.connect()
    client.set_callback(on_message)
    client.subscribe(ev3)
    send_state()
    check_message_thread = Thread(target = check_message, args=(client,))
    check_message_thread.start()

def getdata(aiclass):
    global pvalue
    global value
    if len(pvalue) ==0:
        pvalue = value

    if len(pvalue) ==0:
        data = None
    else:
        data= pvalue.get(aiclass)
    
    if data == None:
        data = 0
    return data


def getdatas():
    global value
    data = value
    return data

def next():
    global pvalue
    pvalue ={}

def clear():
    global value
    value ={}
    next()
