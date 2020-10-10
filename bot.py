import requests
import logging
from bs4 import BeautifulSoup
import telegram
import pickle
import os
import sys

TOKEN="INSERT_YOUR_TELEGRAM_TOKEN_HERE"
CHANNEL_NAME = "@INSERT_CHANNEL_NAME_HERE"
URL_VALFURVA = "https://comune.valfurva.so.it/viabilita"
URL_BORMIO = "https://www.comune.bormio.so.it/viabilita"
URL_VALDIDENTRO = "https://www.comune.valdidentro.so.it/viabilita"
URL_VALDISOTTO = "https://www.comune.valdisotto.so.it/viabilita"
URL_LIVIGNO = "https://www.comune.livigno.so.it/viabilita"
URL_SONDALO = "https://www.comune.sondalo.so.it/viabilita"
URL_CMAV = "https://www.cmav.so.it/viabilita"

def fetch_news_generic(url, lista_notizie, bot):

  r = requests.get(url)
  logging.debug("[!] contenuto della richiesta GET: \n" + r.text)
  soup = BeautifulSoup(r.content, 'html.parser')

  notizie = soup.find_all('li')
  
  for n in notizie:
     titolo = n.find('h2', class_='Accordion-header js-fr-accordion__header fr-accordion__header')
     descrizione = n.find('div', class_='Accordion-panel fr-accordion__panel js-fr-accordion__panel')
     
     #check if not null
     if(titolo != None):
      
      logging.debug("LISTA NOTIZIE PARSATA: \n" + "Titolo: " + titolo.text + "\nDescrizione: " + descrizione.text)
      
      #TODO usare hash di titolo+descrizione per verificare se notizia già trovata, per risparmiare spazio in memoria
      if (titolo.text+descrizione.text not in lista_notizie):
         
         lista_notizie.append(titolo.text + descrizione.text)
            
         #inoltra la notizia al bot
         bot.sendMessage(chat_id=CHANNEL_NAME, text=lista_notizie[-1])
         logging.debug("Inoltro al bot la notizia: \n" + lista_notizie[-1])

def main():
 
  bot = telegram.Bot(token = TOKEN)
  lista_notizie = [] 
  
  try:
      with open (os.path.join(sys.path[0], "lista_notizie.txt"), "rb") as fp:
        lista_notizie = pickle.load(fp)
  except FileNotFoundError:
      with open (os.path.join(sys.path[0], "lista_notizie.txt"), "wb") as fp:
        pickle.dump(lista_notizie, fp)

  #fetch news from URLS
  fetch_news_generic(URL_VALFURVA, lista_notizie, bot)
  fetch_news_generic(URL_BORMIO, lista_notizie, bot)
  fetch_news_generic(URL_VALDISOTTO, lista_notizie, bot)
  fetch_news_generic(URL_VALDIDENTRO, lista_notizie, bot)
  fetch_news_generic(URL_LIVIGNO, lista_notizie, bot)
  fetch_news_generic(URL_SONDALO, lista_notizie, bot)
  fetch_news_generic(URL_CMAV, lista_notizie, bot)
  
  #write changes to file 
  with open (os.path.join(sys.path[0], "lista_notizie.txt"), "wb") as fp:
   pickle.dump(lista_notizie, fp)
      



if __name__=='__main__':
   main()
