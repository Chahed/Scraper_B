from bs4 import BeautifulSoup
from urllib import urlopen
from splinter import Browser
import time
import random
import scraperwiki


def get_Id(url):
    d=url.split('=')
    return d[1]

def suittext(text):
    text=text.replace("   ","")
    a=text.split(" ")
    a=a[0]
    l=""
    for i in range(0,len(a)) :
        if a[i] in ['1','2','3','4','5','6','7','8','9','0','-']:
            l+=a[i]
    return l

def dateclean(date):
    date=suittext(date)
    a=date.split('-')
    return a[2]+'-'+a[1]+'-'+a[0]

def scrap(url):
    response = urlopen(url)
    htmltext = BeautifulSoup(response)

    id=get_Id(url)
    Title =htmltext.find('div',{"class":"mod page-title"}).findNext('h2').text

    Text= htmltext.find('div',{"class":"mod page-title"})
    Text= Text.findAll('p')
    Textfinal=""
    for i in range(0,len(Text)) :
        Textfinal= Textfinal + BeautifulSoup(str(Text[i])).text

    try:
        Deadline= htmltext.find('div', {"class":"tbHeader"}).findNext('h4').text
        Deadline_clean=dateclean(Deadline)
    except:
        Deadline=""
        Deadline_clean=""
    table= htmltext.findAll('td', {"class":"rightTd"})
    Udbudstype= table[0].text
    Opgavetype= table[1].text
    Tildelingskriterier= table[2].text
    Ordregiver= table[3].text
    Adresse= table[4].text
    CPV_kode= table[5].text
    Udbudsform =table[6].text
    try :
        SMV_venligt =table[7].text
        Kontaktperson =table[8].text
        Kontakt=table[9].text
    except :
        try:
            SMV_venligt=""
            Kontaktperson =table[7].text
            Kontakt=table[8].text
        except :
            SMV_venligt=""
            Kontaktperson =""
            Kontakt=""

    data={"ID":unicode(id), \
          "Url":unicode(url),\
          "Title":unicode(Title),\
          "Deadline":unicode(Deadline),\
          "Deadline clean":unicode(Deadline_clean),\
          "Udbudstype":unicode(Udbudstype),\
          "Opgavetype":unicode(Opgavetype),\
          "Tildelingskriterier":unicode(Tildelingskriterier),\
          "Ordregiver":unicode(Ordregiver),\
          "Adresse":unicode(Adresse),\
          "CPV kode":unicode(CPV_kode),\
          "Udbudsform":unicode(Udbudsform),\
          "SMV venligt":unicode(SMV_venligt),\
          "Kontaktperson":unicode(Kontaktperson),\
          "Kontakt":unicode(Kontakt)}
    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)




def redondance(l):
    a=False
    for i in range(0,len(l)-2):
        for j in range(i+1,len(l)-1):
            if l[i]==l[j] :
                a=True

    return a

def suppredon(l):
    l1=[]
    for el in l:
        if el in l1:
            pass
        else:
            l1.append(el)
    return l1

def Navigation(link):
    with Browser("phantomjs", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any']) as browser:
        browser.driver.set_window_size(1280, 1024)
        browser.visit(link)
        time.sleep(random.uniform(0.5,2.9))
        href=[]
        htmltext = BeautifulSoup(browser.html, "html.parser")
        soop = htmltext.find('table',{"id":"datagridtenders_1F8CBE3E"}).findNext('tbody')
        links = soop.findAll('a')
        for i in range(0,len(links)-1):
            if i%2==0:
                href.append("http://udbud.dk"+links[i].get('href'))
        button=1
        try:
            while(button):
                time.sleep(random.uniform(0.5,2.9))
                button = browser.find_by_id('datagridtenders_1F8CBE3E_next')
                button.click()
                htmltext = BeautifulSoup(browser.html, "html.parser")
                soop = htmltext.find('table',{"id":"datagridtenders_1F8CBE3E"}).findNext('tbody')
                links = soop.findAll('a')
                for i in range(0,len(links)-1):
                    if i%2==0:
                        href.append("http://udbud.dk"+links[i].get('href'))
                    if redondance(href) :
                        button=0

        except:
            pass

    return suppredon(href)

def main():
    urls = ['http://udbud.dk/Pages/Tenders/News']

    for link in urls:
        href=Navigation(link)
        for i in href:
            try:
                scrap(i)
            except :
                pass

if __name__ == '__main__':
    main()
