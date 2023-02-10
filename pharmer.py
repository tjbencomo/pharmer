"""
pharmer: Python tool to convert UWSOM drug list to info into Anki cards

Usage:
    pharmer [drug list xlsx] [output file prefix] [tag prefix] [sheet name 1] [sheet name 2]

Example:
    python pharmer.py mjbs_druglist.xlsx mjbs_pharm MJBS_2022 'MSK Injuries' 'Rheumatic' 'Topical'

    This takes drug information from mjbs_druglist.xlsx and makes cards for the MSK Injuries, Rheumatic, and
    Topical sheets in the file. The files  mjbs_pharm_MS_Injuries.txt, mjbs_pharm_Rheumatic.txt, and
    mjbs_pharm_Topical.txt will be created. Tags will be MJBS_2022::PHARM_MSK_Injuries, MJBS_2022::PHARM_Rheumatic,
    and MJBS_2022::PHARM_Topical.txt respectively for each file

Usage Notes:
CLI:
    output file prefix = filename for output card .txt files. The sheet name will be suffixed onto the filename
    tag prefix = tagPrefix::PHARM_[sheet name] is the tag the cards will be given for a specific sheet

Specifying a sheet name will create cards for all the drugs in that
sheet. Multiple sheets can be specified
If a sheet name has spaces, enclose the name in single quotes like 'MSK Injuries'
If a cell has the value 'Same as above', you'll need to copy the referenced value into each
cell that says 'Same as above'
Sometimes the Type column is a merged cell with one Type value for several prototype rows. This breaks
pharmer, and you will need to unmerge the Type cell and copy the Type value into each respective cell

WARNING: For merged cells, only one cell will actually have the value in the merged cells.
pharmer will carry through the above value into all empty cells until it reaches another cell
that already has a value. Check the Type column to make sure there aren't any drugs without type
already filled in to prevent erroneous Type labeling.
"""

import os
import sys
import numpy as np
import pandas as pd

def parse_args(args):
    drugfp = args[1]
    outPrefix = args[2]
    tagPrefix = args[3]
    if len(args) < 5:
        raise ValueError("Not enough arguments. Check the usage notes!")
    sheets = []
    for i in range(4, len(args)):
        sheets.append(args[i])
    return drugfp, outPrefix, tagPrefix, sheets

def merge_cards(cards):
    cardDict = {}
    for card in cards:
        if card[0] not in cardDict:
            cardDict[card[0]] = [card[1]]
        else:
            cardDict[card[0]].append(card[1])
    cards = []
    for question in cardDict.keys():
        answers = '<br>'.join(cardDict[question])
        cards.append([question, answers])
    return cards

def isEmpty(cell1, cell2):
    x = not (isinstance(cell1, str) and isinstance(cell2, str))
    # print(cell1)
    return x

def make_cards(df):
    # Remove rows with missing prototype column
    df = df.dropna(subset = ['Prototypes'])
    # print(df.columns)
    # print(df)
    cards = []
    typeCards = [] #list of drugs and their type
    if 'Serious adverse effects' not in df.columns:
        raise ValueError("Serious adverse effects column is missing. May be named differently")
    # Make Type - Prototype cards
    # print("Making type-prototype cards")
    for index, row in df.iterrows():
        if isEmpty(row['Type'], row['Prototypes']):
            continue
        typeCards.append([f"{row['Type']} drugs", row['Prototypes']])
    typeCards = merge_cards(typeCards)
    # Make Prototype - MoA cards
    # print("Making MoA cards")
    for index, row in df.iterrows():
        if isEmpty(row['Type'], row['Mechanism of Action']):
            continue
        cards.append([f"{row['Prototypes'].strip()} MoA", row['Mechanism of Action'].strip()])
    # Make Prototype - Theraputic uses cards
    # print("Making uses cards")
    for index, row in df.iterrows():
        if isEmpty(row['Type'], row['Therapeutic Uses']):
            continue
        cards.append([f"{row['Prototypes'].strip()} uses", row['Therapeutic Uses'].strip()])
    # Make Prototype - Adverse effects cards
    # print("Making AE cards")
    for index, row in df.iterrows():
        if isEmpty(row['Type'], row['Serious adverse effects']):
            continue
        cards.append([f"{row['Prototypes'].strip()} adverse effects", row['Serious adverse effects'].strip()])
    # Remove cards with empty answers - no data for this field
    cards = [card for card in cards if not isinstance(card[1], float)]
    # Anki doesn't accept \n - convert to <br>
    # semicolons in an answer makes anki think there are multiple fields - replace these
    for card in cards:
        card[0] = card[0].replace("\n", "<br>")
        card[1] = card[1].replace("\n", "<br>").replace(";", ".")
    for card in typeCards:
        card[0] = card[0].replace("\n", "<br>")
        card[1] = card[1].replace("\n", "<br>").replace(";", ".")
    cards = typeCards + cards
    return cards

def write_cards_file(cards, sheet, filePrefix, tagPrefix):
    sheet = sheet.replace(' ', '_')
    fn = f"{filePrefix}_{sheet}.txt"
    tag = f"tags:{tagPrefix}::PHARM::{sheet}"
    print(f"Writing file {fn} with tag {tag} with {len(cards)} cards")
    with open(fn, 'w') as f:
        f.write(f"{tag}\n")
        for card in cards:
            # print(f"{card[0]}; {card[1]}")
            f.write(f"{card[0]}; {card[1]}\n")

def print_cards(cards):
    print(f"Printing {len(cards)} cards")
    for card in cards:
        print(card)
    
def process_sheet(fn, sheetName, outputPrefix, tagPrefix):
    df = pd.read_excel(fn, sheet_name = sheetName, skiprows = 2)
    df.Type = pd.Series(df.Type).fillna(method='ffill')
    cards = make_cards(df)
    write_cards_file(cards, sheetName, outputPrefix, tagPrefix)

def main():
    fp, outputPrefix, tagPrefix,  sheets = parse_args(sys.argv)
    # print(f"fp : {fp}")
    # print(f"outputPrefix: {outputPrefix}")
    # print(f"tagPrefix: {tagPrefix}")
    # print(f"sheets: {sheets}")
    for sheet in sheets:
        print(f"Processing sheet {sheet}")
        process_sheet(fp, sheet, outputPrefix, tagPrefix)


if __name__ == '__main__':
    main()

