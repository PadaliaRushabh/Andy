# Andy  - Android Keystore and Signing Automator.

Andy is very simple automaton script for generating the keystore and signing the APK with that particular keystore.
This script will be handy to those researchers and security professionals who are much more into reversing.

Syntax :
-------
>python andy.py : Generates the keystore with Andy's default credentials.

[upcoming] 
>python andy.py -n [keystore-name] #Generate user based keystore name

>python andy.py -a [apk-path] #Sign the apk using above created keystore

This will save lot of time for security person. 

Pre-Requisites :
---------------
'jarsigner' and 'keytool' to be present and set appropriately in environment path. [This process will also be automated soon]

[Expect bugs. This is just beta phase]
[Warning : For educational purpose only]


[More documentation coming soon....]
