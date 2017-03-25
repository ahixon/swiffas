from struct import unpack_from, calcsize
from deserialise import BitObject, Unpackable

class SWFRectangle (BitObject):
	_struct = [
		('UB', 'nbits', 5),
		('SB', 'x_min', 'nbits'),
		('SB', 'x_max', 'nbits'),
		('SB', 'y_min', 'nbits'),
		('SB', 'y_max', 'nbits')
	]

class FileAttributesTag (BitObject):
	_struct = [
		('UB', '_reserved_1', 1),
		('UB', 'use_direct_blit', 1),
		('UB', 'use_gpu', 1),
		('UB', 'has_metadata', 1),
		('UB', 'actionscript_3', 1),
		('UB', '_reserved_2', 2),
		('UB', 'use_network', 1),
		('UB', '_reserved_3', 24),
	]

class ContentFreeTag (object):
	def __init__ (self, file, offset, remaining=None):
		self._size = 0

class ProtectTag (ContentFreeTag):
	pass

class End (ContentFreeTag):
	pass
	
class ShowFrame (ContentFreeTag):
	pass

class EnableDebugger (Unpackable):
	_struct = [
		(unicode, 'password')
	]

class EnableDebugger2 (Unpackable):
	_struct = [
		('H', '_reserved'),
		(unicode, 'password')
	]

class DefineBinaryData (Unpackable):
	_struct = [
		('H', 'character_id'),
		('I', '_reserved'),
		(bytes, 'data', None) # None indicates fills rest of tag
	]

class Metadata (Unpackable):
	_struct = [
		(unicode, 'metadata')
	]

class ScriptLimits (Unpackable):
	_struct = [
		('H', 'max_recursion_depth'),
		('H', 'script_timeout_seconds')
	]

class FrameLabel (Unpackable):
	_struct = [
		(unicode, 'name')
	]

class ExportedAsset (Unpackable):
	_struct = [
		('H', 'character_id'),
		(unicode, 'name')
	]

class ExportAssets (Unpackable):
	_struct = [
		('H', 'count'),
		(ExportedAsset, 'tags', 'count')
	]

class ImportedAsset (Unpackable):
	_struct = [
		('H', 'character_id'),
		(unicode, 'name')
	]

class ImportAssets (Unpackable):
	_struct = [
		(unicode, 'url'),
		('H', 'count'),
		(ImportedAsset, 'assets', 'count')
	]

class ImportAssets2 (Unpackable):
	_struct = [
		(unicode, 'url'),
		('B', '_reserved_1'),
		('B', '_reserved_2'),
		('H', 'count'),
		(ImportedAsset, 'assets', 'count')
	]

class SetTabIndex (Unpackable):
	_struct = [
		('H', 'depth'),
		('H', 'tab_index')
	]

class SetBackgroundColor (Unpackable):
	_struct = [
		('B', 'red'),
		('B', 'green'),
		('B', 'blue'),
	]

class ProductInfo (Unpackable):
	_struct = [
		('I', 'product_id'),
		('I', 'edition'),
		('B', 'major_version'),
		('B', 'minor_version'),
		('I', 'build_low'),
		('I', 'build_high'),
		('Q', 'compilation_date'),
	]

class DoABC (Unpackable):
	_struct = [
		('I', 'flags'),
		(unicode, 'name'),
		(bytes, 'bytecode', None) # None indicates fills rest of tag
	]

class ExportedSymbol (Unpackable):
	_struct = [
		('H', 'character_id'),
		(unicode, 'name') # AS3 class name
	] 

class SymbolClass (Unpackable):
	_struct = [
		('H', 'num_symbols'),
		(ExportedSymbol, 'symbols', 'num_symbols')
	]

class DefineScalingGrid (Unpackable):
	_struct = [
		('H', 'character_id'),
		(SWFRectangle, 'center_rect')
	]

TAG_HANDLERS = {
	0: End,
	1: ShowFrame,
	# 2: DefineShape
	# 4: PlaceObject
	# 5: RemoveObject
	# 6: DefineBits
	# 7: DefineButton
	# 8: JPEGTables
	9: SetBackgroundColor,
	# 10: DefineFont
	# 11: DefineText
	# 12: DoAction - most of the ActionScript model lives here
	# 13: DefineFontInfo
	# 14: DefineSound
	# 15: StartSound
	# 17: DefineButtonSound
	# 18: SoundStreamHead
	# 19: SoundStreamBlock
	# 20: DefineBitsLossless (optionally compressed bitmap)
	# 21: DefineBitsJPEG2
	# 22: DefineShape2
	# 23: DefineButtonCxform
	24: ProtectTag,
	# 26: PlaceObject2
	# 28: RemoveObject2
	# 32: DefineShape3
	# 33: DefineText2
	# 34: DefineButton2
	# 35: DefineBitsJPEG3
	# 36: DefineBitsLossless2
	# 37: DefineEditText
	# 39: DefineSprite
	41: ProductInfo,
	43: FrameLabel,
	# 45: SoundStreamHead2
	# 46: DefineMorphShape
	# 48: DefineFont2
	56: ExportAssets,
	57: ImportAssets,
	58: EnableDebugger,
	# 59: DoInitAction
	# 60: DefineVideoStream
	# 61: VideoFrame
	# 62: DefineFontInfo2
	64: EnableDebugger2,
	65: ScriptLimits,
	66: SetTabIndex,
	69: FileAttributesTag,
	# 70: PlaceObject3
	71: ImportAssets2,
	# 73: DefineFontAlignZones
	# 74: CSMTextSettings
	# 75: DefineFont3
	76: SymbolClass,
	77: Metadata,
	78: DefineScalingGrid,
	82: DoABC,
	# 83: DefineShape4
	# 84: DefineMorphShape2
	# 86: DefineSceneAndFrameLabelData
	87: DefineBinaryData
	# 88: DefineFontName
	# 89: StartSound2
	# 90: DefineBitsJPEG4
	# 91: DefineFont4
	# 92: signed swf tag; undocumented
	# 93: EnableTelemetry
}