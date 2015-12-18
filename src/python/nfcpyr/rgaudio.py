
import os
import pygame

class RgAudio(object):
	
	def __init__(self):
			
			pygame.mixer.init()
			
	def playfile(self, filepath):
		if not os.path.exists(filepath):
			return False
		pygame.mixer.music.load(filepath)
		pygame.mixer.music.set_volume(1.0)
		pygame.mixer.music.play()
		return True
		
	