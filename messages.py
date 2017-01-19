import random


chat_responses = {}

chat_responses['not-a-city'] = [
    'Isso é uma cidade do Brasil? Não está na minha lista... :( Tente o botão abaixo para locais fora do país.',
    'Tem certeza de que isso é uma cidade? 8) Só reconheço cidades do Brasil.' \
    'No botão abaixo dá pra escolher no mapa locais fora do país.',
    'Não encontrei essa cidade... =( Eu só reconheço cidades do Brasil. ' \
    'Nesse botão aí embaixo você pode escolher lugares fora do país.',
    'Não achei essa cidade aí... foi mal... :( Só pra avisar, eu só reconheço nome de cidades do Brasil, ' \
    'Mas apertando no botão aí embaixo dá pra escolher qualquer lugar no mundo!',
]

chat_responses['error'] = [
    'Aconteceu um problema na hora de buscar as informações... =(',
    'Alguma coisa deu errado aqui... desculpe... :/',
]

chat_responses['no_answer'] = [
    'Não entendi alguma coisa... =(',
    'Desculpe, não entendi. 8)',
    'Não saquei... foi mal... ;(',
]

chat_responses['location-button'] = [
    'Digite uma cidade ou aperte no botão abaixo para saber o clima. :)',
    'Escreva o nome de uma cidade ou use o botão abaixo...',
]

chat_responses['greetings'] = [
    'Oi, tudo bem? Vamos ver como anda o clima por aí?',
    'Oie! Tá querendo saber o clima de onde?',
    'Olá! Quer saber a temperatura de algum lugar?',
    'Oi! Será que tá chovendo aí?',
    'Oi! Quer saber informações metereológicas de qual lugar?',
    'Oie! Será que chove ou faz sol lá fora?',
]

chat_responses['thanks'] = [
    'De nada! 8)',
    'Eu agradeço. <3',
    'Que isso? Só estou fazendo meu trabalho :)',
]

chat_responses['good-bye'] = [
    'Volte quando quiser! :D',
    'Tchau-tchau! 8)',
]


def get_message(response_type):
    """
    Return a random string message from a given type
    """
    if response_type in chat_responses:
        return random.choice(chat_responses[response_type])
    return random.choice(chat_responses['no_answer'])


chat_keywords = {}

chat_keywords['greetings'] = [
    'oi',
    'olá',
    'ola',
    'hello',
    'e ai',
    'hey',
    'hi',
    'bom dia',
    'boa tarde',
    'boa noite',
    'eae'
]

chat_keywords['good-bye'] = [
    'tchau',
    'até mais',
    'ate mais',
    'partiu',
    'fui',
    'bye',
    'bye bye',
    'bye-bye',
    'ate logo',
    'até logo',
]

chat_keywords['thanks'] = [
    'obrigado',
    'valeu',
    'thank',
]


def search_keyword(raw_text):
    """
    Search for a keyword on a text and returns the right message
    """
    for key, word_list in chat_keywords.items():
        for word in word_list:
            if word in raw_text.lower():
                return get_message(key)
    return None
