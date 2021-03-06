#!/usr/bin/env python
# coding: utf-8

from array import array
import re

KEY_1 = [
	0x17, 0xB4, 0x03, 0xB1, 0x26, 0x9F, 0xE0, 0x6B, 0x85, 0x1C, 0xB2,
	0xF0, 0xB1, 0x7B, 0x5C, 0xC1, 0x57, 0xE1, 0xC1, 0xB5, 0x82, 0xE9,
	0x2D, 0x87, 0xBF, 0xA9, 0xE9, 0x10, 0x44, 0x92, 0xF3, 0xD1, 0x1A,
	0x55, 0x39, 0x94, 0xB0, 0x54, 0x1F, 0xB3, 0x20, 0x7F, 0x77, 0x86,
	0x2F, 0xB4, 0xDE, 0x27, 0xB2, 0x8E, 0xB1, 0xBF, 0x32, 0xA0, 0xAF,
	0x2F, 0x5F, 0x65, 0xCD, 0x22, 0x60, 0x32, 0x05, 0x43, 0xA3, 0x4E,
	0x88, 0x5E, 0x0C, 0x79, 0x52, 0xE2, 0x91, 0xEB, 0x96, 0xD4, 0x2E,
	0x4A, 0xC5, 0x24, 0x18, 0x2A, 0xAD, 0x5B, 0x33, 0xF2, 0x4A, 0xED,
	0xA4, 0xD0, 0xBC, 0xD4, 0xAB, 0x2A, 0x8E, 0x72, 0x49, 0x11, 0xF6,
	0x5C, 0x9D, 0x30, 0x67, 0xA3, 0xBF, 0xDD, 0x34, 0x56, 0xF1, 0xE7,
	0x7D, 0x30, 0x0A, 0xCC, 0xD6, 0x5F, 0xE9, 0xF0, 0x07, 0xB7, 0x51,
	0x7B, 0x87, 0xA6, 0xFC, 0x56, 0x3A, 0xFA, 0xE0, 0x03, 0x1E, 0x2E,
	0xEB, 0xEC, 0x46, 0xD7, 0xDC, 0x85, 0x87, 0xF0, 0xFB, 0xCA, 0xDA,
	0x10, 0x54, 0x59, 0xBC, 0xD5, 0x8B, 0x52, 0xC1, 0x04, 0xCF, 0x2D,
	0xB2, 0x1D, 0x35, 0x21, 0x96, 0xA7, 0x6E, 0x98, 0xC2, 0xCD, 0xBC,
	0xC7, 0x56, 0x54, 0xEA, 0xF5, 0x24, 0x73, 0xCD, 0xAE, 0x8A, 0x4A,
	0x86, 0x09, 0x04, 0x95, 0x81, 0xB1, 0xAF, 0xF0, 0x17, 0x01, 0x25,
	0xF2, 0x1C, 0xE1, 0xD5, 0x4E, 0xD8, 0x65, 0x2F, 0xD7, 0x47, 0xC1,
	0xAA, 0x88, 0xA2, 0x57, 0xB1, 0x93, 0x65, 0xBD, 0xCB, 0x8A, 0x80,
	0x11, 0x24, 0x64, 0x0A, 0xF2, 0xC6, 0x79, 0x3E, 0xCB, 0x87, 0xE9,
	0x17, 0x82, 0x12, 0xEA, 0xDF, 0x7F, 0xEA, 0xA2, 0xFC, 0x7B, 0x41,
	0x72, 0x46, 0xA3, 0x92, 0xC4, 0xE9, 0x15, 0xDA, 0x88, 0x7A, 0xE9,
	0xA2, 0x24, 0xBF, 0x68, 0x7F, 0x50, 0x24, 0x3F, 0xD0, 0xD4, 0x6F,
	0x08, 0x8C, 0x65, 0xDB, 0xC8, 0x2A, 0xA1, 0x59, 0xD9, 0xEB, 0x71,
	0xCF, 0x4F, 0xF6, 0x7C, 0x11, 0x5D, 0x9F, 0xE3, 0x13, 0xB6, 0x6E,
	0x80, 0x6A, 0x1C, 0x76, 0xCB, 0xC8, 0x54, 0x7C, 0x3B, 0x74, 0x57,
	0x66, 0xA4, 0xC1, 0x9B, 0x9F, 0x8B, 0x61, 0x1B, 0x48, 0x72, 0x07,
	0x89, 0xD6, 0x68, 0xBA, 0xF0, 0x19, 0x73, 0xE9, 0x56, 0xB8, 0xB1,
	0xAB, 0xD4, 0x69, 0x6A, 0xC4, 0x6A, 0xF5, 0x2F, 0x2C, 0xDA, 0x5B,
	0x47, 0xE4, 0x50, 0x0E, 0xC8, 0x1B, 0xE3, 0x60, 0xED, 0x07, 0x6E,
	0x67, 0xFC, 0x3B, 0x12, 0x03, 0x9C, 0x31, 0x8A, 0xE1, 0xBD, 
]

