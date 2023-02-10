# pharmer
Python tool to convert UWSOM drug list info into Anki cards

# Input
The drug list must have the following columns:
* `Type` - Also called Drug Family
* `Prototypes` - Also called Prototype Drugs
* `Mechanism of Action`
* `Therapeutic Uses`
* `Serious adverse effects`

If any of these columns are missing or mispelled `pharmer` won't run!

The column header row should also start on row 3. If the header is above or below row 3, `pharmer` won't run!

# Usage
```
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
```

# Example Input
See `mjbs_druglist.xlsx` for a properly formatted file in `tests/`
