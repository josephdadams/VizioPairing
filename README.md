# VizioPairing

Just a little module I wrote to help pair all the Vizio TVs I have to work with.

Some are the older kind that use port 9000, and some are the newer ones that use port 7345.

To use:

1. Run the `vizio.py` script.
1. It will prompt you for the IP address of the TV.
1. It will prompt you for the port, either 7345 or 9000. If one doesn't work, try the other!
1. After pairing is initiated, a 4 digit code should be displayed on the TV.
1. Enter this code in the script when prompted.
1. If all is succuessful, an Auth Token will be generated and displayed in the script.
1. Use this for whatever you needed it for!