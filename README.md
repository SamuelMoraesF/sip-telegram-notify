# VoIP notifications over Telegram

This app requires the `pjsip` library.

* `cd /tmp`
* `svn checkout http://svn.pjsip.org/repos/pjproject/trunk/`
* `cd trunk/`
* `./configure CFLAGS='-fPIC'`
* `make dep`
* `make`
* `sudo make install`
* `cd pjsip-apps/src/python/`
* `sudo python setup.py install`
