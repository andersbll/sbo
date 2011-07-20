# coding: utf-8

import sqlite3
import groparser
import sys

class GRODict(object):
	def __init__(self, name, gdd_path, dat_path):
		self.name = name
		self.dat = open(dat_path, 'rb')
		self.con = sqlite3.connect(gdd_path)
		self.cur = self.con.cursor()

		self.cur.execute('select count(*) from dict_setup')
		if self.cur.fetchone()[0] == 2:
			self.two_way = True
		else:
			self.two_way = False

		self.db_version = self.__get_info('Database version')

	def get_entry(self, entry_id, offset, nbyte):
		raw_entry = groparser.get_raw_entry(self.dat, self.db_version, entry_id, offset, nbyte)
		raw_entry = raw_entry[8:] # remove garbage
		raw_entry = unicode(raw_entry, 'utf_8')
		raw_entry = raw_entry.split('\0')
		title = raw_entry[0] + ' ' + raw_entry[1]
		summary = raw_entry[2] + ' ' + raw_entry[3]
		content = raw_entry[4]
		r = (title, summary, content)
		return r
#		print 'title', title
#		print '0', raw_entry[0]
#		print '1', raw_entry[1]
#		print '2', raw_entry[2]
#		print '3', raw_entry[3]
#		print '4', raw_entry[4]
#		print '5', raw_entry[5]

	def __get_info(self, name):
		self.cur.execute('select value from info where name like \'%s\''%name)
		return self.cur.fetchone()[0]

	def dict_name(self):
		return self.__get_info('Publication name')

	def description(self):
		return self.__get_info('About')

	def entries(self):
		if self.two_way:
			tables = ['entries1', 'entries2']
		else:
			tables = ['entries1']
		l = []
		self.id_offset = [0]
		for t in tables:
			if self.db_version == '1':
#				self.cur.execute('select id, offset, count from %s where 0 <= type and type <= 1'%t)
				self.cur.execute('select id, offset, count from %s'%t)
			elif self.db_version == '2':
#				self.cur.execute('select id_, offset_, count_ from %s where 0 <= type_ and type_ <= 1'%t)
				self.cur.execute('select id_, offset_, count_ from %s'%t)
			for row in self.cur:
				e = self.get_entry(*row)
				l_ = (row[0]+self.id_offset[-1], e[0], e[1], e[2])
				l.append(l_)
			if self.db_version == '1':
#				self.cur.execute('select max(id) from %s where 0 <= type and type <= 1'%t)
				self.cur.execute('select max(id) from %s'%t)
			elif self.db_version == '2':
#				self.cur.execute('select max(id_) from %s where 0 <= type_ and type_ <= 1'%t)
				self.cur.execute('select max(id_) from %s'%t)
			self.id_offset.append(self.cur.fetchone()[0]);
		return l

	def lookup_types(self):
		if self.two_way:
			return [
						(0, 'Dansk-%s'%self.name, True, None, 0)
					, (1, 'Ordforbindelser', False, 0, 1)
					, (2, u'Modsat søgning', False, 0, 2)
					, (3, '%s-Dansk'%self.name, True, None, 3)
					, (4, 'Ordforbindelser', False, 3, 4)
					, (5, u'Modsat søgning', False, 3, 5)
					]
		else:
			return [
						(0, 'Dansk-%s'%self.name, True, None, 0)
					, (1, 'Ordforbindelser', False, 0, 1)
					]

	def all_lookups(self):
		#TODO: maaske kan der fjernes lookups, som peger på nogle underlige entries??
		result = []
		if self.two_way:
			lookup_types = [
						(0, False, 'lookup1')
					, (1, False, 'collocation_lookup1')
					, (2, True, 'reverse2')
					, (3, True, 'lookup2')
					, (4, True, 'collocation_lookup2')
					, (5, False, 'reverse1')
					]
		else:
			lookup_types = [
						(0, False, 'lookup1')
					, (1, False, 'collocation_lookup1')
					]

		for type_, offset, table in lookup_types:
			if self.db_version == '1':
				self.cur.execute('select entry_id, word, cast(%i as int) from %s'%(type_,table))
			if self.db_version == '2':
				self.cur.execute('select entry_id_, word_, cast(%i as int) from %s'%(type_,table))
#				self.cur.execute('select %s.entry_id_, %s.word_, cast(%i as int) from %s,%s where %s.type_<2 and %s.entry_id_ = %s.id_'%(table,table,type_,table,'entries1','entries1',table,'entries1'))
			lookups = self.cur.fetchall()
			if offset:
				# english entry ids must be incremented by offset to avoid 
				# clashes with danish entry ids
				lookups = map(lambda x: (x[0]+self.id_offset[1],x[1],x[2]), lookups)
			result.extend(lookups)
		return result

