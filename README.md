# nfcpyr
Do cool stuff with NFC and Raspberry Pi's

<img src="http://static.rejh.nl/phpth/phpThumb.php?w=640&h=240&zc=1&src=http://storage.rejh.nl/_stored/res/github/IMG_6186.JPG" />

<br /><br />

Introduction
===========

<br />

##What
-----------

Nfcpyr lets you use a raspberry pi with a NFC reader to trigger all sorts of things via http requests.

It supports the following events:

* On_scan - triggered whenever you scan a compatible NFC card
* On_checkin - triggered when you 'check in'
* On_checkout - triggered when you 'check out'

The following actions are supported for above mentioned events:

* Check in - a list of other readers that should register you as 'checked in' [1]
* Check out - a list of other readers that should register you as 'checked out' [1]
* Url requests - a list of urls that are requested [2]

[1] For example: if you 'check in' at the livingroom it will automatically check you in at the front door (in case you missed that one). Any actions that are associated with checking in using the reader at the front door will also be triggered. It works other way around, too: Checking out at the front door may check you out at all readers in the building and trigger any actions that are associated with those.

[2] For example: if you have lights that can be turned on or off via a http request you can trigger that. Certain supported keywords will be replaced before requesting the url so you can pass parameters (like the username or name of the reader).

<br data-effect="nomal"/>

Installation
===========

<br />

##Requirements
-----------

* Raspberry Pi with Raspbian (Jessie)
* NFC reader (tested with ACR122U)
* Python 2 + bunch of python 2 modules (simplejson, netifaces, pygame)
* Libnfc, python-usb

I'm working on an installation script that installs all the required software components and sets up raspbian to properly work with Nfcpyr. The short version is: you  need to install the above mentioned requirements. 

For the ACR122U reader you should get it working by running these commands in the terminal:

```bash:terminal
# Install python modules..
sudo pip2 install simplejson
sudo pip2 install netifaces
sudo pip2 install pygame
# Install nfcpy requirements..
sudo apt-get install python-usb
# Install ACR122U pcsc driver
sudo apt-get install libpcsclite1
sudo apt-get install libnfc-bin
modprobe -r pn533 nfc
sudo reboot
sudo dpkg -i [acr122u driver package filename] # google "acr122u driver download"
sudo reboot
```

##Setting up Nfcpyr
------------

**Set up a reader**

  * Download or copy the contents of the /python/nfcpyr folder to the raspberry
  * Copy nfcpyr.config.json and nfcpyr.users.json from 'data_examples' to 'data'
  * Edit the json files (see examples below)
  * Start nfcpyr by running 'python2 nfcpyr.py'
  * Repeat the steps for every raspberry/reader you want to set up

```text:nfcpyr.config.json
{

    # Id, user and pass are used to generate an apikey which identifies your 'group' of readers
    # These should be identical for every raspberry/reader you set up
    "nfcpyr_id":"YOUR_CUSTOM_ID", 
    "nfcpyr_user":"CUSTOM_USERNAME",
    "nfcpyr_pass":"CUSTOM_PASSWORD",
    
    # The url of the nfcpyr api. You can run it on your own server or use mine
    "url_nfcpyrapi":"http://www.rejh.nl/nfcpyr/api/?",
    
    # The configuration of this reader
    "reader":{
        "id":"nfcpi001", # a unique(!) id of this reader
        "name":"Livingroom", # a human-readable name for this reader
        "on_checkin":{
            "checkout":[
                "nfcpi002"
            ],
            "url_requests":[
                "http://www.google.com"
            ]
        },
        "on_checkout":{
            "checkout":[],
            "url_requests":[]
        }
    },
    
    "sounds":{
        "enabled":true,
        "checkin":"sound/snd.beeps01.ogg",
        "checkout":"sound/snd.fail01.ogg"
    }
    
}
```

<br data-effect="turn"/>
