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

The included `analyze.py` is a complete example, but here's a quick rundown:

```python
import swiffas
from swiffas import swftags

# parse the SWF file
p = swiffas.SWFParser ()
with open ('watch_as3.swf', 'rb') as f:
    p.parse (f)

print 'has', p.properties.frame_count, 'frames'
print 'has', len(p.record_headers), 'records; parsed', len(p.tags), 'of them'

# get each exported AS3 program in the SWF file
as3_exports = filter (lambda x: isinstance (x, swftags.DoABC), p.tags)

# print some information about them
for as3_export in as3_exports:
    as3 = swiffas.ABCFile (as3_export.bytecode, 0, len(as3_export.bytecode))
    print as3_export.name, 'has', as3.method_count, 'methods'

    # print all the strings used in the program
    print '\n'.join (map (lambda sinfo: sinfo.value, as3.constant_pool.strings))
```

## Adding new SWF tags

See `swiffas/swftags.py`. Missing tags are listed at the bottom. 

The current limitation is just that you can't encode a bitfields inside a byte aligned object. The BitObject and Unpackable classes just need to be combined.

## License 

Released under the MIT license. Refer to `LICENSE` for complete license text.