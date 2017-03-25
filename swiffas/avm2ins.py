from deserialise import AVM2Unpackable

class AVM2Instruction (AVM2Unpackable):
	pass

class AVM2InstructionNoArg(AVM2Instruction):
	def __init__ (self, file, offset, remaining=None):
		self._size = 0
		self._fields = []

class AVM2IndexedInstruction (AVM2Instruction):
	_struct = [
		('vlu30', 'index')
	]

class AVM2VarArgInstruction (AVM2Instruction):
	_struct = [
		('vlu30', 'arg_count')
	]

class AVM2IndexWithVarArgInstruction (AVM2Instruction):
	_struct = [
		('vlu30', 'index'),
		('vlu30', 'arg_count')
	]

class Add(AVM2InstructionNoArg):
	_name = 'add'

class AddInteger (AVM2InstructionNoArg):
	_name = 'addi'

class AsType (AVM2IndexedInstruction):
	_name = 'astype'

class AsTypeRuntime (AVM2InstructionNoArg):
	_name = 'astypelate'

class BitwiseAnd (AVM2InstructionNoArg):
	_name = 'bitand'

class BitwiseNot (AVM2InstructionNoArg):
	_name = 'bitnot'

class BitwiseOr (AVM2InstructionNoArg):
	_name = 'bitor'

class BitwiseXor (AVM2InstructionNoArg):
	_name = 'bitxor'

class CallClosure (AVM2VarArgInstruction):
	_name = 'call'

class CallMethod (AVM2IndexWithVarArgInstruction):
	_name = 'callmethod'

class CallProperty (AVM2IndexWithVarArgInstruction):
	_name = 'callproperty'

class CallPropertyNoSelf (AVM2IndexWithVarArgInstruction):
	_name = 'callproplex'

class CallPropertyVoid (AVM2IndexWithVarArgInstruction):
	_name = 'callpropvoid'

class CallStatic (AVM2IndexWithVarArgInstruction):
	_name = 'callstatic'

class CallSuper (AVM2IndexWithVarArgInstruction):
	_name = 'callsuper'

class CallSuperVoid (AVM2IndexWithVarArgInstruction):
	_name = 'callsupervoid'

class CheckFilter (AVM2InstructionNoArg):
	_name = 'checkfilter'

class CoerceToType (AVM2IndexedInstruction):
	_name = 'coerce'

class CoerceToAny (AVM2InstructionNoArg):
	_name = 'coerce_a'

class CoerceToString (AVM2InstructionNoArg):
	_name = 'coerce_s'

class CoerceToString (AVM2InstructionNoArg):
	_name = 'coerce_s'

class Construct (AVM2VarArgInstruction):
	_name = 'construct'

class ConstructProp (AVM2IndexWithVarArgInstruction):
	_name = 'constructprop'

class ConstructSuper (AVM2VarArgInstruction):
	_name = 'constructsuper'

class ConvertBoolean (AVM2InstructionNoArg):
	_name = 'convert_b'

class ConvertInteger (AVM2InstructionNoArg):
	_name = 'convert_i'

class ConvertDouble (AVM2InstructionNoArg):
	_name = 'convert_d'

class ConvertObject (AVM2InstructionNoArg):
	_name = 'convert_o'

class ConvertUnsigned (AVM2InstructionNoArg):
	_name = 'convert_u'

class ConvertString (AVM2InstructionNoArg):
	_name = 'convert_s'

class Debug (AVM2Instruction):
	DI_LOCAL = 0x1

	_name = 'debug'
	_struct = [
		('B', 'debug_type'),
		('vlu30', 'index'),
		('B', 'reg'),
		('vlu30', 'extra'), # currently unused
	]

class DebugFile (AVM2IndexedInstruction):
	_name = 'debugfile'

class DebugLine (AVM2IndexedInstruction):
	_name = 'debugline'

class DecrementRegister (AVM2IndexedInstruction):
	_name = 'declocal'

class DecrementRegisterInteger (AVM2IndexedInstruction):
	_name = 'declocal_i'

class Decrement (AVM2InstructionNoArg):
	_name = 'decrement'

class DecrementInteger (AVM2InstructionNoArg):
	_name = 'decrement_i'

class DeleteProperty (AVM2IndexedInstruction):
	_name = 'deleteproperty'

class Divide (AVM2InstructionNoArg):
	_name = 'divide'

class DuplicateStackHead (AVM2InstructionNoArg):
	_name = 'dup'

class DefaultXMLNamespace (AVM2IndexedInstruction):
	_name = 'dxns'

