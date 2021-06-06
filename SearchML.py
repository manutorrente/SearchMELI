from MethodsML import get_date, send_mail, open_sheet
from ClassML import SearchML



json_key_file="%service_account.json%" #json key for google service account
num_pages=5 #number of pages of ML you want to go through. API might throw an error if you go high enough


items_ws=open_sheet("ItemsML", 0, json_key_file)
items=items_ws.get_all_values() #gets worksheet as a list of lists
items.pop(0) #removes the title row


results_ws=open_sheet("ResultsML", 0, json_key_file)
existent_ids=results_ws.col_values(2) #get the values of the existent publication ids to avoid repetition later on
existent_ids.pop(0)


searchML=SearchML(num_pages)
results_found=[]

for search in items:
    
    searchML.search_API(search)
    
    results=searchML.final_results
    
    for result in results:
        
        if result["id"] not in existent_ids:
            
            results_found.append(result)
        
            results_ws.append_row([search[0], result["id"], result["title"], result["price"], result["permalink"], get_date()])
            


#check if any new publications were found and send a mail
if len(results_found) > 0:

    message = f"Found {len(results_found)} result/s"
    
    for result in results:
        
        result_des = "\n{} a {}$\n{}".format(result["title"], result["price"], result["permalink"])
        message += result_des
        
    #send_mail("%from%", "%password%", "%to%", "MercadoLibre publications found", message)






        

    






