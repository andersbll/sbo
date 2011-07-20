# coding: utf-8
import sqlite3

class SBODict(object):
	def __init__(self, filename):
		self.con = sqlite3.connect(filename)
		self.cur = self.con.cursor()

	def create(self):
		self.con.executescript(cmd_create)
		self.__set_info('SBO Version', '1.0', None)

	def commit(self):
		self.con.commit()

	def compact(self):
		self.cur.execute('vacuum;')

	def close(self):
		self.cur.close()
		self.con.close()

	def __set_info(self, name, text, blob):
		self.cur.execute('insert into info values (?,?,?)', (name, text, blob))
	def __get_info(self, name):
		self.cur.execute('select value from info where name like \'%s\''%name)
		return self.cur.fetchone()[0]

	def set_dict_name(self, name):
		self.__set_info('Name', name, None)
	def dict_name(self):
		return self.__get_info('Name')

	def set_description(self, description):
		self.__set_info('Description', description, None)
	def description(self):
		return self.__get_info('Description')

	def set_icon(self, blob):
		self.__set_info('Icon', None, blob)
	def icon(self):
		return self.__get_info('Icon')

	def set_entries(self, entries):
		self.cur.executemany('insert into entry values (?,?,?,?)', entries)

	def set_lookup_types(self, lookup_types):
		self.cur.executemany('insert into lookup_type values (?,?,?,?,?)', lookup_types)

	def lookup_types(self):
		self.cur.execute('select * from lookup_type')

	def generate_lookups(self, all_lookups):
		# create temporary table containing all lookups
		self.cur.execute('drop table if exists all_lookups;')
		self.cur.execute('''
				create temp table all_lookups (
				    entry_id INTEGER,
				    word TEXT,
				    lookup_type_id INTEGER
				);''')
		self.cur.executemany('insert into all_lookups values (?,?,?)', all_lookups)

		# create lookup table containing distinct lookup words
		self.cur.execute('''
				insert into word (word) 
				    select distinct word
				    from all_lookups
				''')

		# generate all lookup-entry-lookup_type relations
		self.cur.execute('''
				insert into lookup (word_id, entry_id, lookup_type_id) 
				    select distinct word.id, all_lookups.entry_id, all_lookups.lookup_type_id
				    from all_lookups 
				        inner join word 
				        on all_lookups.word = word.word
				''')


	def search(self, searchstring, lookup_types = []):
		if len(lookup_types) == 0:
			query = '''
select entry.title 
from (
    select lookup.entry_id 
    from (
        select word.id 
        from word 
        where word.word like "afviklingen"
    ) as word 
        inner join (
            select * 
            from lookup
            where lookup_type_id = 0
        ) as lookup
            on word.id = lookup.word_id 
) as lookup
    inner join entry
        on lookup.entry_id = entry.id;
'''
		else:
			query = '''
select entry.title
from (
    select lookup.entry_id 
    from (
        select word.id 
        from word 
        where word.word like "afvikling"
    ) as word 
        inner join lookup
            on word.id = lookup.word_id 
) as lookup
    inner join entry
        on lookup.entry_id = entry.id;
'''
	def lookup(self, searchstring, lookup_types = []):
		return self.cur.execute('''
select entry.title,entry.summary,entry.text
from word,lookup,lookup_type,entry
where
    word.word like "%s"
    and lookup.word_id = word.id 
    and lookup.entry_id = entry.id
;
'''%searchstring).fetchall()


#SELECT entry.id,word.word,entry.title,entry.summary,entry.text
#FROM  word,lookup,lookup_type,entry
#WHERE  
#    lookup.word_id = word.id 
#AND lookup.entry_id = entry.id
#AND lookup.lookup_type_id = lookup_type.id
#AND lookup_type.id = 0 -- 'dansk engelsk'
#AND word.word like "afviklingen"; --TODO: undersøg om gyldendals får ordforbindelsen 'it hurts badly' ved søgning som her

cmd_create = """
-- Drop existing tables
 
DROP INDEX IF EXISTS entry_index;
DROP INDEX IF EXISTS word_index;
DROP TABLE IF EXISTS lookup;
DROP TABLE IF EXISTS entry;
DROP TABLE IF EXISTS lookup_index;
DROP TABLE IF EXISTS lookuptype_index;
DROP TABLE IF EXISTS word;
DROP TABLE IF EXISTS lookup_type;
DROP TABLE IF EXISTS info;


-- Create new ones

CREATE TABLE info (
    name TEXT PRIMARY KEY,
    value TEXT,
    value_blob BLOB
); 

CREATE TABLE lookup_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    primary_search INTEGER,
    parent INTEGER,
    display_order INTEGER,
    FOREIGN KEY(parent) REFERENCES lookup_type(id)
);

CREATE TABLE word (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT
);

CREATE TABLE entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    summary TEXT,
    text TEXT
);

CREATE TABLE lookup (
    word_id INTEGER,
    entry_id INTEGER,
    lookup_type_id INTEGER,
    PRIMARY KEY(word_id, entry_id, lookup_type_id),
    FOREIGN KEY(word_id) REFERENCES word(id),
    FOREIGN KEY(entry_id) REFERENCES entry(id),
    FOREIGN KEY(lookup_type_id) REFERENCES lookup_type(id)
);

CREATE INDEX entry_index ON entry (id);
CREATE INDEX word_index ON word (word);
CREATE INDEX lookup_index ON lookup (word_id, lookup_type_id);

"""

