import yaml
from os.path import join
from os.path import realpath
from os.path import dirname
import os

dir_path = dirname(realpath(__file__))
filepath = join(dir_path,"config.yml")
print("path to config.yml:", filepath)
with open(filepath) as f:
    config = yaml.load(f.read())