KEY_2 = [
	0xBA, 0x59, 0xD9, 0xC2, 0x32, 0xB7, 0x21, 0x78, 0xB5, 0x86, 0x0C, 
	0x8C, 0xA7, 0x3E, 0xA5, 0x12, 0xA2, 0xA4, 0x4B, 0x95, 0xE0, 0x31,
	0xBD, 0x9E, 0x4D, 0x86, 0x45, 0xCE, 0x17, 0xD5, 0x5D, 0x7D, 0x08,
	0xC0, 0x52, 0x40, 0xA3, 0x6E, 0x86, 0x1B, 0xD4, 0xAC, 0xBA, 0xC4,
	0x5B, 0x2B, 0xC4, 0xE1, 0x84, 0x12, 0x19, 0x91, 0x88, 0xB1, 0xEC,
	0x5A, 0x52, 0x61, 0x39, 0x25, 0xA8, 0x98, 0x07, 0x26, 0x35, 0x64,
	0x5D, 0xA4, 0x98, 0x32, 0xDB, 0x57, 0x57, 0x5A, 0xCC, 0xDD, 0x2A,
	0x67, 0xE0, 0x11, 0x65, 0xC9, 0x61, 0x47, 0x62, 0x79, 0x60, 0x6E,
	0x22, 0x27, 0x17, 0x86, 0x67, 0x29, 0x72, 0x59, 0x72, 0xB8, 0xDB,
	0x14, 0x2D, 0x3A, 0x53, 0x72, 0x36, 0x4C, 0xC8, 0xED, 0xC6, 0x2E,
	0xEA, 0xE4, 0xBD, 0x23, 0x3D, 0x16, 0x0D, 0x53, 0x3C, 0x13, 0xE0,
	0x50, 0xC7, 0xBD, 0x3C, 0xB7, 0x92, 0x57, 0xEE, 0xD6, 0x14, 0xD5,
	0x5D, 0xBE, 0x3B, 0x9E, 0x4D, 0xEE, 0x4D, 0x63, 0x13, 0x05, 0x29,
	0xCD, 0x7D, 0x34, 0xD9, 0x2A, 0x10, 0xAE, 0xBB, 0xA7, 0x3B, 0x2A, 
	0x26, 0x20, 0x79, 0x4C, 0x47, 0x2B, 0x0C, 0x65, 0x75, 0x09, 0xB4,
	0xC3, 0x36, 0x75, 0x87, 0x25, 0x61, 0xA1, 0xA3, 0xB4, 0x44, 0x68,
	0xDE, 0xDD, 0x45, 0x0C, 0xB8, 0xED, 0x8E, 0xC1, 0x2E, 0x4B, 0x5C,
	0x4E, 0x15, 0x93, 0x8B, 0x46, 0xC3, 0x53, 0x79, 0x02, 0x74, 0x8D,
	0x2C, 0x7B, 0x6A, 0x25, 0x09, 0x31, 0x9E, 0xBE, 0xAB, 0x40, 0x38,
	0x04, 0x98, 0x87, 0xD1, 0x40, 0x36, 0xC4, 0xDD, 0xCC, 0x9E, 0x53,
	0x03, 0x98, 0xC1, 0x7A, 0xE8, 0x98, 0xB2, 0x1C, 0x29, 0x6D, 0x53,
	0xC2, 0x26, 0x1B, 0xE7, 0x64, 0x2C, 0x45, 0xEE, 0xAC, 0x98, 0x0A,
	0xB3, 0x8A, 0xBE, 0xA0, 0x77, 0xDB, 0x66, 0x65, 0x0A, 0xB7, 0x25,
	0x6E, 0xCB, 0xD2, 0xD8, 0x4B, 0x32, 0x6D, 0xD5, 0xE0, 0xB6, 0xBA,
	0xE7, 0xE8, 0x84, 0xCE, 0xC7, 0x76, 0xC9, 0xC0, 0x07, 0x1D, 0x21,
	0x83, 0x07, 0x69, 0xAA, 0xBA, 0x9A, 0xE4, 0xC5, 0x99, 0xB4, 0xEA,
	0x90, 0x14, 0x7E, 0xE3, 0x5C, 0x7D, 0xEA, 0x70, 0xC2, 0x41, 0xBB,
	0xB1, 0x97, 0x39, 0xD6, 0x2C, 0x1D, 0x80, 0x62, 0x1A, 0xA7, 0x5C,
	0x31, 0x51, 0xC9, 0xB8, 0x0D, 0xEC, 0x30, 0xA0, 0xA5, 0x5D, 0x99,
	0xB1, 0x17, 0x9A, 0x08, 0x53, 0x6E, 0xC8, 0x21, 0xB4, 0xA8, 0xC2,
	0xDA, 0xB5, 0x71, 0xE5, 0x27, 0x28, 0x44, 0xE4, 0x01, 0x87, 0x7A,
	0x63, 0x22, 0xC9, 0x81, 0x31, 0xC8, 0x26, 0xB3, 0x3E, 0x8E, 0x1D,
	0xC4, 0x3C, 0x27, 0x38, 0x04, 0x92, 0x37, 0x35, 0x35, 0xC0, 0x31,
	0xAA, 0x18, 0x8B, 0xC9, 0xE8, 0x98, 0x6D, 0xD0, 0x71, 0xC9, 0x08,
	0xDE, 0x23, 0x0D, 0xA2, 0x20, 0x9A, 0x87, 0xA8, 0xD6, 0xB6, 0x51,
	0x8A, 0x05, 0x63, 0xDB, 0x39, 0x02, 0xB2, 0x64, 0xBE, 0xDB, 0x58,
	0xDA, 0x46, 0x4D, 0x25, 0xD9, 0x3C, 0x66, 0x29, 0x66, 0x36, 0xC0,
	0xA5, 0xA8, 0x28, 0xAB, 0x78, 0xA0, 0xC5,
]