class DefaultXMLNamespaceRuntime (AVM2InstructionNoArg):
	_name = 'dxnslate'

class Equals (AVM2InstructionNoArg):
	_name = 'equals'

class EscapeXMLAttribute (AVM2InstructionNoArg):
	_name = 'esc_xattr'

class EscapeXMLElement (AVM2InstructionNoArg):
	_name = 'esc_xelem'

class FindProperty (AVM2IndexedInstruction):
	_name = 'findproperty'

class FindPropertyOrException (AVM2IndexedInstruction):
	_name = 'findpropstrict'

class GetDescendants (AVM2IndexedInstruction):
	_name = 'getdescendants'

class GetGlobalScope (AVM2InstructionNoArg):
	_name = 'getglobalscope'

class GetGlobalSlot (AVM2IndexedInstruction):
	_name = 'getglobalslot'

class FindAndGetProperty (AVM2IndexedInstruction):
	_name = 'getlex'

class GetRegister (AVM2IndexedInstruction):
	_name = 'getlocal'

# I guess I could reduce this somehow...
class GetRegister0 (AVM2InstructionNoArg):
	_name = 'getlocal_0'

class GetRegister1 (AVM2InstructionNoArg):
	_name = 'getlocal_1'

class GetRegister2 (AVM2InstructionNoArg):
	_name = 'getlocal_2'

class GetRegister3 (AVM2InstructionNoArg):
	_name = 'getlocal_3'

class GetProperty (AVM2IndexedInstruction):
	_name = 'getproperty'

class GetScopeObject (AVM2Instruction):
	_name = 'getscopeobject'
	_struct = [
		('B', 'index')
	]

class GetSlot (AVM2IndexedInstruction):
	_name = 'getslot'

class GetPropFromSuper (AVM2IndexedInstruction):
	_name = 'getsuper'

# documentation has these as the same instruction...
class GreaterThanEquals (AVM2InstructionNoArg):
	_name = 'greaterequals'

class GreaterThan (AVM2InstructionNoArg):
	_name = 'greaterthan'

class HasMoreProperties (AVM2InstructionNoArg):
	_name = 'hasnext'

class HasMorePropertiesByRef (AVM2Instruction):
	_name = 'hasnext2'
	_struct = [
		('B', 'object_reg'),
		('B', 'index_reg'),
	]

class AVM2OffsetInstruction (AVM2Instruction):
	_struct = [
		('s24', 'offset')
	]

class BranchEquals (AVM2OffsetInstruction):
	_name = 'ifeq'

class BranchFalse (AVM2OffsetInstruction):
	_name = 'iffalse'

class BranchGreaterEqual (AVM2OffsetInstruction):
	_name = 'ifge'

class BranchGreater (AVM2OffsetInstruction):
	_name = 'ifgt'

class BranchLessEqual (AVM2OffsetInstruction):
	_name = 'ifle'

class BranchLess (AVM2OffsetInstruction):
	_name = 'iflt'

class BranchNotGreaterEqual (AVM2OffsetInstruction):
	_name = 'ifnge'

class BranchNotGreater (AVM2OffsetInstruction):
	_name = 'ifngt'

class BranchNotLessEqual (AVM2OffsetInstruction):
	_name = 'ifnle'

class BranchNotLess (AVM2OffsetInstruction):
	_name = 'ifnlt'

class BranchNotLess (AVM2OffsetInstruction):
	_name = 'ifnlt'

class BranchNotEqual (AVM2OffsetInstruction):
	_name = 'ifne'

class BranchStrictEqual (AVM2OffsetInstruction):
	_name = 'ifstricteq'

class BranchStrictNotEqual (AVM2OffsetInstruction):
	_name = 'ifstrictne'

class BranchTrue (AVM2OffsetInstruction):
	_name = 'iftrue'

class In (AVM2InstructionNoArg):
	_name = 'in'

class IncrementRegister (AVM2IndexedInstruction):
	_name = 'inclocal'

class IncrementRegisterInteger (AVM2IndexedInstruction):
	_name = 'declocal'

class Increment (AVM2InstructionNoArg):
	_name = 'increment'

class IncrementInteger (AVM2InstructionNoArg):
	_name = 'increment_i'

class InitializeProperty (AVM2IndexedInstruction):
	_name = 'initproperty'

class InstanceOf (AVM2InstructionNoArg):
	_name = 'instanceof'

class IsType (AVM2IndexedInstruction):
	_name = 'istype'

class IsTypeRuntime (AVM2InstructionNoArg):
	_name = 'istypelate'

