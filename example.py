import sys

import swiffas
from swiffas import swftags

def main():
    if len(sys.argv) != 2:
        sys.stderr.write ('Usage: %s <input.swf>\n' % sys.argv[0])
        sys.exit (1)

    # parse the SWF file
    p = swiffas.SWFParser ()
    with open (sys.argv[1], 'rb') as f:
        p.parse (f)

    # print some information about the SWF
    print 'has', len(p.record_headers), 'records; parsed', len(p.tags), 'of them'
    print 'has', p.properties.frame_count, 'frames'

    # get each exported AS3 program in the SWF file
    as3_exports = filter (lambda x: isinstance (x, swftags.DoABC), p.tags)

    # print some information about them
    for as3_export in as3_exports:
        as3 = swiffas.ABCFile (as3_export.bytecode, 0, len(as3_export.bytecode))
        print as3_export.name, 'has', as3.method_count, 'methods'

        # print all the string table
        print "Strings:"
        print '\n'.join (map (lambda sinfo: sinfo.value, as3.constant_pool.strings))

        # print an assembly listing for each method
        print "Disassembly:"
        for method_body in as3.method_bodies:
            method_info = as3.methods[method_body.method]

            # methods with name index 0 are anonymous
            # otherwise, it represents their name in the global string pool
            if method_info.name != 0:
                method_name = as3.constant_pool.strings[method_info.name - 1].value
            else:
                method_name = "method %d" % method_body.method

            print method_name

            # dump the instruction list
            for instruction in method_body.iter_bytecode():
                pretty_fields = '; '.join (
                    map (
                        lambda f: '%s: %r' % (f, instruction.__dict__[f]),
                        instruction._fields
                    ))
                
                if instruction._fields:
                    print '    %s (%s)' % (instruction._name, pretty_fields)
                else:
                    print '    %s' % instruction._name


            print

if __name__ == '__main__':
    main()