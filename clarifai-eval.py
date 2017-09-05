# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 23:29:16 2017

@author: Frank

api-key "xxxxxxxxxxxxxxxx"
"""

import os
import sys
import platform
from pprint import pprint
from configparser import ConfigParser
from builtins import input
from subprocess import call

from clarifai.rest import ClarifaiApp

def setup(api_key):
  ''' write back CLARIFAI_API_KEY to config file
      config file is at ~/.clarifai/config
  '''

  os.environ['CLARIFAI_API_KEY'] = api_key

  homedir = os.environ['HOMEPATH'] if platform.system() == 'Windows' else os.environ['HOME']
  CONF_DIR=os.path.join(homedir, '.clarifai')
  CONF_DIR="C:" + CONF_DIR#frank-todo
  if not os.path.exists(CONF_DIR):
    os.mkdir(CONF_DIR)
  elif not os.path.isdir(CONF_DIR):
    raise Exception('%s should be a directory for configurations' % CONF_DIR)

  CONF_FILE=os.path.join(CONF_DIR, 'config')

  parser = ConfigParser()
  parser.optionxform = str

  if os.path.exists(CONF_FILE):
    parser.readfp(open(CONF_FILE, 'r'))

  if not parser.has_section('clarifai'):
    parser.add_section('clarifai')

  # remove CLARIFAI_APP_ID
  if parser.has_option('clarifai', 'CLARIFAI_APP_ID'):
    parser.remove_option('clarifai', 'CLARIFAI_APP_ID')

  # remove CLARIFAI_APP_SECRET
  if parser.has_option('clarifai', 'CLARIFAI_APP_SECRET'):
    parser.remove_option('clarifai', 'CLARIFAI_APP_SECRET')

  parser.set('clarifai', 'CLARIFAI_API_KEY', api_key)

  with open(CONF_FILE, 'w') as fdw:
    parser.write(fdw)
    
setup('xxxxxxxxxxxxxxxxxxxxxx')
app = ClarifaiApp()
model = app.models.get('general-v1.3')
response = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')

concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
    print(concept['name'], concept['value'])
