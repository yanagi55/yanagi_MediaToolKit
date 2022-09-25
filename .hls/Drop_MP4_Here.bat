:loop
if "%~1"=="" goto :break
@REM mkdir "%~dpn1"
python "%~dp0/mp4_to_hls.py" "%~dpnx1"
shift

goto :loop
:break