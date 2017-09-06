@echo off

set fn=%1
set p2=%2

set pyFile=%fn%.py %p2%

python %pyFile%

REM pause