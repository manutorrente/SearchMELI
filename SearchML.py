import json
from MethodsML import *

date=get_date()
json_file="%service_account.json%"
num_paginas=4

#open google service account with gspread 
#Get the item spreadsheet values on a list of lists
w=open_sheet("ItemsML", 0, json_file)
items=w.get_all_values()
items.pop(0)#delete the title row

#get the ids of the already found publications
w1=open_sheet("PublicacionesML", 0, json_file)
ids=w1.col_values(2)
ids.pop(0)

 #Sets the number of pages the scripts searches (max 20)


#search for the items in mercado libre
results=[]
for i in range(len(items)):
        
   search_raw=search_ml(items[i][0], num_paginas)
        
        #sort by price
   search_sorted=sorted(search_raw, key=lambda x: x["price"])#sort the results by price
   low_p=False
        
        #checks if there are any forbidden or required words. In case there arent, sets the variables to unrecognizable random strings
   forbidden=items[i][3]
   if items[i][3]=="":
       forbidden="{}"
   required=items[i][4]

        #check conditions
   for publication in search_sorted:
        title=publication["title"].lower()
        if publication["price"]<(float(items[i][2])+1):
            pass
        elif publication["price"]>(float(items[i][1])-1):
            pass
        elif forbidden in title:
            pass
        elif not required in title:
            pass
        else:
            low_p=publication
            break
            
             
   if low_p!=False and (low_p["id"] not in ids):        
        results.append(low_p)#list of publications with low prices
        #add to the publications spreadsheet
        w1.append_row([items[i][0], low_p["id"], low_p["title"], low_p["price"], low_p["permalink"], date])
       
   
    
if len(results)>0:
    results_str=[f"Found {len(results)} result/s: "]        
    for i in results:
        rf=f"\n{i['title']} : {i['price']}$\n{i['permalink']}"
        results_str.append(rf)
    results_str="".join(results_str)
    send_mail("%from%", "%password%", "%to%", "MercadoLibre publications found", results_str)
        

    