class Jump (AVM2OffsetInstruction):
	_name = 'jump'

class KillRegister (AVM2IndexedInstruction):
	_name = 'kill'

class Label (AVM2InstructionNoArg):
	_name = 'label'

class LessThanEqual (AVM2InstructionNoArg):
	_name = 'lessequals'

class LessThan (AVM2InstructionNoArg):
	_name = 'lessthan'

class Switch (AVM2Instruction):
	_name = 'lookupswitch'
	_struct = [
		('s24', 'default_offset'),
		('vlu30', 'case_count'),
		('s24', 'case_offsets', lambda d: d['case_count'] + 1),
	]

class BitwiseShiftLeft (AVM2InstructionNoArg):
	_name = 'lshift'

class Modulo (AVM2InstructionNoArg):
	_name = 'modulo'

class Modulo (AVM2InstructionNoArg):
	_name = 'modulo'

class Multiply (AVM2InstructionNoArg):
	_name = 'multiply'

class MultiplyInteger (AVM2InstructionNoArg):
	_name = 'multiply_i'

class Negate (AVM2InstructionNoArg):
	_name = 'negate'

class NegateInteger (AVM2InstructionNoArg):
	_name = 'negate_i'

class NewActivation (AVM2InstructionNoArg):
	_name = 'newactivation'

class NewArray (AVM2VarArgInstruction):
	_name = 'newarray'

class NewCatchScope (AVM2IndexedInstruction):
	_name = 'newcatch'

class NewClass (AVM2IndexedInstruction):
	_name = 'newclass'

class NewFunction (AVM2IndexedInstruction):
	_name = 'newfunction'

class NewObject (AVM2IndexedInstruction):
	_name = 'newobject'

class NextPropertyName (AVM2InstructionNoArg):
	_name = 'nextname'

# instruction set has them with hte same operation
# but surely this one gives you the property's value
# not it's name...
class NextPropertyValue (AVM2InstructionNoArg):
	_name = 'nextvalue'

class Nop (AVM2InstructionNoArg):
	_name = 'nop'

class BooleanNot (AVM2InstructionNoArg):
	_name = 'not'

class PopValue (AVM2InstructionNoArg):
	_name = 'pop'

class PopScope (AVM2InstructionNoArg):
	_name = 'popscope'

class PushByte (AVM2Instruction):
	_name = 'pushbyte'
	_struct = [
		('B', 'value')
	]

class PushDouble (AVM2IndexedInstruction):
	_name = 'pushdouble'

class PushFalse (AVM2InstructionNoArg):
	_name = 'pushfalse'

class PushInteger (AVM2IndexedInstruction):
	_name = 'pushint'

class PushNamespace (AVM2IndexedInstruction):
	_name = 'pushnamespace'

class PushNaN (AVM2InstructionNoArg):
	_name = 'pushnan'

class PushNull (AVM2InstructionNoArg):
	_name = 'pushnull'

class PushScope (AVM2InstructionNoArg):
	_name = 'pushscope'

class PushShort (AVM2Instruction):
	_name = 'pushshort'
	_struct = [
		('vlu30', 'value')
	]

class PushString (AVM2IndexedInstruction):
	_name = 'pushstring'

class PushTrue (AVM2InstructionNoArg):
	_name = 'pushtrue'

class PushUnsignedInteger (AVM2IndexedInstruction):
	_name = 'pushuint'

class PushUndefined (AVM2InstructionNoArg):
	_name = 'pushundefined'

class PushWith (AVM2InstructionNoArg):
	_name = 'pushwith'

class ReturnValue (AVM2InstructionNoArg):
	_name = 'returnvalue'

class ReturnVoid (AVM2InstructionNoArg):
	_name = 'returnvoid'

class BitwiseShiftRight (AVM2InstructionNoArg):
	_name = 'rshift'

class SetRegister (AVM2IndexedInstruction):
	_name = 'setlocal'

# again, could be nicer, but there's only 4 registers
class SetRegister0 (AVM2InstructionNoArg):
	_name = 'setlocal_0'

class SetRegister1 (AVM2InstructionNoArg):
	_name = 'setlocal_1'

class SetRegister2 (AVM2InstructionNoArg):
	_name = 'setlocal_2'

class SetRegister3 (AVM2InstructionNoArg):
	_name = 'setlocal_3'

class SetGlobalSlot (AVM2IndexedInstruction):
	_name = 'setglobalslot'

class SetProperty (AVM2IndexedInstruction):
	_name = 'setproperty'

