@echo off
rem Deletes unit from Crowdflower (can only be done before starting)
setlocal
set CURL=\cygwin64\bin\curl
%CURL% -X DELETE https://crowdflower.com/jobs/705639/units/%1.json?key=377837b7b5539ef549e678a6bd82cfcdd2a19df4
endlocal