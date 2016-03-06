import requests
import ast
import os
import configparser
import time

config = configparser.ConfigParser()
config.read('settings.ini')

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))

buffer_id = -1
def get_wall(modes):
   global buffer_id
   global config
   ID = buffer_id
   try:
       r = requests.get( config['_sysdat']['wall_get'].format( config['_def']['public_id'] ), timeout=10 )
       response = ast.literal_eval(r.text)
       ID = response['response']['items'][int(config['_def']['offset'])]['id']
   except:
       print('exception occured')
   if ID != buffer_id:
       buffer_id = ID
       modes[int(config['_def']['mode'])](ID)
  
def main(modes):
    global config
    while True:
      s = input().split(' ')
      if s[0] == 'start':
          break
      if s[0] == 'set':
          if s[1] in config['_def']:
              config['_def'][s[1]] = s[2]
              with open('settings.ini', 'w') as configfile:
                  config.write(configfile)
          else:
              print('Error: No such key in config file')

    global buffer_id
    r = requests.get( config['_sysdat']['wall_get'].format( config['_def']['public_id'] ), timeout=10 )
    response = ast.literal_eval(r.text)
    buffer_id = response['response']['items'][int(config['_def']['offset'])]['id']
    print(buffer_id)
    while True:
       with Profiler() as p:
           get_wall(modes)
       time.sleep(float(config['_def']['delay']))

  
def auto_mode(ID):
    global config
    p = requests.post( config['_sysdat']['wall_post'].format( config['_def']['public_id'], ID, config['_def']['text'], config['_sysdat']['token'] ) )
    print('\a')
    print('\n>>> Posted')
    time.sleep(10*60)
def hand_writing_mode(ID):
    global config
    print('\a')
    os.startfile(config['_sysdat']['link'].format(config['_def']['public_id'], ID))
    time.sleep(11)
    p = requests.post( config['_sysdat']['wall_post'].format( config['_def']['public_id'], ID, config['_def']['text_lentach'], config['_sysdat']['token'] ) )
    time.sleep(10*60)

modes = [auto_mode, hand_writing_mode]
print('>>> FACS Terminal @ US Chair Corps.')
main(modes)