class SetSlot (AVM2IndexedInstruction):
	_name = 'setslot'

class SetSuper (AVM2IndexedInstruction):
	_name = 'setsuper'

class EqualsStrict (AVM2InstructionNoArg):
	_name = 'strictequals'

class Subtract (AVM2InstructionNoArg):
	_name = 'subtract'

class SubtractInteger (AVM2InstructionNoArg):
	_name = 'subtract_i'

class Swap (AVM2InstructionNoArg):
	_name = 'swap'

class ThrowException (AVM2InstructionNoArg):
	_name = 'throw'

class Typename (AVM2InstructionNoArg):
	_name = 'typeof'

class UnsignedBitwiseShiftRight (AVM2InstructionNoArg):
	_name = 'urshift'

# undocumented
class Breakpoint (AVM2InstructionNoArg):
	pass

# undocumented
class FindDefinition (AVM2IndexedInstruction):
	_name = 'finddef'

# undocumented
class ApplyType (AVM2VarArgInstruction):
	_name = 'applytype'

# undocumented
class PushFloat (AVM2IndexedInstruction):
	_name = 'pushfloat'

# undocumented
class PushDecimal (AVM2IndexedInstruction):
	_name = 'pushdecimal'

# undocumented
class PushDecimalNaN (AVM2IndexedInstruction):
	_name = 'pushdnan'

# undocumented
class CallInterface (AVM2IndexedInstruction):
	_name = 'callinterface'

# below are all undocumented; added for flacc
class StoreInteger8 (AVM2InstructionNoArg):
	_name = 'si8'

class StoreInteger16 (AVM2InstructionNoArg):
	_name = 'si16'

class StoreInteger32 (AVM2InstructionNoArg):
	_name = 'si32'

class StoreFloat32 (AVM2InstructionNoArg):
	_name = 'sf32'

class StoreFloat64 (AVM2InstructionNoArg):
	_name = 'sf64'

class LoadInteger8 (AVM2InstructionNoArg):
	_name = 'li8'

class LoadInteger16 (AVM2InstructionNoArg):
	_name = 'li16'

class LoadInteger32 (AVM2InstructionNoArg):
	_name = 'li32'

class LoadFloat32 (AVM2InstructionNoArg):
	_name = 'lf32'

class LoadFloat64 (AVM2InstructionNoArg):
	_name = 'lf64'

class SignExtend1 (AVM2InstructionNoArg):
	_name = 'sxi1'

class SignExtend8 (AVM2InstructionNoArg):
	_name = 'sxi8'

class SignExtend16 (AVM2InstructionNoArg):
	_name = 'sxi16'

