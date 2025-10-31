#!/usr/bin/env python
from glx.collection import Collection
from glx.attribute import Attribute
import glx.helper as helper
import glx.apphelper
import os
import toml
import argparse

APPNAME = "warprabbit"

def main(community_name):
    config = helper.load_app_config(community_name,APPNAME)
    if not config:
        return False

    pawatt = Attribute(community_name,config["collection_id"],config["paw_id"])
    pawcards = pawatt.instances()
    for instance in pawcards:
        if instance["interacted_at"]:
            print("   *pawclaimer:",instance["card_id"],"interacted.")
            interact(community_name,APPNAME,instance["card_id"])

    print("has paws:",len(pawcards))

def cli():
    print("manually rewarding paw clicks")
    parser = glx.apphelper.setup_parser()
    args = parser.parse_args()
    community_name = glx.apphelper.process_common_args(args,None,APPNAME)
    main(community_name)

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
