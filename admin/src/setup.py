from distutils.core import setup
import py2exe
import os
import sys
import shutil

# Find GTK+ installation path
__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]

try:
	shutil.rmtree("dist")
except:
	pass

try:
	shutil.rmtree("build")
except:
	pass

shutil.copytree("..\data","dist\\data")
shutil.copytree("..\installer","dist\\installer")
shutil.copytree("..\locale","dist\\locale")

setup(
	name='skarphed-admin',
	description='Skarphed Administration Interface',
	version='0.1alpha',
	windows= [
	    {
	    	'script':'Application.py',
	    	'icon_resources':[(1,'skarphed.ico')]
	    }
	],
	options = {
		'py2exe': {
			'packages':'encodings',
			'includes': 'cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms'
		}
	},
	
)

