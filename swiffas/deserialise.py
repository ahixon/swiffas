import bitstring
from struct import unpack, unpack_from, calcsize
import math

class BitObject (object):
	def __init__ (self, data, offset, remaining=None):
		# okay, we need to calculate the size first
		self.size_in_bits = 0

		bs = bitstring.ConstBitStream (bytes=data)
		bs.bytepos = offset

		for field in self._struct:
			fmt, name, field_size = field
			# TODO: handle regular struct sizes later?
			# or merge back into Unpackable?

			if not isinstance (field_size, int):
				# look up the bit size from an earlier field
				field_size = self.__dict__[field_size]

			if fmt == 'UB':
				self.__dict__[name] = bs.read ('uint:%d' % field_size)
			elif fmt == 'SB':
				self.__dict__[name] = bs.read ('int:%d' % field_size)
			else:
				raise ValueError ("unknown fmt " + fmt)

			self.size_in_bits += field_size

		bs.bytealign()
		self._size = bs.bytepos - offset

class Unpackable (object):
	byte_order = '<'
	def _unpack_child (self, data, offset, remaining, fmt, size=None):
		if size != None:
			# array, dependent on some other field
			values = []
			objsize = 0

			for i in xrange (size):
				if remaining:
					subremaining = remaining - objsize
				else:
					subremaining = None

				value = fmt (data, offset + objsize, remaining=subremaining)
				objsize += value._size

				values.append (value)

			value = values
		else:
			if remaining:
				subremaining = remaining
			else:
				subremaining = None

			value = fmt (data, offset, remaining=subremaining)
			objsize = value._size

		return (value, objsize)

	def _unpack_bytes (self, data, offset, remaining, size=None):
		if size == None:
			# use remaining data (only if last field)
			# we could support non-last field to guess size
			# but then we'd have to calculate gaps in sizing.. not important (yet)
			# assert name == self._struct[-1][1]
			assert remaining

			size = remaining

		value = data[offset:offset + size]
		objsize = len(value)

		return (value, objsize)

	def _unpack_string (self, data, offset, remaining, size=None):
		# keep walking until we find \0
		if size is None:
			str_end = data.index ('\0', offset, offset + remaining)
			value = unicode(data[offset : str_end], 'utf-8')
			objsize = len(value) + 1
		else:
			value = unicode(data[offset : offset + size], 'utf-8')
			objsize = size
		
		return (value, objsize)

	def _unpack_ctype (self, data, offset, fmt):
		value = unpack_from (self.byte_order + fmt, data, offset)[0]
		objsize = calcsize (self.byte_order + fmt)
		return (value, objsize)

	def _unpack_object (self, data, offset, remaining, fmt, size=None):
		if fmt == None:
			return (None, 0)
		elif fmt == bytes:
			return self._unpack_bytes (data, offset, remaining, size)
		elif fmt == unicode:
			return self._unpack_string (data, offset, remaining, size)
		elif isinstance (fmt, list):
			return self._unpack_from_struct (fmt, data, offset, remaining)
		elif isinstance (fmt, dict):
			# lookup the relevant type based on the size
			try:
				new_fmt = fmt[size]
			except KeyError:
				print "failed to find", size, "in type table", fmt
				raise

			return self._unpack_object (data, offset, remaining, new_fmt)
		elif type (fmt) == type:
			# unpack child structure
			return self._unpack_child (data, offset, remaining, fmt, size)
		else:
			values = []
			objsize = 0

			if size:
				# array
				for i in xrange (size):
					thisval, thissize = self._unpack_ctype (data, offset, fmt)
					objsize += thissize
					offset += thissize
					values.append (thisval)

				return (values, objsize)
			elif size == None:
				return self._unpack_ctype (data, offset, fmt)
			else:
				return (None, 0)

	def __init__ (self, data, offset=0, remaining=None):
		keys, self._size = self._unpack_from_struct (self._struct, data, offset, remaining, place_in_self=True)

		self.__dict__.update (keys)
		self._fields = keys.keys()
	
	def _unpack_from_struct (self, struct, data, offset, remaining, place_in_self=False):
		structsize = 0
		keys = {}

		for field in struct:
			if len(field) == 3:
				fmt, name, size = field
			else:
				fmt, name = field
				size = None

			value = None

			if size is not None and type(size) != int:
				if type(size) == str:
					size = keys[size]
				else:
					size = size(keys)

			if type(size) == bool:
				if size == True:
					# deserialise it, but not actually array
					size = None

			# okay, deserialise it
			if size == False and type(fmt) != dict:
				# XXX: really do set strings to None, but not ~this~ way
				if fmt != unicode:
					continue

			value, objsize = self._unpack_object (data, offset, remaining, fmt, size)
			
			offset += objsize
			structsize += objsize
			if remaining:
				remaining -= objsize

			if value is not None:
				if not name:
					# if you want to not provide a name to merge value
					# with the child, then you MUST return deserialise to dict
					assert isinstance (value, dict)
					keys.update (value)
				else:
					keys[name] = value

		return (keys, structsize)

	@classmethod
	def _ssize (self):
		"""Static size of a structure. Returns size in bytes for fixed structures,
		and None for dynamic structures."""
		static_size = 0

		for field in self._struct:
			if len(field) == 3:
				fmt, name, size = field
			else:
				fmt, name = field
				size = None

			if size is not None and size is not int:
				return None

			if isinstance (fmt, str) or isinstance (fmt, unicode):
				single_field_size = calcsize (self.byte_order + fmt)
			else:
				# get size of child object
				single_field_size = fmt._ssize()
				if single_field_size == None:
					raise ValueError ("cannot get static size from %r" % fmt)

			if size:
				# array
				static_size += size * single_field_size
			else:
				# single element
				static_size += single_field_size

		return static_size


