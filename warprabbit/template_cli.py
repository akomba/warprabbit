#!/usr/bin/env python 
# get list of engines and owners
# get all community members
# loop through community card
#   is the card in the engine list?
#       yes: 
#           1. make sure it has the engine badge
#           2. set the engine badge to the number of engines
#       no:
#           1. make sure it does not have the engine badge
import sys
import glx.helper as helper

APPNAME = "template"
__version__ = "0.0.1"

def main():
    if "--version" in sys.argv[1:]:
        print(__version__)
        exit(0)

    # check for config file
    # create if none
    config = helper.load_app_config(APPNAME)
    if not config:
        config = { 
                "template_id":False,
                }
        fn = helper.create_app_config(APPNAME,config)
        print("Config file created:",fn)
        print("Please fill it out carefully and run this app again")
        exit()

        # confirm config
        print("Please confirm that config is correct:")
        print("-------")
        for k,v in config.items():
            print(k,":",v)

        print("-------")
        print("Pausing for 10 seconds")
        time.sleep(10)

if __name__ == "__main__":
    main()
