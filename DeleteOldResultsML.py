# from ClassML import SearchML
import requests as rq
from MethodsML import open_sheet

url="https://api.mercadolibre.com/items/"
json_key_file="%service_account.json%" #json key for google service account


results_ws=open_sheet("ResultsML", 0, json_key_file)


existent_ids=results_ws.col_values(2) #get the values of the existent publication ids to avoid repetition later on
existent_ids.pop(0)


for Id in range(len(existent_ids)):
    
    publication = rq.get(url + existent_ids[Id]).json()
    
    if publication["status"] != "active":
        
        results_ws.delete_row(Id+2)





    


