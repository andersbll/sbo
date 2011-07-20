#!/usr/bin/env python
# coding: utf-8

import os
import os.path
from gro import GRODict
from sbo import SBODict

GRO_path = 'data_gro'
SBO_path = 'data'

dictionaries = {
#	'en_vb': {
#		'name': 'Engelsk',
#		'iconfile': 'gb.png',
#		'gddfile': 'StorDanskEngelskDownload.gdd',
#		'datfile': 'StorDanskEngelskDownload.dat',
#		'sbofile': 'DanskEngelsk.sqlite',
#	},
#	'en_k-n': {
#		'name': 'Engelsk',
#		'iconfile': 'gb.png',
#		'gddfile': 'StorEngelskDanskDownload.gdd',
#		'datfile': 'StorEngelskDanskDownload.dat',
#		'sbofile': 'EngelskDansk.sqlite',
#	},
#	'en_fagordbog': {
#		'name': 'Engelsk',
#		'iconfile': 'gb.png',
#		'gddfile': 'FagordbogEngelskDownload.gdd',
#		'datfile': 'FagordbogEngelskDownload.dat',
#		'sbofile': 'EngelskDanskFagordbog.sqlite',
#	},
#	'en_cd': {
#		'name': 'Engelsk',
#		'iconfile': 'gb.png',
#		'gddfile': 'Engelsk.gdb',
#		'datfile': 'Engelsk.dat',
#		'sbofile': 'Engelsk.sqlite',
#	},
	'en': {
		'name': 'Engelsk',
		'iconfile': 'gb.png',
		'gddfile': 'EngelskOrdbog.gdd',
		'datfile': 'EngelskOrdbog.dat',
		'sbofile': 'Engelsk.sqlite',
	},
#	'de': {
#		'name': 'Tysk',
#		'iconfile': 'de.png',
#		'gddfile': 'TyskOrdbog.gdd',
#		'datfile': 'TyskOrdbog.dat',
#		'sbofile': 'Tysk.sqlite',
#	},
#	'de_cd': {
#		'name': 'Tysk',
#		'iconfile': 'de.png',
#		'gddfile': 'Tysk.gdb',
#		'datfile': 'Tysk.dat',
#		'sbofile': 'Tysk.sqlite',
#	},
#	'fr': {
#		'name': 'Fransk',
#		'iconfile': 'fr.png',
#		'gddfile': 'FranskOrdbog.gdd',
#		'datfile': 'FranskOrdbog.dat',
#		'sbofile': 'Fransk.sqlite',
#	},
#	'es': {
#		'name': 'Spansk',
#		'iconfile': 'es.png',
#		'gddfile': 'SpanskOrdbog.gdd',
#		'datfile': 'SpanskOrdbog.dat',
#		'sbofile': 'Spansk.sqlite',
#	},
#	'es_cd': {
#		'name': 'Spansk',
#		'iconfile': 'es.png',
#		'gddfile': 'Spansk.gdb',
#		'datfile': 'Spansk.dat',
#		'sbofile': 'Spansk.sqlite',
#	},
#	'no': {
#		'name': 'Norsk',
#		'iconfile': 'no.png',
#		'gddfile': 'NorskDownload.gdd',
#		'datfile': 'NorskDownload.dat',
#		'sbofile': 'Norsk.sqlite',
#	},
#	'se':  {
#		'name': 'Svensk',
#		'iconfile': 'se.png',
#		'gddfile': 'SvenskOrdbog.gdd',
#		'datfile': 'SvenskOrdbog.dat',
#		'sbofile': 'Svensk.sqlite',
#	},
#	'da':  {
#		'name': 'Dansk',
#		'iconfile': 'dk.png',
#		'gddfile': 'DanskDownload.gdd',
#		'datfile': 'DanskDownload.dat',
#		'sbofile': 'Dansk.sqlite',
#	},
}


if __name__ == '__main__':
	for dict_ in dictionaries.values():
		dict_['datfile'] = os.path.join(GRO_path, dict_['datfile'])
		dict_['gddfile'] = os.path.join(GRO_path, dict_['gddfile'])
		dict_['sbofile'] = os.path.join(SBO_path, dict_['sbofile'])
		dict_['iconfile'] = os.path.join('graphics','flags_iso','32', dict_['iconfile'])

		if not (os.path.exists(dict_['datfile']) \
				and os.path.exists(dict_['gddfile'])):
			print 'Skipping %s, %s.[gdd|dat] do not exist'%(dict_['name'],os.path.splitext(dict_['gddfile'])[0])
			continue

		if os.path.exists(dict_['sbofile']):
			os.remove(dict_['sbofile'])
#			print 'Skipping %s, %s already exists'%(dict_['name'],dict_['sbofile'])
#			continue


		gro = GRODict(dict_['name'], dict_['gddfile'], dict_['datfile'])
		sbo = SBODict(dict_['sbofile'])
		sbo.create()

		dict_name = gro.dict_name()
		print 'Dictionary:', dict_name
		sbo.set_dict_name(dict_name)

		sbo.set_description(gro.description())

		sbo.set_icon(buffer(open(dict_['iconfile'], 'rb').read()))

		print 'Generating entries'
		sbo.set_entries(gro.entries())

		print 'Generating lookup table'
		sbo.set_lookup_types(gro.lookup_types())
		sbo.generate_lookups(gro.all_lookups())

#		print 'Compacting database'
#		sbo.compact()

		print 'Done'
		sbo.commit()
		sbo.close()