class AVM2Unpackable (Unpackable):
	byte_order = '<'

	def _unpack_s24 (self, data, offset, remaining):
		(low, lowsize) = self._unpack_ctype (data, offset, 'H')
		(high, highsize) = self._unpack_ctype (data, offset + lowsize, 'B')

		# unsigned value
		value = (high << 16) + low

		mask = 1 << (24 - 1)
		value = -(value & mask) + (value & ~mask)

		return (value, lowsize + highsize)

	def _unpack_vl (self, data, offset, remaining, fmt):
		value = 0
		bitoffset = 0
		objsize = 0

		has_next = True
		vl_len = 0
		while has_next:
			# (thisval, subsize) = self._unpack_ctype (data, offset, 'B')
			thisval = ord(data[offset])
			subsize = 1

			objsize += subsize
			vl_len += 1
			offset += subsize

			# bottom 7 bits indicate value for byte
			subval = thisval & ((1 << 7) - 1)
			value = value | (subval << bitoffset)

			# top 1 bit indicates if the next byte belongs to this value
			has_next = not (thisval & (1 << 7) == 0)
			bitoffset += 7

		assert vl_len >= 1 and vl_len <= 5

		# mask to size
		if fmt == 'vlu30':
			mask = (1 << 30) - 1
			value = value & mask
		elif fmt == 'vlu32' or 'vls32':
			mask = (1 << 32) - 1
			value = value & mask

		# do signed-ness
		if fmt == 'vls32':
			mask = 1 << (32 - 1)
			value = -(value & mask) + (value & ~mask)

		return (value, objsize)

	def _unpack_object (self, data, offset, remaining, fmt, size=None):
		# variable length bits
		value = None
		objsize = 0

		if fmt == 'vlu30' or fmt == 'vlu32' or fmt == 'vls32':
			if size:
				# array
				value = []
				for i in xrange (size):
					thisval, thissize = self._unpack_vl (data, offset, remaining, fmt)
					objsize += thissize
					offset += thissize
					if remaining:
						remaining -= thissize

					value.append (thisval)

			else:
				value, objsize = self._unpack_vl (data, offset, remaining, fmt)
		elif fmt == 's24':
			if size:
				value = []
				for i in xrange(size):
					thisval, thissize = self._unpack_s24 (data, offset, remaining)
					objsize += thissize
					offset += thissize
					if remaining:
						remaining -= thissize

					value.append (thisval)
			else:
				value, objsize = self._unpack_s24 (data, offset, remaining)
		else:
			return Unpackable._unpack_object (self, data, offset, remaining, fmt, size)

		return (value, objsize)