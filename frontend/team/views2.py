from django import http

from core.team import Team
                              


def team(request, item_id = None, format='json'):

    item = Team(item_id)
    
    if request.method == "GET":    #READ
        return item.get()


    if request.method == "POST":   #CREATE         
        return item.create(request)        
                                                         
    
    if request.method == "PUT":    #UPDATE           
        return item.update(request)
              
        
    if request.method == "DELETE": #DELETE   
        return item.delete()
    
    
    return http.HttpResponse(status = 404)
    
