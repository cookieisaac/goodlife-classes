wget https://bootstrap.pypa.io/get-pip.py \
&& python get-pip.py 
&& pip install mechanize
&& pip install bs4

#Load javascript generated content
pip install selenium
&& pip install selenium-requests

#Use real browser
yum install firefox
#Or headless dummy browser
 wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
tar jvxf phantomjs-2.1.1-linux-x86_64.tar.bz2
yum install fontconfig

