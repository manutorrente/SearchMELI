import gspread
import requests as rq
import json
import time
import smtplib as mail



def get_date():
    f = '%Y-%m-%d %H:%M'
    now = time.localtime()
    return time.strftime(f, now)

date=get_date()

def search_ml(search):
    busqueda=search.replace(" ", "%20")
    l=[]
    for b in range(4):
        r=rq.get("https://api.mercadolibre.com/sites/MLA/search?q={}&limit=50&offset=".format(busqueda)+str(b*50)).json()
        for a in r["results"]:
            l.append(a)
    return l

def send_mail(sender, password, to, subject, message):
    con=mail.SMTP("smtp.gmail.com", 587)
    con.ehlo()
    con.starttls()
    con.login(sender, password)
    con.sendmail(sender, to, "Subject: {}\n\n{}\n\n".format(subject, message))
    


#open google service account with gspread https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access
gc = gspread.service_account(filename="%service_account.json%")

#Get the item spreadsheet values on a list of lists
sh = gc.open("ItemsML")
w=sh.get_worksheet(0)
items=w.get_all_values()
items.pop(0)#delete the title row

#get the ids of the already found publications
sh1=gc.open("PublicacionesML")
w1=sh1.get_worksheet(0)
ids=w1.col_values(2)
ids.pop(0)

#search for the items in mercado libre
results=[]
for i in range(len(items)):
        
   l=search_ml(items[i][0])
        
        #sort by price
   d=sorted(l, key=lambda x: x["price"])#sort the results by price
   low_p=False
        
        #checks if there are any forbidden or required words. In case there arent, sets the variables to unrecognizable random strings
   forbidden=items[i][3]
   if items[i][3]=="":
       forbidden="Requirement already satisfied: chardet<3.1.0,>=3.0.2 in "
   required=items[i][4]

        #check conditions
   for f in d:
        title=f["title"].lower()
        if f["price"]<(float(items[i][2])+1):
            pass
        elif f["price"]>(float(items[i][1])-1):
            pass
        elif forbidden in title:
            pass
        elif not required in title:
            pass
        else:
            low_p=f
            break
            
             
   if low_p!=False and (low_p["id"] not in ids):        
        results.append(low_p)#list of publications with low prices
        #add to the publications spreadsheet
        w1.append_row([items[i][0], low_p["id"], low_p["title"], low_p["price"], low_p["permalink"], date])
       
   
    
if len(results)>0:
    r=["Found {} result/s: ".format(len(results))]        
    for i in results:
        rf="\n{} : {}$\n{}".format(i["title"], i["price"], i["permalink"])
        r.append(rf)
    
r="".join(r)
send_mail("%from%", "%password%", "%to%", "MercadoLibre publications found", r)
        

    






