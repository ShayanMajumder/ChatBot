import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "hrep-numbers-rpyofk-4f6521157787.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "hrep-numbers-rpyofk"
import requests
import bs4

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(query,session_id):
    response = detect_intent_from_text(query,session_id)
    if response.fulfillment_text=='Mess Menu':
        res=requests.get('http://www.ssms-pilani.org/ssms/menu/')
        soup=bs4.BeautifulSoup(res.text,'lxml')
        x=soup.select('h1')
        y=soup.select('h3')
        z=soup.select('ul')
        k=x[0].getText()+'\n'+'\n'+y[0].getText()+'\n'+z[1].getText()+'\n'+y[1].getText()+'\n'+z[2].getText()+'\n'+y[2].getText()+'\n'+z[3].getText()
        return k
    elif response.fulfillment_text=='Weather':
        res=requests.get('https://www.worldweatheronline.com/lang/en-in/pilani-weather/rajasthan/in.aspx')
        soup=bs4.BeautifulSoup(res.text,'lxml')
        allo=soup.find_all('div',class_='col-sm-3')
        return allo[0].getText()
    else:
        return response.fulfillment_text
#hi