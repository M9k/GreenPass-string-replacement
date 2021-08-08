# GreenPass-string-replacement
This Python script allows you to replace values inside a GreenPass QR Code.
It DOENS'T generate a valid Greenpass, any modification invalidates the cryptographic key of the certification, making it useless. 

I create this script to analyze how the Greenpass is encoded and to see how the Android application react to a incorrect code.
If you are interested in learning more, there are official documents of the European community that describe how it works. 

PS: The original and the replaced string must have the same length, otherwise the new QR is not valid and is not even read.
