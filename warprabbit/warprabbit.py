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
import glx.apphelper
import argparse

CONFIG_TEMPLATE = "config_template.toml"
APPNAME = "warprabbit"
__version__ = "0.6.4"

def cli():
    parser = glx.apphelper.setup_parser()
    parser.add_argument("-a", "--add", type=int)
    args = parser.parse_args()
    community_name = glx.apphelper.process_common_args(args,__version__,APPNAME)

    if args.add:
        config = helper.load_app_config(community_name,APPNAME)
        if not config:
            print("Can't find config file, can't add rabbit.")
            exit()
        collection = Collection(community_name,config["collection_id"])
        collection.card(args.add).add_attribute(config["rabbit_id"],1)
        print("Rabbit added to",args.add)
        exit()

    #print("config file location:")
    #print(os.path.join(os.path.dirname(os.path.abspath(__file__))))
    main(community_name)

def main(community_name):
    config_template = os.path.join(os.path.dirname(os.path.abspath(__file__)),CONFIG_TEMPLATE)
    config = helper.load_app_config(community_name,APPNAME,config_template)
    if not config:
        return False

    Logger().init(community_name)

    collection = Collection(community_name,config["collection_id"])

    rabbitcards = Attribute(community_name,config["collection_id"],config["rabbit_id"]).instances()
    card_ids = [int(m["id"]) for m in collection.cards(raw=True) if (not int(m["id"]) in [rc["card_id"] for rc in rabbitcards])]
    
    # replenish rabbits
    rabbits_on_the_field = len(rabbitcards)
    for r in range(config["max_rabbits"]-rabbits_on_the_field):
        newcard = random.choice(card_ids)
        print("    WR new rabbit added:",newcard)
        Logger().logger.info("    WR new rabbit added "+str(newcard))
        collection.card(newcard).add_attribute(config["rabbit_id"],1)

    # loop all instances of the rabbit that was caught (interacted with)
    for r in rabbitcards:
        rabbit = Rabbit(config,collection.card(r["card_id"]))
        if r["interacted_at"] or rabbit.card.has_attribute(config["rabbitmaster_id"]):
            Logger().logger.info("    WR rabbit caught on "+str(r["card_id"])+" and reward distributed: "+str(config["reward_id"])+" "+str(config["reward_amount"]))
            interact(community_name,APPNAME,r["card_id"])
        else:
            if rabbit.is_ready_to_warp():
                rabbit.card.increase_attribute_value(config["paw_id"],config["paw_amount"],60*24)
                rabbit.warp(collection.card(random.choice(card_ids))) # inside selects time
                print("    WR rabbit warped to", str(rabbit.card.id))
                Logger().logger.info("WR rabbit warped to "+str(rabbit.card.id))
            else:
                c = rabbit.decrease_counter()
                print("    WR",str(rabbit.card.id)+": counter was decreased to",c)
                Logger().logger.info("WR rabbit CARD "+str(rabbit.card.id)+" counter decreased to "+str(c))

def interact(community_name, app_name, card_id, data=None):
    print("    WR i> rabbit was caught.")
    config = helper.load_app_config(community_name,APPNAME)
    collection = Collection(community_name,config["collection_id"])
    rabbit = Rabbit(config,collection.card(card_id))
    rabbit.card.increase_attribute_value(config["reward_id"],config["reward_amount"])
    rabbit.kill()
    print("Rabbit on "+str(card_id)+" caught, added +"+str(config["reward_amount"])+" to reward attribute ("+str(config["reward_id"])+")")
