##Wheater app
####Source: http://projects.knmi.nl/klimatologie/daggegevens/selectie.cgi
For running tests in PyCharm: the Run with Python Console checkbox in run config has to be unchecked.
When compiling with pyinstaller the build and dist folders have to be deleted. The command is:
`pyinstaller app.spec`.pip3 install -U \
    -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 \
    wxPython