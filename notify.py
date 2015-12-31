#!/usr/bin/python
# -*- encoding: utf8 -*-
import sys
import time
import atexit
import urllib
import urllib2
import pjsua as pj

telegramBotId = "XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXX"
telegramChatId = "-XXXXXXX"

sipId = "sip:user@example.com"
sipRegUrl = "sip:example.com"
sipProxy = "sip:example.com"
sipUser = "user"
sipPassword = "password"

# Logging callback
def log_cb(level, str, len):
    print str,

class CallbackAccount(pj.AccountCallback):
    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)
        
    def on_incoming_call(self, call):
        info = call.info()
        data = { 'chat_id' : '%s' %telegramChatId, 'parse_mode' : 'Markdown', 'text' : '```Nova ligação de %s em %s```' %(info.remote_contact, time.strftime("%Y-%m-%d %H:%M")) }
        urllib2.urlopen("https://api.telegram.org/bot%s/sendMessage?%s" %(telegramBotId, urllib.urlencode(data)) ).read()
        
try:
    # Create library instance
    lib = pj.Lib()

    # Init library with default config
    lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))
    
    transportConfig = pj.TransportConfig();
    transportConfig.port = 5080

    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP, transportConfig)
    
    # Start the library
    lib.start()

    acc_cfg = pj.AccountConfig()
    acc_cfg.id = "%s" %sipId
    acc_cfg.reg_uri = "%s" %sipRegUrl
    acc_cfg.proxy = [ "%s" %sipProxy ]
    acc_cfg.auth_cred = [ pj.AuthCred("*", "%s" %sipUser, "%s" %sipPassword) ]

    acc_ck = CallbackAccount()
    acc = lib.create_account(acc_cfg, cb=acc_ck)

    # Wait for ENTER before quitting
    print "Press <ENTER> to quit"
    input = sys.stdin.readline().rstrip("\r\n")

    # We're done, shutdown the library
    lib.destroy()
    lib = None

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()
    lib = None
    sys.exit(1)
    
