import requests as rq
import json



    
class SearchML():
    
    def __init__(self, num_pages):
        self.url="https://api.mercadolibre.com/sites/MLA/search?q={}&limit=50&sort=price_asc&condition={}&offset="
        self.num_pages=num_pages
        self.final_results=[]
    
        
    #builds API link in accordance to the parameters provided in a list
    #[search, lowest_price, floor_price, forbidden_words, required words, forbidden_ids, condition]
    def build_link(self, search_parameters):
        search=search_parameters[0].replace(" ", "%20")
        return self.url.format(search, search_parameters[6])
    
    
    
    #performs search in the API
    def perform_search(self, link):
        all_results=[]
        
        for pages in range(self.num_pages):
            results=rq.get(link + str(pages*50)).json()
            all_results += results["results"];
            
        return all_results    
    
    
    
    
    #remove the resutls that dont fulfill the requirements
    def filter_results(self, search_parameters, all_results):
        
        
        filtered_results=filter(lambda result: int(search_parameters[2]) < float(result["price"]), all_results)
        
        if search_parameters[1] != 0: #allows the UpdateML script to work without prices
            filtered_results=filter(lambda result: float(result["price"]) < float(search_parameters[1]) , filtered_results)
            
        for forbidden in search_parameters[3].split(" "): #supports multiple forbidden words separated by space
            filtered_results=list(filter(lambda result: forbidden not in result["title"].lower() or forbidden == "", filtered_results))

        for required in search_parameters[4].split(" "):
            filtered_results=list(filter(lambda result: required in result["title"].lower(), filtered_results))
            
        for forbidden_id in search_parameters[5].split(" "):
            filtered_results=list(filter(lambda result: forbidden_id != result["id"], filtered_results))
        
        return list(filtered_results)
        


    #gets the parameters and puts together the whole process
    def search_API(self, search_parameters):
        
        if search_parameters[1] == "": #give values if the cells are empty
            search_parameters[1] = 1
        
        if search_parameters[2] == "":
            search_parameters[2] = 0
        
        link=self.build_link(search_parameters)
        
        all_results=self.perform_search(link)
        
        filtered_results=self.filter_results(search_parameters, all_results)
        
        self.final_results = sorted(filtered_results, key=lambda result: result["price"])[0:7] #limits amount of results