#3 * x + 51944
#	* 1103
#	% 0x19E

#3 * x + 89432
#	* 1097
#	% 0x154

#x + 94376
#	* 1103
#	% 0x19E

#+ 69247
#	* 1097
#	% 0x154

#+ 0x10E7F
#* 1097
#% 340 = 0x154

def get_raw_entry(dat_file, dat_version, entry_id, offset, nbyte):
	data = extract_from_dat(dat_file, offset, nbyte)
	return parse_entry(data, dat_version, entry_id, offset, nbyte)

def extract_from_dat(dat_file, offset, nbyte):
	dat_file.seek(offset)
	data = array('B')
	data.fromfile(dat_file, nbyte)
	return data

def parse_entry(entry_data, dat_version, entry_id, offset, nbyte):
	""" Hent artikel fra datafil

	file_path = sti til datafilen
	entry_id = artikelID fra databasen
	offset = byte offset i filen
	nbyte = antal af bytes der skal læses """

	if dat_version == '1':
		key = KEY_1
		key_offset = ((entry_id + 0x10E7F) * 1097) % len(key)
	elif dat_version == '2':
		key = KEY_2
		key_offset = ((entry_id + 0x170A8) * 1103) % len(key)
#	key_offset = ((entry_id + 0x170A8) * 1103) % 414
#	for i in range(len(entry_data)):
#		entry_data[i] ^= KEY[(i + key_offset) % 414]
#	key_offset = ((entry_id + 0x10E7F) * 1097) % len(KEY)
#	for i in range(10):
#		print '%x'%entry_data[i]
#	print '%x'%(entry_id + 0x10E7F)
#	for i in range(200):
	for i in range(len(entry_data)):
		entry_data[i] ^= key[(i + key_offset) % len(key)]
	return entry_data.tostring()

if __name__ == '__main__':
	dat_file = open('in/Engelsk.dat','r')
	entry_id = 25106
	offset = 7396331
	nbyte = 1860
	get_raw_entry(dat_file, entry_id, offset, nbyte)

def entry_to_html(entry, entry_type):
#	print entry
	entry = entry.strip()
#	entry = re.sub(r'<h3>', '<span style="font-size:11pt">', entry)
#	entry = re.sub(r'</h3>', '</span>', entry)
	entry = re.sub(r'</?font.*?>', '', entry)
	if entry_type == 'lookup':
		entry = re.sub(r'<h2>', '<span style="font-size:8pt">- ', entry)
		entry = re.sub(r'</h2>', ' </span>', entry)
		entry = re.sub(r'<h3>.*?</h3>', '<br/>', entry)
	elif entry_type == 'collocation_lookup':
		entry = re.sub(r'<h3>', '<span style="font-size:8pt">- ', entry)
		entry = re.sub(r'</h3>', ' </span><br/>', entry)
#		entry = re.sub(r'</h3>', '<br/>', entry)
		entry = re.sub(r'</?div>', '', entry)
	elif entry_type == 'reverse':
		if entry.find('h2') == -1:
			entry = re.sub(r'<h3>', '<span style="font-size:8pt">- ', entry)
			entry = re.sub(r'</h3>', ' </span>', entry)
		else:
			entry = re.sub(r'<h2>', '<span style="font-size:8pt">- ', entry)
			entry = re.sub(r'</h2>', ' </span>', entry)
			entry = re.sub(r'<h3>.*?</h3>', '<br/>', entry)
	entry = re.sub(r'\[LYD\]', '', entry)
	entry = re.sub(r'\[INFO\]', '', entry)
	entry = re.sub(r'<div>', '<span>', entry)
	entry = re.sub(r'</div>', ' </span>', entry)
#	entry = re.sub(r'<a href.*?>', '', entry)
#	entry = re.sub(r'</a>', '', entry)
	entry = re.sub(r'</?h[1-9]>', '', entry)
#	entry = re.sub(r'</?i>', '', entry)
#	entry = '- ' + entry
	if entry.endswith('</ol>') or entry.endswith('</ul>'):
		entry = entry + '<br/>'
	else:
		entry = entry + '<br/><br/>'			
#	print '\n',entry,'\n\n'
	return entry

