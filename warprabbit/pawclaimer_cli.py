#!/usr/bin/env python
from glx.collection import Collection
from glx.attribute import Attribute
import glx.helper as helper
import os
import toml

APPNAME = "warprabbit"

def main():
    config = helper.load_app_config(APPNAME)

    collection = Collection(config["community_name"],config["collection_id"])

    clicked = []
    pawatt = Attribute(config["community_name"],config["collection_id"],config["paw_id"])
    pawcards = pawatt.instances()
    for instance in pawcards:
        if instance["interacted_at"]:
            clicked.append(instance["card_id"])
            print(">>> paw was clicked") 
            v = float(instance["value"])
            card = collection.card(instance["card_id"])
            card.increase_attribute_value(config["reward_id"],config["paw_amount"])
            print(">>> reward increased by",config["paw_amount"]) 
            card.remove_attribute(config["paw_id"])
            print(">>> paw was removed") 

    print("has paws:",len(pawcards))
    print("clicked:",clicked)

if __name__ == "__main__":
    main()
