@echo off

set fn=%1
set p2=%2

set pyFile=%~dp0\%fn%.py %p2%

python %pyFile%