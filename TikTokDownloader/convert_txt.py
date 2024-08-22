import json
import pandas as pd
import numpy as np

def create_text(spreadsheet, category):
    df = pd.read_excel(spreadsheet)
    df.url.to_csv(f'links_{category}.txt', header=None, index=None, sep='\n', mode='a')
def convert_text(category):
    links_status = {}
    with open(f'links_{category}.txt') as file:
        for line in file:
            links_status[line.strip("\n")] = 'unvisited'

    with open(f'links_{category}.json', 'w') as file:
        file.write(json.dumps(links_status))
