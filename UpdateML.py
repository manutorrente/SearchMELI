import gspread
import requests as rq
import json
import sys
from checkmercado import search_ml


#open google service account with gspread https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access
gc = gspread.service_account(filename="%service_account.json%")

#Get the item spreadsheet values on a list of lists
sh = gc.open("ItemsML")
w=sh.get_worksheet(0)
items=w.get_all_values()
items.pop(0)#delete the title row


for i in range(len(items)):
    
    l=search_ml(items[i][0])
    
     #checks if there are any forbidden or required words. In case there arent, sets the variables to unrecognizable random strings
    forbidden=items[i][3]
    if items[i][3]=="":
        forbidden="Requirement already satisfied: chardeyt<3.1.0,>=3.0.2 in "
    required=items[i][4]        
        
    for f in l:
    #check conditions
        title=f["title"].lower()
        if f["price"]<(float(items[i][2])+1):
            l.remove(f)
        elif f["price"]>(float(items[i][1])-1):
            l.remove(f)
        elif forbidden in title:
            l.remove(f)
        elif not required in title:
            l.remove(f)
    l=sorted(l, key=lambda x: x["price"])#sort the results by price        
    print("cheapest publications for {}:\ncurrent prices: {},{}\n".format(items[i][0],items[i][1], items[i][2]))        
    for h in range(5):
        #cheapest publications
        print("{}, price: {}".format(l[h]["title"],l[h]["price"] ))
    #options
    change=input("Change price? (y/n)\nto exit enter e: ")
    
    #update the changes
    if change=="y":
        min_p=int(input("New min price? "))
        floor_p=int(input("New floor price? "))
        w.update_cell(i+2, 2, min_p)
        w.update_cell(i+2, 3, floor_p)
    if change=="e":
        sys.exit()


