from deserialise import AVM2Unpackable
import avm2ins

class OptionDetail (AVM2Unpackable):
	_struct = [
		('vlu30', 'val'),
		('B', 'kind'),
	]

class OptionInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'option_count'),
		(OptionDetail, 'option', 'option_count'),
	]

HAS_OPTIONAL = 0x08
HAS_PARAM_NAMES = 0x80

class MethodInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'param_count'),
		('vlu30', 'return_type'),
		('vlu30', 'param_type', 'param_count'),
		('vlu30', 'name'),
		('B', 'flags'),
		(OptionInfo, 'options', lambda d: d['flags'] & HAS_OPTIONAL != 0),
		('vlu30', 'param_names', lambda d: d['param_count'] if (d['flags'] & HAS_PARAM_NAMES != 0) else False),
	]

class MultinameInfo (AVM2Unpackable):
	QName = 0x07
	QNameA = 0x0D
	RTQName = 0x0F
	RTQNameA = 0x10
	RTQNameL = 0x11
	RTQNameLA = 0x12
	Multiname = 0x09
	MultinameA = 0x0E
	MultinameL = 0x1B
	MultinameLA = 0x1C
	TypeName = 0x1D # undocumented

	# 0 for name_idx where applicable indicates the wildcard name

	_struct_QName = [
		('vlu30', 'namespace_idx'),
		('vlu30', 'name_idx') 
	]

	_struct_RTQName = [
		('vlu30', 'name_idx'),
	]

	_struct_Multiname = [
		('vlu30', 'name_idx'),
		('vlu30', 'ns_set_idx')
	]

	_struct_MultinameL = [
		('vlu30', 'ns_set_idx')
	]

	_struct_TypeName = [
		('vlu30', 'name_idx'),
		('vlu30', 'num_params'),
		('vlu30', 'params', 'num_params')
	]

	_multiname_map = {
		QName: _struct_QName,
		QNameA: _struct_QName,
		RTQName: _struct_RTQName,
		RTQNameA: _struct_RTQName,
		RTQNameL: None,
		RTQNameLA: None,
		Multiname: _struct_Multiname,
		MultinameA: _struct_Multiname,
		MultinameL: _struct_MultinameL,
		MultinameLA: _struct_MultinameL,
		TypeName: _struct_TypeName
	}

	_struct = [
		('B', 'kind'),

		# None name indicate just merge the keys with this class
		(_multiname_map, None, 'kind'),
	]

class NsSetInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'count'),
		('vlu30', 'ns', 'count'),
	]

class NamespaceInfo (AVM2Unpackable):
	_struct = [
		('B', 'kind'),
		('vlu30', 'name'),
	]	

class StringInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'size'),
		(unicode, 'value', 'size'),
	]

class ItemInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'key_idx'),
		('vlu30', 'value_idx'),
	]

class MetadataInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'name'),
		('vlu30', 'item_count'),
		(ItemInfo, 'items', 'item_count'),
	]

class CPoolInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'int_count'),
		('vls32', 'ints', lambda d: d['int_count'] - 1),
		('vlu30', 'uint_count'),
		('vlu32', 'uints', lambda d: d['uint_count'] - 1),
		('vlu30', 'double_count'),
		('d', 'doubles', lambda d: d['double_count'] - 1),
		('vlu30', 'string_count'),
		(StringInfo, 'strings', lambda d: d['string_count'] - 1),
		('vlu30', 'namespace_count'),
		(NamespaceInfo, 'namespaces', lambda d: d['namespace_count'] - 1),
		('vlu30', 'ns_set_count'),
		(NsSetInfo, 'ns_sets', lambda d: d['ns_set_count'] - 1),
		('vlu30', 'multiname_count'),
		(MultinameInfo, 'multinames', lambda d: d['multiname_count'] - 1),
	]

