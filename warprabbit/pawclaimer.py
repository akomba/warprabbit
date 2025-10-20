#!/usr/bin/env python
from glx.collection import Collection
from glx.attribute import Attribute
import glx.helper as helper
import os
import toml
import argparse

APPNAME = "warprabbit"

def main(community_name=None):
    print("manually rewarding paw clicks")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--community")
    args = parser.parse_args()
    
    # find community
    if not community_name:
        if args.community:
            community_name = args.community
        else:
            print(APPNAME,"No community name is given, exiting.")
            return False
    
    config = helper.load_app_config(community_name,APPNAME)
    pawatt = Attribute(community_name,config["collection_id"],config["paw_id"])
    pawcards = pawatt.instances()
    for instance in pawcards:
        if instance["interacted_at"]:
            print(">",instance,"<")
            interact(community_name,APPNAME,instance["card_id"])

    print("has paws:",len(pawcards))


def interact(community_name, app_name, card_id, data=None):
    config = helper.load_app_config(community_name,app_name)
    collection = Collection(community_name,config["collection_id"])
    print("i> paw was clicked")
    # find attribute instance
    card = collection.card(card_id)
    card.increase_attribute_value(config["reward_id"],config["paw_amount"])
    print("reward increased by",config["paw_amount"]) 
    card.remove_attribute(config["paw_id"])
    print("paw was removed") 

if __name__ == "__main__":
    main()
