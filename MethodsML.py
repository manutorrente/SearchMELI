import gspread
import requests as rq
import json
import time
import smtplib as mail



def get_date():
    f = '%Y-%m-%d %H:%M'
    now = time.localtime()
    return time.strftime(f, now)



def search_ml(search, num_paginas):
    busqueda=search.replace(" ", "%20")
    l=[]
    url="https://api.mercadolibre.com/sites/MLA/search?q={}&limit=50&offset=".format(busqueda)
    for b in range(num_paginas):
        r=rq.get(url+str(b*50)).json()
        for a in r["results"]:
            l.append(a)
    return l

def send_mail(sender, password, to, subject, message):
    con=mail.SMTP("smtp.gmail.com", 587)
    con.ehlo()
    con.starttls()
    con.login(sender, password)
    con.sendmail(sender, to, f"Subject: {subject}\n\n{message}\n\n")
    
    
def open_sheet(file, worksheet, json_file):
    gc = gspread.service_account(filename=json_file)
    sheet=gc.open(file)
    worksheet=sheet.get_worksheet(worksheet)
    return worksheet
