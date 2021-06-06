import requests as rq
import json



    
class SearchML():
    
    def __init__(self, num_pages):
        self.url="https://api.mercadolibre.com/sites/MLA/search?q={}&limit=50&sort=price_asc&condition={}&offset="
        self.num_pages=num_pages
        self.final_results=[]
    
        
    #builds API link in accordance to the parameters provided in a list
    #[search, lowest_price, floor_price, forbidden_words, required words, condition]
    def build_link(self, search_parameters):
        search=search_parameters[0].replace(" ", "%20")
        return self.url.format(search, search_parameters[5])
    
    
    
    #performs search in the API
    def perform_search(self, link):
        all_results=[]
        
        for pages in range(self.num_pages):
            results=rq.get(link + str(pages*50)).json()
            all_results += results["results"];
            
        return all_results    
    
    
    
    
    
    
    #remove the resutls that dont fulfill the requirements
    def filter_results(self, search_parameters, all_results):
        
        filtered_results=filter(lambda result: float(result["price"]) < float(search_parameters[1]) , all_results)
        
        filtered_results=filter(lambda result: int(search_parameters[2]) < float(result["price"]), filtered_results)
        
        filtered_results=filter(lambda result: search_parameters[3] not in result["title"].lower() or search_parameters[3] == "", filtered_results)

        filtered_results=filter(lambda result: search_parameters[4] in result["title"].lower(), filtered_results)
        
        return list(filtered_results)
        


    
    def search_API(self, search_parameters):
        link=self.build_link(search_parameters)
        
        all_results=self.perform_search(link)
        
        filtered_results=self.filter_results(search_parameters, all_results)
        
        self.final_results = sorted(filtered_results, key=lambda result: result["price"])[0:5] #limits amount of results



        