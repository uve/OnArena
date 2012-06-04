# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.views.generic.base import TemplateView
    
class Index(TemplateView):

    template_name = 'common/templates/index.html'
    
   
    
    '''
    c = template.RequestContext(request, locals())
    #c.update(csrf(request))
    t = loader.get_template('templates/index.html')            
    result = http.HttpResponse(t.render(c))
    
    #result['Access-Control-Allow-Origin'] = 'http://goapi.cometiphrd.appspot.com/'
                   
    return result
    '''
