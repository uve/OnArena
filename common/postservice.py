import datetime

from protorpc import message_types
from protorpc import remote
from protorpc import messages
#from common import models

import logging

class Note(messages.Message):

  text = messages.StringField(1, required=False)
  when = messages.IntegerField(2)

class PostService(remote.Service):

  @remote.method(Note, message_types.VoidMessage)
  def post_note(self, request):
  
    logging.info("Hello: %s",request.text)
    #if request.when:
    #  when = datetime.datetime.utcfromtimestamp(request.when)
    #else:
    #  when = datetime.datetime.now()
    #note = guestbook.Greeting(content=request.text, date=when)
    #note.put()
    
    return message_types.VoidMessage()
