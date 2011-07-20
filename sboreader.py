#!/usr/bin/env python2.6
# coding: utf-8

import os
import os.path
import sboreader_gui

from sbo import SBODict

SBO_path = 'data'
SBO_suffix = '.sqlite'

def main():

	dicts = []
	for d in os.listdir(SBO_path):
		if d.endswith(SBO_suffix):
			dicts.append( SBODict(os.path.join(SBO_path, d)) )
	dictionaryGUI = sboreader_gui.DictionaryGUI(dicts)
	dictionaryGUI.run()


if __name__ == '__main__':
	main()

