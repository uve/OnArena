from common import api
import logging

def widget(request, format='html'):

    #logging.info("request: %s",request)
    all_groups = api.group_browse(league_id = "1001")

    if format == 'html':
        return api.response_get(request, locals(), 'common/templates/widget.html')    
