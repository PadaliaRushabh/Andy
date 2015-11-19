# arapk  - Android Reverse APK.

arapk is very simple automaton script for decompiling, recompiling, generating the keystore and signing the APK with specified keystore arguments.


Syntax :
-------

>python arapk.py -g <Keystore_name> #Generate user based keystore name
>python arapk.py -n <keystore_name> -s <path_to_apk> #sign the modified apk using the generated keystore
>python arapk.py -d <path_to_apk_decompile> #decompile the apk file 
>python arapk.py -r <path_to_folder_to_recompile> #recompile the modifed folder back to apk

 

Pre-Requisites :
---------------
'python 2.7', 'jarsigner', 'keytool' and "apktool.jar" to be present and set appropriately in environment path. [This process will also be automated soon]

[Expect bugs. This is just beta phase]
[Warning : For educational purpose only]


[More documentation coming soon....]