InstructionSet = {
	0xa0: Add,
	0xc5: AddInteger,
	0x86: AsType,
	0x87: AsTypeRuntime,
	0xa8: BitwiseAnd,
	0x97: BitwiseNot,
	0xa9: BitwiseOr,
	0xaa: BitwiseXor,
	0x41: CallClosure,
	0x43: CallMethod,
	0x46: CallProperty,
	0x4c: CallPropertyNoSelf,
	0x4f: CallPropertyVoid,
	0x44: CallStatic,
	0x45: CallSuper,
	0x4e: CallSuperVoid,
	0x78: CheckFilter,
	0x80: CoerceToType,
	0x82: CoerceToAny,
	0x85: CoerceToString,
	0x42: Construct,
	0x4a: ConstructProp,
	0x49: ConstructSuper,
	0x76: ConvertBoolean,
	0x73: ConvertInteger,
	0x75: ConvertDouble,
	0x77: ConvertObject,
	0x74: ConvertUnsigned,
	0x70: ConvertString,
	0xef: Debug,
	0xf1: DebugFile,
	0xf0: DebugLine,
	0x94: DecrementRegister,
	0xc3: DecrementRegisterInteger,
	0x93: Decrement,
	0xc1: DecrementInteger,
	0x6a: DeleteProperty,
	0xa3: Divide,
	0x2a: DuplicateStackHead,
	0x06: DefaultXMLNamespace,
	0x07: DefaultXMLNamespaceRuntime,
	0xab: Equals,
	0x72: EscapeXMLAttribute,
	0x71: EscapeXMLElement,
	0x5e: FindProperty,
	0x5d: FindPropertyOrException,
	0x59: GetDescendants,
	0x64: GetGlobalScope,
	0x6e: GetGlobalSlot,
	0x60: FindAndGetProperty,
	0x62: GetRegister,
	0xd0: GetRegister0,
	0xd1: GetRegister1,
	0xd2: GetRegister2,
	0xd3: GetRegister3,
	0x66: GetProperty,
	0x65: GetScopeObject,
	0x6c: GetSlot,
	0x04: GetPropFromSuper,
	0xaf: GreaterThanEquals,
	0xb0: GreaterThan, # spec defines this also as 0xaf
	0x1f: HasMoreProperties,
	0x32: HasMorePropertiesByRef,
	0x13: BranchEquals,
	0x12: BranchFalse,
	0x18: BranchGreaterEqual,
	0x17: BranchGreater,
	0x16: BranchLessEqual,
	0x15: BranchLess,
	0x0f: BranchNotGreaterEqual,
	0x0e: BranchNotGreater,
	0x0d: BranchNotLessEqual,
	0x0c: BranchNotLess,
	0x14: BranchNotEqual,
	0x19: BranchStrictEqual,
	0x1a: BranchStrictNotEqual,
	0x11: BranchTrue,
	0xb4: In,
	0x92: IncrementRegister,
	0xc2: IncrementRegisterInteger,
	0x91: Increment,
	0xc0: IncrementInteger,
	0x68: InitializeProperty,
	0xb1: InstanceOf,
	0xb2: IsType,
	0xb3: IsTypeRuntime,
	0x10: Jump,
	0x08: KillRegister,
	0x09: Label,
	0xae: LessThanEqual,
	0xad: LessThan,
	0x1b: Switch,
	0xa5: BitwiseShiftLeft,
	0xa4: Modulo,
	0xa2: Multiply,
	0xc7: MultiplyInteger,
	0x90: Negate,
	0xc4: NegateInteger,
	0x57: NewActivation,
	0x56: NewArray,
	0x5a: NewCatchScope,
	0x58: NewClass,
	0x40: NewFunction,
	0x55: NewObject,
	0x1e: NextPropertyName,
	0x23: NextPropertyValue,
	0x02: Nop,
	0x96: BooleanNot,
	0x29: PopValue,
	0x1d: PopScope,
	0x24: PushByte,
	0x2f: PushDouble,
	0x27: PushFalse,
	0x2d: PushInteger,
	0x31: PushNamespace,
	0x28: PushNaN,
	0x20: PushNull,
	0x30: PushScope,
	0x25: PushShort,
	0x2c: PushString,
	0x26: PushTrue,
	0x2e: PushUnsignedInteger,
	0x21: PushUndefined,
	0x1c: PushWith,
	0x48: ReturnValue,
	0x47: ReturnVoid,
	0xa6: BitwiseShiftRight,
	0x63: SetRegister,
	0xd4: SetRegister0,
	0xd5: SetRegister1,
	0xd6: SetRegister2,
	0xd7: SetRegister3,
	0x6f: SetGlobalSlot,
	0x61: SetProperty,
	0x6d: SetSlot,
	0x05: SetSuper,
	0xac: EqualsStrict,
	0xa1: Subtract,
	0xc6: SubtractInteger,
	0x2b: Swap,
	0x03: ThrowException,
	0x95: Typename,
	0xa7: UnsignedBitwiseShiftRight,

	# not published in "ActionScript Virtual Machine 2 (AVM2) Overview"

	0x53: ApplyType,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/applytype.dox
	0x5F: FindDefinition,	

	0x35: LoadInteger8,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/li8.dox
	0x36: LoadInteger16,	# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/li16.dox
	0x37: LoadInteger32,	# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/li32.dox
	0x38: LoadFloat32,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/lf32.dox
	0x39: LoadFloat64,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/lf64.dox

	0x3a: StoreInteger8,	# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/si8.dox
	0x3b: StoreInteger16,	# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/si16.dox
	0x3c: StoreInteger32,	# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/si32.dox
	0x3d: StoreFloat32,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/sf32.dox
	0x3e: StoreFloat64,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/sf64.dox

	0x50: SignExtend1,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/sxi1.dox
	0x51: SignExtend8,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/sxi8.dox
	0x52: SignExtend16,		# https://github.com/adobe/avmplus/blob/master/doc/bytecode/src/sxi16.dox

	# entirely undocumented
	# 0x0a - OP_lf32x4
	# 0x0b - OP_sf32x4
	0x01: Breakpoint, 		# OP_bkpt
	0x22: PushFloat,		# OP_pushfloat
	0x33: PushDecimal,
	0x34: PushDecimalNaN,

	# 0x4b - callsuperid
	0x4d: CallInterface

	# 0x101: OP_ext_pushbits
	# 0x102: OP_ext_push_doublebits
}
