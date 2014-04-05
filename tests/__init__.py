import firstboot.serverconf
import firstboot
from firstboot.serverconf import *
import json

s = None
conf = None

fp = open('/home/damian/Proyectos/emergya/gecos/apps/gecosws-config-assistant/tests/autoconfig-gecos.json','r')
content = fp.read()
conf = json.loads(content)
s=ServerConf()
s.load_data(conf)
