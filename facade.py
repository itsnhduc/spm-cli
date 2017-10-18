import sys
import importlib

importlib.import_module(sys.argv[1]).main(sys.argv[2:])