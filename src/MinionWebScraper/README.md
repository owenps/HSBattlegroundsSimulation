# Minion Web Scraper

## Introduction
Minion Web Scraper (MWS) is a service that extracts the list of HS Battleground Minions from [this source](https://hearthstone.fandom.com/wiki/Battlegrounds/Minion_by_pool). The final output is a `.json` file which follows the following structure.
```
[
    ...
    {
        "name": "Agamaggan, the Great Boar", 
        "miniontype": "Beast", 
        "taverntier": "5 ", 
        "attack": "6 ", 
        "health": "6 ", 
        "description": null
    },
    ...
]
```
You can use http://jsonviewer.stack.hu/ to visualize the output `.json` more elegantly. 

## Execute The Service
Download the relevant packages using `pip`, then navigate to the `src` directory are run the script.
```
pip -r requirements.txt
cd /src
python GetMinions.py
```

## TO DO
* Argparse for download flags
* Fetch descriptions
* Deal with two missing minions (Amalgam, Weaver)
