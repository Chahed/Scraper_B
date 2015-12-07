from bs4 import BeautifulSoup
from urllib import urlopen
from splinter import Browser
import time
import random
import scraperwiki


def get_Id(url):
    d=url.split('=')
    return d[1]

def suittext2(text):
    text=text.replace("   ","")
    a=text.split(" ")
    a=a[0]
    l=""
    for i in range(0,len(a)) :
        if a[i] in ['1','2','3','4','5','6','7','8','9','0','-']:
            l+=a[i]
    return l

def dateclean(date):
    date=suittext2(date)
    a=date.split('-')
    return a[2]+'-'+a[1]+'-'+a[0]

def datecleannow(date):
    d=date.split('-')
    return d[2].strip()+'-'+d[1].strip()+'-'+d[0].strip()

def suittext(text):
    text=text.replace(", ,","")
    text=text.replace("'","")
    text=text.replace("  ","")
    text=text.replace("u\\n","")
    text=text.replace("\\r"," ")
    text=text.replace("\t","")
    return text

def scrap(url,m):
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
    table= htmltext.find('div',{"class":"tbContent"}).findAll('td', {"class":"rightTd"})
    table2=htmltext.find('div',{"class":"tbContent"}).findAll('td', {"class":"leftTd"})
    Udbudstype= table[0].text
    Opgavetype= table[1].text
    Tildelingskriterier= table[2].text
    a=suittext(BeautifulSoup(str(table2[3])).text)
    if "Ordregiver" in a:
        i=3
    else :
        i=4
    Ordregiver=table[i].text
    Adresse= table[i+1].text
    CPV_kode= table[i+2].text
    b=suittext(BeautifulSoup(str(table2[i+3])).text)
    j=i+3
    if "Udbudsform" in b :
        Udbudsform =table[j].text
        j+=1
    else:
        Udbudsform=""

    try:
            Kontaktperson =table[j].text
            Kontakt=table[j+1].text
    except :
            Kontaktperson =""
            Kontakt=""
    Annoceret=suittext(BeautifulSoup(str(m)).text)
    Annoceret_clean=datecleannow(Annoceret)
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
          "Annoceret":unicode(Annoceret),\
          "Annoceret_clean":unicode(Annoceret_clean),\
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

def lil(a,ch):
    j=0
    for i in ch :
        if i==a :
            j+=1
    return j


def Navigation(link):
    with Browser("phantomjs", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any']) as browser:
        browser.driver.set_window_size(1280, 1024)
        browser.visit(link)
        time.sleep(random.uniform(0.5,2.9))
        href=[]
        htmltext = BeautifulSoup(browser.html, "html.parser")
        soop = htmltext.find('table',{"id":"datagridtenders_1F8CBE3E"}).findNext('tbody')
        links = soop.findAll('a')
        Annonceret=htmltext.findAll('td',{"class":"center"})
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
                k=htmltext.findAll('td',{"class":"center"})
                for i in k :
                    Annonceret.append(i)
                for i in range(0,len(links)-1):
                    if i%2==0:
                        href.append("http://udbud.dk"+links[i].get('href'))
                    if redondance(href) :
                        button=0

        except:
            pass
    a=[]
    for i in Annonceret:
        if lil('-',str(i))==2 :
            a.append(i)

    return a,suppredon(href)

def main():
    urls = ['http://udbud.dk/Pages/Tenders/News']

    for link in urls:
        a,href=Navigation(link)
        j=-1
        for i in href:
            scrap(i,a[j])



if __name__ == '__main__':
    main()
