import os
import sys
import json
import requests
from flask import Flask, request
from wit import Wit

PAGE_ACCESS_TOKEN = "EAAUfMqxEKwABALsXnm62hzurf1tDQnc511RmXKgCRPdy7L03ZBEaU7myNnt0SQXy5qWt8zwLiQtHZAWE2f2XVkuUwhGHzDRELXXRTWZCKNxbFaWZAHSvmy0a9YdRobS8IQmZBWy5H4ZAKsROybpDqPO6IP6j0ID0yxTo6mdUO6HwZDZD"
CLIENT_ACCESS_TOKEN = "OCN2WF3JM4DC5ZBXHAGHNU2L2RGSZ7CW"

app = Flask(__name__) 

def send(request, response):
    print('Sending to user...', response['text'])
def my_action(request):
    print('Received from user...', request['text'])

actions = {
    'send': send,
    'my_action': my_action,
}

client = Wit(access_token=CLIENT_ACCESS_TOKEN, actions=actions)

@app.route('/', methods=['GET'])
def verify():

    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "test_token":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():

    # Recieve your package from facebook

    data = request.get_json()

    # print(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    print(sender_id)
                    print(message_text)

                    wit_bit(message_text, sender_id)

                    # responding to your user
                    #send_message(sender_id, message_text)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def send_message(recipient_id, message_text):

    # Prepare your package

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            # add the text you want to send here
            "text": message_text
        }
    })

    # Send the package to facebook with the help of a POST request
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    # do this to check for errors
    if r.status_code != 200:
        print("something went wrong")

def wit_bit(message_text, sender_id):
    resp = client.message(message_text)

    if(resp["entities"] != {}):
        if(resp["entities"]["intent"][0]["value"] == "greeting"):
            print("Hey! How can I help you?")
            send_message(sender_id, "Hey! How can I help you?")

        elif(resp["entities"]["intent"][0]["value"] == "tourInfo"):
        	print("Getting tour info...")
        	send_message(sender_id, "Getting tour info...")

        else:
            print("I'm to dumb to understand complex sentences.")
            send_message(sender_id, "I'm dumb sometimes. Maybe start by saying Hello?")
    else:
        print("I'm to dumb to understand complex sentences.")
        send_message(sender_id, "I'm dumb sometimes. Maybe start by saying Hello?")

if __name__ == '__main__':
	app.run(debug=True)