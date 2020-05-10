from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
import requests
import bs4
import json
app = Flask(__name__)

@app.route("/")
def hello():
    res=requests.get('https://nalanda.bits-pilani.ac.in/')#events
    soup=bs4.BeautifulSoup(res.text,'lxml')
    allo=soup.find_all('div',class_='event')
    k="UPCOMING EVENTS"

    for i in range(len(allo)):
        k=k+'\n'+allo[i].getText()

    res=requests.get('https://gadgets.ndtv.com/news')#technews
    soup=bs4.BeautifulSoup(res.text,'lxml')
    allo=soup.find_all('span',class_='news_listing')
    tnews="Latest technical NEWS"

    for i in range(len(allo)):
        tnews=tnews+'\n\n'+allo[i].getText()

    res=requests.get('https://www.dailymail.co.uk/news/headlines/index.html')#normal news
    soup=bs4.BeautifulSoup(res.text,'lxml')
    allo=soup.find_all('span',class_='headline')
    news="Latest NEWS"

    for i in range(10):
        news=news+'\n\n'+allo[i].getText()

    res=requests.get('https://www.worldometers.info/coronavirus/')
    soup=bs4.BeautifulSoup(res.text,'lxml')
    allo=soup.find_all('h1')
    p=soup.find_all('span')
    a='WORLD\n'+allo[0].getText()+p[4].getText()+'\n'+allo[1].getText()+p[5].getText()+'\n'
    res=requests.get('https://www.worldometers.info/coronavirus/country/india/')
    soup=bs4.BeautifulSoup(res.text,'lxml')
    allo=soup.find_all('h1')
    p=soup.find_all('span')
    b='INDIA\n'+allo[1].getText()+p[4].getText()+'\n'+allo[2].getText()+p[5].getText()

    return "Hello, Worldz!\n"+k+tnews+news+a+b
@app.route("/mess_menu", methods=['POST'])
def food():
    res=requests.get('http://www.ssms-pilani.org/ssms/menu/')
    soup=bs4.BeautifulSoup(res.text,'lxml')
    x=soup.select('h1')
    y=soup.select('h3')
    z=soup.select('ul')
    k=x[0].getText()+'\n'+'\n'+y[0].getText()+'\n'+z[1].getText()+'\n'+y[1].getText()+'\n'+z[2].getText()+'\n'+y[2].getText()+'\n'+z[3].getText()
    #response = requests.post('https://httpbin.org/post', json={"replies": [{"message": k}]})

    return {"fulfillmentMessages": [{"text": {"text": [k]}}]}#{"replies": [{"message": k}]}

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    phone_no=request.form.get('From')
    reply=fetch_reply(msg,phone_no)

    # Create reply
    resp = MessagingResponse()
    resp.message(reply)
    
    return str(resp)


@app.route('/webhook', methods=["POST"])
def webhook():
    data = request.get_json(silent=True)#FOR THE URL OF PLACES
    if data['queryResult']['parameters']['URL'] == 'events':
        res=requests.get('https://nalanda.bits-pilani.ac.in/')#events
        soup=bs4.BeautifulSoup(res.text,'lxml')
        allo=soup.find_all('div',class_='event')
        k="UPCOMING EVENTS"

        for i in range(len(allo)):
            k=k+'\n'+allo[i].getText()

        return {"fulfillmentMessages": [{"text": {"text": [k]}}]}

    elif data['queryResult']['parameters']['URL'] == 'tnews':
        res=requests.get('https://gadgets.ndtv.com/news')#technews
        soup=bs4.BeautifulSoup(res.text,'lxml')
        allo=soup.find_all('span',class_='news_listing')
        tnews="Latest technical NEWS"

        for i in range(len(allo)):
            tnews=tnews+'\n\n'+allo[i].getText()

        return {"fulfillmentMessages": [{"text": {"text": [tnews]}}]}
    elif data['queryResult']['parameters']['URL'] == 'news':
        res=requests.get('https://www.dailymail.co.uk/news/headlines/index.html')#normal news
        soup=bs4.BeautifulSoup(res.text,'lxml')
        allo=soup.find_all('span',class_='headline')
        news="Latest NEWS"

        for i in range(10):
            news=news+'\n\n'+allo[i].getText()


        return {"fulfillmentMessages": [{"text": {"text": [news]}}]}

    elif data['queryResult']['parameters']['URL'] == 'corona':
        res=requests.get('https://www.worldometers.info/coronavirus/')
        soup=bs4.BeautifulSoup(res.text,'lxml')
        allo=soup.find_all('h1')
        p=soup.find_all('span')
        a='WORLD\n'+allo[0].getText()+p[4].getText()+'\n'+allo[1].getText()+p[5].getText()+'\n'
        res=requests.get('https://www.worldometers.info/coronavirus/country/india/')
        soup=bs4.BeautifulSoup(res.text,'lxml')
        allo=soup.find_all('h1')
        p=soup.find_all('span')
        b='INDIA\n'+allo[1].getText()+p[4].getText()+'\n'+allo[2].getText()+p[5].getText()

        return {"fulfillmentMessages": [{"text": {"text": [a+b]}}]}
    elif data['queryResult']['parameters']['URL'] == 'weather':

        res=requests.get('https://www.worldweatheronline.com/lang/en-in/pilani-weather/rajasthan/in.aspx')
        soup=bs4.BeautifulSoup(res.text,'lxml')
        allo=soup.find_all('div',class_='col-sm-3')
        return {"fulfillmentMessages": [{"text": {"text": [allo[0].getText()]}}]}
    elif data['queryResult']['parameters']['URL'] == 'holiday':
        res=requests.get('https://nalanda.bits-pilani.ac.in/')#events
        soup=bs4.BeautifulSoup(res.text,'lxml')
        y=soup.find_all('td',class_='day hasevent calendar_event_global calendar_event_global')
        p="This month \n"
        for i in range(len(y)):
            A=y[i].find('a')['data-title'][:-6]
            x=y[i].find('a')['data-content']
            html = x
            soup = bs4.BeautifulSoup(html, "html.parser")
            B=soup.getText()
            if B[-3:]=='(H)':
                Z=A+'->'+B[:-3] 
                p=p+'\n'+Z
        return {"fulfillmentMessages": [{"text": {"text": [p]}}]}

if __name__ == "__main__":
    app.run(debug=True)