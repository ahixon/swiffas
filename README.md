# swifas

A small Python 2 library that provides:

* a SWF parser (enough tags to get the Actionscript stuff out, but a few others too)
* a complete AVM2 parser (Actionscript 3 bytecode)

Original intention was to provide a transpiler from compiled AS3 code to LLVM IR. 

There are one or two in other languages, but most have bitrotted, or they were too incomplete to parse my target files.

Serialising back to SWF files should be relatively straightforward to add.

## Installation

    pip install swiffas

## Usage

Take a look at `example.py` -- it prints a disassembly listing for all the Actionscript code it finds in a DoABC tag.

In any case, here's a quick rundown:

```python
import swiffas
from swiffas import swftags

# parse the SWF file
p = swiffas.SWFParser ()
with open ('example.swf', 'rb') as f:
    p.parse (f)

print 'has', p.properties.frame_count, 'frames'
print 'has', len(p.record_headers), 'records; parsed', len(p.tags), 'of them'

# get each exported AS3 program in the SWF file
as3_exports = filter (lambda x: isinstance (x, swftags.DoABC), p.tags)

# print some information about them
for as3_export in as3_exports:
    as3 = swiffas.ABCFile (as3_export.bytecode)
    print as3_export.name, 'has', as3.method_count, 'methods'

    # print all the strings used in the program
    print '\n'.join (map (lambda sinfo: sinfo.value, as3.constant_pool.strings))
```

## Parsed object structure

The structure of each parsed SWF and AVM2 object can be found in `swiffas/swftags.py` and `swiffas/avm2.py`, respectively. Each element of the `_struct` list is instantiated on the object during deserialisation (if its size is not None, False or 0).

Each tuple in `_struct` is of the form `(type, name, optional size or existence boolean)`. The size may be an integer, or refer to a previous field's value.

A special case of a tuple is where its type is `bytes`, is the last element in the list and has size `None`. This represents a field that takes up the remainder of the object, and who's contents are those bytes.

## Doing stuff with AS3

There's no AS3 VM packaged (yet), so you'll manually iterate over each method's body, and link all the indexes up.

## Adding new SWF tags

See `swiffas/swftags.py`. Missing tags are listed at the bottom. 

The current limitation is just that you can't encode a bitfields inside a byte aligned object. The BitObject and Unpackable classes just need to be combined.

## Adding new AVM2 instructions

See `swiffas/avm2ins.py`. 

All the ones from the specification are included, as are several undocumented instructions (including all the FlasCC ones).

There are a few undocumented ones in [this table](https://www.free-decompiler.com/flash/docs/as3_pcode_instructions.en.html) that we don't support, but be weary that some entries on there *are* wrong. 

However, it's better to cross check with Adobe's [source code drop](https://github.com/adobe/avmplus) of their Actionscript virtual machine (downside being you have to navigate through lots of cruft to get what you want).

## License 

Released under the MIT license. Refer to `LICENSE` for complete license text.