# nfcpyr
Do cool stuff with NFC and Raspberry Pi's

<img src="http://static.rejh.nl/phpth/phpThumb.php?w=640&h=240&zc=1&src=http://storage.rejh.nl/_stored/res/github/IMG_6186.JPG" />

<br /><br />

Introduction
===========

What
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

[1] For example: if you 'check in' at the livingroom it can automatically check you in at the front door (in case you missed that one). Any actions that are associated with checking in using the reader at the front door will in this case also be triggered. It works other way around, too: Checking out at the front door may check you out at all readers in the building and trigger any actions that are associated with those.

[2] For example: if you have lights that can be turned on or off via a http request you can trigger that. Certain supported keywords will be replaced before requesting the url so you can pass parameters (like the username or name of the reader).

<br data-effect="nomal"/>

Documentation
===========

See the Wiki:
https://github.com/rejhgadellaa/nfcpyr/wiki
