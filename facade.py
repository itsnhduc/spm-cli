import sys
import importlib
import os

# available modules
modules = ['add', 'find', 'init', 'list', 'publish', 'remove']

if len(sys.argv) == 1:
    print("""
    SCSE Package Manager.

    Usage:
      spm init            -- Initialize SPM
      spm add             -- Install all packages listed in spm.json
      spm add <name>      -- Install a new package and add to spm.json
      spm remove <name>   -- Remove a package listed in spm.json
      spm find <name>     -- Find a package
      spm list            -- List all packages in spm.json
      spm publish         -- Publish current project as a package
    """)
elif sys.argv[1] in modules:
    # call module
    importlib.import_module(sys.argv[1]).main(sys.argv[2:])
else:
    # module not found
    print('Command "{}" not found.'.format(sys.argv[1]))
    print('Use "$ spm" for further instructions.')
