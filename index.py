import os
import traceback
import json
import requests

from flask import Flask, request

token = os.environ.get('FB_ACCESS_TOKEN')
api_key = os.environ.get('WEATHER_API_KEY')
app = Flask(__name__)


def location_quick_reply(sender, text=None):
    if not text:
        text = "Digite uma cidade ou aperte no botão abaixo para saber o clima. :)"
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": text,
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
                "payload": {
                    "url": url
                }
            }
        }
    }


def send_text(sender, text):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": text
        }
    }


def send_message(payload):
    requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)


def send_weather_info(sender, **kwargs):
    latitude = kwargs.pop('latitude', None)
    longitude = kwargs.pop('longitude', None)
    city_name = kwargs.pop('city_name', None)

    if latitude and longitude:
        query = 'lat={}&lon={}'.format(latitude, longitude)
    elif city_name:
        query = 'q={},br'.format(city_name.title())

    url = 'http://api.openweathermap.org/data/2.5/weather?' \
          '{}&appid={}&units={}&lang={}'.format(query,
                                                api_key,
                                                'metric',
                                                'pt')

    r = requests.get(url)
    response = r.json()

    if 'cod' in response:
        if response['cod'] == "502":
            return 'error'

    description = response['weather'][0]['description'].title()
    icon = response['weather'][0]['icon']
    weather = response['main']

    payload = send_attachment(sender,
                              'image',
                              'http://openweathermap.org/img/w/{}.png'.format(icon))
    send_message(payload)

    text_res = '{}\n' \
               'Temperatura: {}\n' \
               'Humidade: {}%'.format(description,
                                     weather['temp'],
                                     weather['humidity'])
    payload = {'recipient': {'id': sender}, 'message': {'text': text_res}}
    send_message(payload)

    return None


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            sender = data['entry'][0]['messaging'][0]['sender']['id']

            if 'message' in data['entry'][0]['messaging'][0]:
                message = data['entry'][0]['messaging'][0]['message']

            if 'postback' in data['entry'][0]['messaging'][0]:
                # Action when user first enters the chat
                payload = data['entry'][0]['messaging'][0]['postback']['payload']
                if payload == 'begin_button':
                    message = send_text(sender, 'Olá, tudo bem? Vamos começar?')
                    send_message(message)

                    payload = location_quick_reply(sender)
                    send_message(payload)

                    return 'Ok'

            if 'attachments' in message:
                if 'payload' in message['attachments'][0]:
                    if 'coordinates' in message['attachments'][0]['payload']:
                        location = message['attachments'][0]['payload']['coordinates']
                        latitude = location['lat']
                        longitude = location['long']

                        send_weather_info(sender, latitude=latitude, longitude=longitude)
                        
                        payload = location_quick_reply(sender)
                        send_message(payload)
            else:
                text = message['text']
                _return = send_weather_info(sender, city_name=text)

                if _return == 'error':
                    message = send_text(sender, 'Não encontrei a cidade... :( Quer tentar de novo?')
                    send_message(message)

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
