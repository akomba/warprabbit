#!/usr/bin/env python 
import random
from warprabbit.rabbit import Rabbit
from glx.community import Community
from glx.collection import Collection
from glx.attribute import Attribute
import sys
import os
import time
import glx.helper as helper

APPNAME = "warprabbit"
__version__ = "0.0.1"

def main():
    if "--version" in sys.argv[1:]:
        print(__version__)
        exit(0)

    config_template = { 
        "rabbit_id":False,
        "reward_id":False,
        "reward_amount": 1,
        "paw_id":False,
        "paw_amount": 0.1,
        "rabbitmaster_id": False,
        "max_rabbits": 16
    }
    config = helper.load_or_create_app_config(APPNAME,config_template)

    #    # confirm config
    #    print("Please confirm that config is correct:")
    #    print("-------")
    #    for k,v in config.items():
    #        print(k,":",v)

    #    print("-------")
    #    print("Pausing for 10 seconds")
    #    time.sleep(10)

    collection = Collection(config["community_name"],config["collection_id"])
    rabbitcards = Attribute(config["community_name"],config["collection_id"],config["rabbit_id"]).instances()
    card_ids = [int(m["id"]) for m in collection.cards(raw=True) if (not int(m["id"]) in [rc["card_id"] for rc in rabbitcards])]
   

    # create more if less than max_rabbits
    rabbits_on_the_field = len(rabbitcards)
    for r in range(config["max_rabbits"]-rabbits_on_the_field):
        print("new rabbit added")
        collection.card(random.choice(card_ids)).add_attribute(config["rabbit_id"],1)

    # loop all instances of the rabbit that was caught (interacted with)
    for r in rabbitcards:
        rabbit = Rabbit(config["rabbit_id"],collection.card(r["card_id"]))
        if r["interacted_at"] or rabbit.card.has_attribute(config["rabbitmaster_id"]):
            rabbit.card.increase_attribute_value(config["reward_id"],config["reward_amount"])
            rabbit.kill()
            print("Rabbit caught, added +1 to holy hand grenade")
        else:
            if rabbit.is_ready_to_warp():
                rabbit.card.increase_attribute_value(config["paw_id"],config["paw_amount"],3600)
                rabbit.warp(collection.card(random.choice(card_ids))) # inside selects time
                print("rabbit warped to", str(rabbit.card.id))
            else:
                print("WR",str(rabbit.card.id)+": counter was decreased to",rabbit.decrease_counter())

if __name__ == "__main__":
    main()
