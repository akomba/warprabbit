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
from glx.logger import Logger
import argparse

APPNAME = "warprabbit"
__version__ = "0.0.4"

CONFIG_TEMPLATE = { 
    "rabbit_id":False,
    "reward_id":False,
    "reward_amount": 1,
    "paw_id":False,
    "paw_amount": 0.1,
    "rabbitmaster_id": False,
    "max_rabbits": 16,
    "repeat": 1
}


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-a", "--add", type=int)
    parser.add_argument("-c", "--community")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)

    if not args.community:
        print(APPNAME,"No community name is given, exiting.")
        return False
    else:
        run(args.community)

def main(community_name=None):
    if not community_name:
        print(APPNAME,"No community name is given, exiting.")
        return False
    
    
    config = helper.load_or_create_app_config(community_name,APPNAME,CONFIG_TEMPLATE)
    Logger().init(community_name)
    
    #==========================

    collection = Collection(community_name,config["collection_id"])
    rabbitcards = Attribute(community_name,config["collection_id"],config["rabbit_id"]).instances()
    card_ids = [int(m["id"]) for m in collection.cards(raw=True) if (not int(m["id"]) in [rc["card_id"] for rc in rabbitcards])]
    
    #if args.add:
    #    # add a new rabbit to the given card
    #    # (used for testing)
    #    Logger().logger.info("WR new rabbit insreted "+str(args.add))
    #    collection.card(args.add).add_attribute(config["rabbit_id"],1)
    #    print("Rabbit added to",args.add)
    #    exit()

    # replenish rabbits
    rabbits_on_the_field = len(rabbitcards)
    for r in range(config["max_rabbits"]-rabbits_on_the_field):
        newcard = random.choice(card_ids)
        print("new rabbit added:",newcard)
        Logger().logger.info("WR new rabbit added "+str(newcard))
        collection.card(newcard).add_attribute(config["rabbit_id"],1)

    # loop all instances of the rabbit that was caught (interacted with)
    for r in rabbitcards:
        rabbit = Rabbit(config["rabbit_id"],collection.card(r["card_id"]))
        if r["interacted_at"] or rabbit.card.has_attribute(config["rabbitmaster_id"]):
            Logger().logger.info("WR rabbit caught on "+str(r["card_id"])+" and reward distributed: "+str(config["reward_id"])+" "+str(config["reward_amount"]))
            interact(community_name,APPNAME,r["card_id"])
        else:
            if rabbit.is_ready_to_warp():
                rabbit.card.increase_attribute_value(config["paw_id"],config["paw_amount"],3600)
                rabbit.warp(collection.card(random.choice(card_ids))) # inside selects time
                print("rabbit warped to", str(rabbit.card.id))
                Logger().logger.info("WR rabbit warped to "+str(rabbit.card.id))
            else:
                c = rabbit.decrease_counter()
                print("WR",str(rabbit.card.id)+": counter was decreased to",c)
                Logger().logger.info("WR rabbit CARD "+str(rabbit.card.id)+" counter decreased to "+str(c))

def interact(community_name, app_name, card_id, data=None):
    print("i> rabbit was caught.")
    config = helper.load_app_config(community_name,APPNAME)
    collection = Collection(community_name,config["collection_id"])
    rabbit = Rabbit(config["rabbit_id"],collection.card(card_id))
    rabbit.card.increase_attribute_value(config["reward_id"],config["reward_amount"])
    rabbit.kill()
    print("Rabbit on "+str(card_id)+" caught, added +"+str(config["reward_amount"])+" to reward attribute ("+str(config["reward_id"])+")")
 
if __name__ == "__main__":
    run()
