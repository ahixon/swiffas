import io
import zlib
# import pylzma - not a hard dependency; see loader below

from deserialise import Unpackable, BitObject
from struct import unpack, unpack_from, calcsize

from swftags import TAG_HANDLERS, SWFRectangle
from StringIO import StringIO

class SWFHeader (Unpackable):
	_struct = [
		('c', 'sig0'),
		('c', 'sig1'),
		('c', 'sig2'),
		('B', 'version'),
		('I', 'file_length')]

	_compression_signatures = {
		'F': None,
		'C': 'zlib',
		'Z': 'lzma'
	}

	@property
	def compression (self):
		return self._compression_signatures[self.sig0]

class SWFRecordHeader (Unpackable):
	def __init__ (self, data, offset):
		tagcode_and_length = unpack_from ('<H', data, offset)[0]
		self.tagcode = tagcode_and_length >> 6
		self.length = tagcode_and_length & ((1 << 6) - 1)

		self._size = calcsize ('<H')
		offset += calcsize ('<H')

		if self.length >= 0x3F:
			self.length = unpack_from ('<I', data, offset)[0]
			self._size += calcsize ('<I')

class SWFProperties (Unpackable):
	_struct = [
		(SWFRectangle, 'frame_size'),
		('H', 'frame_rate'),
		('H', 'frame_count')]

class SWFParser (object):
	def __init__ (self, file=None):
		self.header = None
		self.properties = None

		# list of parsed tag objects, in file order
		self.tags = []

		# list of SWFRecordHeaders, in file order (parsed and unparsed tags)
		self.record_headers = [] 	

		if file:
			self.parse (file)

	def parse (self, filelike, warn_unknown_tags=True):
		# grab the header
		offset = 0

		# header is 8 bytes long
		hsize = SWFHeader._ssize()
		self.header = SWFHeader (filelike.read (hsize), offset, hsize)
		offset += self.header._size

		if self.header.compression == 'zlib':
			# for now, just decompress the whole thing
			decompressed = zlib.decompress (filelike.read())
			fbuf = decompressed
			# filelike = StringIO (decompressed)

			# ensure decompressed size matches file size
			assert self.header.file_length - hsize == len(decompressed)

			# reset offset since we will load from compressed buffer
			# which is already an offset of 8 bytes in
			offset = 0
		elif self.header.compression == 'pylzma':
			import pylzma
			decompressed = pylzma.decompress (filelike.read())
			fbuf = decompressed
			assert self.header.file_length - hsize == len(decompressed)
			offset = 0
		else:
			fbuf = filelike.read()
			offset = 0

		self.properties = SWFProperties (fbuf, offset)
		offset += self.properties._size

		# now read all the headers we have
		self.tags = []
		self.record_headers = []

		file_offset = (self.properties._size + self.header._size)
		hdr_count = 0
		while file_offset < self.header.file_length:
			hdr = SWFRecordHeader (fbuf, offset)
			self.record_headers.append (hdr)

			offset += hdr._size
			file_offset += hdr._size
			hdr_count += 1

			if hdr.tagcode in TAG_HANDLERS:
				handler = TAG_HANDLERS[hdr.tagcode]
				tag = handler(fbuf, offset, remaining=hdr.length)

				# make sure we deserialised the whole tag
				assert tag._size == hdr.length, \
					"only deserialised %d of %d bytes in tag %r" % (
						tag._size,
						hdr.length,
						tag
					)

				self.tags.append (tag)
			elif warn_unknown_tags:
				print 'warning: unknown tag', hdr.tagcode

			offset += hdr.length
			file_offset += hdr.length