class TraitsInfo (AVM2Unpackable):
	Slot = 0
	Method = 1
	Getter = 2
	Setter = 3
	Class = 4
	Function = 5
	Const = 6

	ATTR_Final = 0x1
	ATTR_Override = 0x2
	ATTR_Metadata = 0x3

	_struct_slot = [
		('vlu30', 'slot_id'),
		('vlu30', 'type_name'),
		('vlu30', 'vindex'),
		('B', 'vkind', lambda d: d['vindex'] != 0),
	]

	_struct_class = [
		('vlu30', 'slot_id'),
		('vlu30', 'class_idx'),
	]

	_struct_function = [
		('vlu30', 'slot_id'),
		('vlu30', 'method_idx'),
	]

	_struct_method = [
		('vlu30', 'disp_id'),
		('vlu30', 'method_idx'),
	]

	_trait_data_map = {
		Slot: _struct_slot,
		Const: _struct_slot,
		Class: _struct_class,
		Function: _struct_function,
		Method: _struct_method,
		Getter: _struct_method,
		Setter: _struct_method

	}

	_struct = [
		('vlu30', 'multiname_idx'),
		('B', 'kind'),
		(_trait_data_map, None, lambda d: d['kind'] & 0b1111),
		('vlu30', 'metadata_count', lambda d: (d['kind'] >> 4) & 0x4 != 0),
		('vlu30', 'metadata', lambda d: d['metadata_count'] if ((d['kind'] >> 4) & 0x4) != 0 else False),
	]

class InstanceInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'multiname_idx'),
		('vlu30', 'super_multiname_idx'),
		('B', 'flags'),
		('vlu30', 'protectedNs', lambda d: d['flags'] & 0x08 != 0),
		('vlu30', 'intrf_count'),
		('vlu30', 'interface', 'intrf_count'),
		('vlu30', 'iinit'),
		('vlu30', 'trait_count'),
		(TraitsInfo, 'trait', 'trait_count'),
	]

class ClassInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'cinit'),
		('vlu30', 'trait_count'),
		(TraitsInfo, 'traits', 'trait_count'),
	]

class ScriptInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'init'),
		('vlu30', 'trait_count'),
		(TraitsInfo, 'trait', 'trait_count'),
	]

class ExceptionInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'from'),
		('vlu30', 'to'),
		('vlu30', 'target'),
		('vlu30', 'exc_type'),
		('vlu30', 'var_name'),
	]

class MethodBodyInfo (AVM2Unpackable):
	_struct = [
		('vlu30', 'method'),
		('vlu30', 'max_stack'),
		('vlu30', 'local_count'),
		('vlu30', 'init_scope_depth'),
		('vlu30', 'max_scope_depth'),
		('vlu30', 'code_length'),
		(bytes, 'code', 'code_length'),
		('vlu30', 'exception_count'),
		(ExceptionInfo, 'exception', 'exception_count'),
		('vlu30', 'trait_count'),
		(TraitsInfo, 'trait', 'trait_count'),
	]

	def bytecode (self):
		return list(bytecode)

	def iter_bytecode (self):
		offset = 0
		remaining = len(self.code)

		while remaining > 0:
			# read the instruction identifier
			# (docs actually never say this is a byte)
			insid, objsize = self._unpack_ctype (self.code, offset, 'B')
			offset += objsize
			remaining -= objsize

			instruction = avm2ins.InstructionSet[insid] (self.code, offset, remaining)
			remaining -= instruction._size
			offset += instruction._size

			yield instruction

class ABCFile (AVM2Unpackable):
	_struct = [
		('H', 'minor_version'),
		('H', 'major_version'),
		(CPoolInfo, 'constant_pool'),
		('vlu30', 'method_count'),
		(MethodInfo, 'methods', 'method_count'),
		('vlu30', 'metadata_count'),
		(MetadataInfo, 'metadata', 'metadata_count'),
		('vlu30', 'class_count'),
		(InstanceInfo, 'instances', 'class_count'),
		(ClassInfo, 'classes', 'class_count'),
		('vlu30', 'script_count'),
		(ScriptInfo, 'scripts', 'script_count'),
		('vlu30', 'method_body_count'),
		(MethodBodyInfo, 'method_bodies', 'method_body_count'),
	]
