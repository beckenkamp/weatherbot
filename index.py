import os
import traceback
import json
import requests

from flask import Flask, request

token = os.environ.get('FB_ACCESS_TOKEN')
api_key = os.environ.get('WEATHER_API_KEY')
app = Flask(__name__)

def location_quick_reply(sender):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": "De onde você quer saber o clima atual?",
            "quick_replies": [
                {
                    "content_type": "location",
                }
            ]
        }
    }

def send_attachment(sender, type, url):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "attachment": {
                "type": type,
                "payload":{
                    "url": url
                }
            }
        }
    }

def send_message(payload):
    requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            # print(data)
            message = data['entry'][0]['messaging'][0]['message']
            sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID

            if 'attachments' in message:
                if 'payload' in message['attachments'][0]:
                    if 'coordinates' in message['attachments'][0]['payload']:
                        location = message['attachments'][0]['payload']['coordinates']
                        latitude = location['lat']
                        longitude = location['long']

                        url = 'http://api.openweathermap.org/data/2.5/weather?' \
                              'lat={}&lon={}&appid={}&units={}&lang={}'.format(latitude,
                                                                               longitude,
                                                                               api_key,
                                                                               'metric',
                                                                               'pt')
                        r = requests.get(url)
                        description = r.json()['weather'][0]['description'].title()
                        icon = r.json()['weather'][0]['icon']
                        weather = r.json()['main']

                        payload = send_attachment(sender,
                                                  'image',
                                                  'http://openweathermap.org/img/w/{}.png'.format(icon))
                        send_message(payload)

                        text_res = '{}\n' \
                                   'Temperatura: {}\n' \
                                   'Pressão: {}\n' \
                                   'Humidade: {}\n' \
                                   'Máxima: {}\n' \
                                   'Mínima: {}'.format(description,
                                                       weather['temp'],
                                                       weather['pressure'],
                                                       weather['humidity'],
                                                       weather['temp_max'],
                                                       weather['temp_min'])
                        payload = {'recipient': {'id': sender}, 'message': {'text': text_res}}
                        send_message(payload)
                        
                        payload = location_quick_reply(sender)
                        send_message(payload)
            else:
                text = message['text']
                payload = location_quick_reply(sender)
                send_message(payload)
        except Exception as e:
            print(traceback.format_exc())
    elif request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"

if __name__ == '__main__':
    app.run(debug=True)
