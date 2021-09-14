from ClassML import SearchML
from MethodsML import open_sheet
import pandas as pd

json_key_file="%service_account.json%"
num_pages=5


items_ws=open_sheet("ItemsML", 0, json_key_file)
items=items_ws.get_all_values() #gets worksheet as a list of lists
items.pop(0) #removes the title row



#percentages are based on the lowest result found, NOT in the price previously set 
max_difference = 0.2
min_difference = 0.05
std_difference=0.1





searchML=SearchML(num_pages)
    
dataframe = pd.DataFrame(columns=["Item", "Old Price", "New Price", "Difference", "Lowest price", "2nd lowest", "3rd lowest", "link 1", "link 2", "link 3"])


reports = []

for search in items:
    
    try:
        set_price = int(search[1])
    except ValueError:
        set_price = 0
    
    search[1] = 0 #set price to 0 for the search not to be filtered by price
    
    searchML.search_API(search)
    
    results = searchML.final_results
    
    lowest_prices = []
    lowest_links = []
    
    new_value = "not changed"
    
    percentage = "no results"
    
    for i in range(3):    
        try:
            lowest_prices.append(results[i]["price"])
            lowest_links.append(results[i]["permalink"])
            
        except IndexError:
            lowest_prices.append("no results")
            lowest_links.append("no results")
    
     
    if lowest_prices[0] != "no results": 
    
        difference = abs(lowest_prices[0] - set_price)
    
        if difference > lowest_prices[0]*max_difference or difference < lowest_prices[0]*min_difference:
        
            new_value = int(lowest_prices[0]-(lowest_prices[0]*std_difference))#sets price lower than the lowest price found, depending on std_percentage
        
            items_ws.update("B"+str(items.index(search)+2), new_value)
        
        percentage = str(round(difference*100/results[0]["price"], 2))+"%"
        
    reports.append([search[0], set_price, new_value, percentage, lowest_prices[0], lowest_prices[1], lowest_prices[2], lowest_links[0], lowest_links[1], lowest_links[2]])
        
#unupdateds = sorted(unupdateds, key=lambda x: x[5], reverse=True) #order by percentage

reports = list(map(lambda x: pd.Series(x, index=dataframe.columns), reports))

dataframe = dataframe.append(reports, ignore_index=True)

try:
    dataframe.to_excel("unupdated.xlsx", index=False)
except PermissionError:
    print("Excel file is open. Unable to edit.")


