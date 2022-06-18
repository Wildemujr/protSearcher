#!/usr/bin/env python3

import re
import requests
import pandas as pd
import json
import sys
from pprint import pprint as pp
from collections import defaultdict
import modules 
import time

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also




def req_by_id(server, request, content_type):
    r = requests.get(f"{server}{request}", headers={"Content-Type": content_type})
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    if content_type == "application/json":
        return r.json() #.content.decode('utf-8')
    else:
        return r.text


def read_pdbID_file(file_na):
    ids_in_file = []
    with open(f"{file_na}", "r") as fh:
        for line in fh.readlines():
            ids_in_file.append(line.rstrip())
    return ids_in_file


def mergeDictionary(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = [value , dict_1[key]]
   return dict_3


def main():    
    
    pdb_identifiers = read_pdbID_file(sys.argv[1])
    test_identifiers = pdb_identifiers[0:1001]
    server =  "https://data.rcsb.org/rest/v1/core/entry/"


    varsList = ["entry", "exptl", "exptl_crystal", "exptl_crystal_grow","refine"]
    # crystalVariableDict = [(var,0) for var in varsList]
    crystalVariableList = []
    d = defaultdict(list)
 
    
 
    # print(crystalVariableDict)
    
    # for identifier in req:
    #     cont_type = "application/json"
    #     test = req_by_id(server, identifier, cont_type)
    #     l = CheckVariables(varsList, test)
        
    #     print(l)
    #     crystalVariableList.append(l[0])
    #     crystalVariableList.append(l[1])
    #     # print(l[0])
    #     print("\n\n")
    
    # for entry, dat in crystalVariableList:
    #     d[entry].append(dat)
    
    # pp(d)

    master_df = pd.DataFrame(
        columns = ["PDB_ID", "pH", "rfactor_rfree", "rfactor_obs", "pdbx_details"]
    )


    for identifier in test_identifiers:
        cont_type = "application/json"
        test = req_by_id(server, identifier, cont_type)
        jsonParser = modules.ParseRcsbJson(test, varsList)
        
        id = next(jsonParser.extractId())
        ph = next(jsonParser.extractPh())
        rObs = next(jsonParser.extractRobs())
        rFree = next(jsonParser.extractRfree())
        pdbxDeets = next(jsonParser.extractPdbxDetails())
        temperature = next(jsonParser.extractTemp())
        rscbDetails = next(jsonParser.extractRcsbEntryInfo())    
        pubmedID = next(jsonParser.extractPubMedRecord())
    
        # print(rscbDetails[1][0], rscbDetails[1][1])
        # print(next(id))
        # l = CheckVariables(varsList, test)
        # jsonParser.printJson()
        # print("\n\n\n")
        # jsonParser.printVarList()
        # print("\n\n\n")
        # print(id)
        # print("\n\n\n")
        # print(ph)
        # print("\n\n\n")
        # print(pdbxDeets)
        data_aggregated = {
             id[0] : id[1],
             ph[0] : ph[1],
             rFree[0] : rFree[1],
             rObs[0] : rObs[1],
             pdbxDeets[0] : pdbxDeets[1],
             "Temperature" : temperature[1],
             "TotalAtomCount" : rscbDetails[0][1],
             "TotalResidueCount" : rscbDetails[1][1],
             rscbDetails[2][0] : rscbDetails[2][1],
             rscbDetails[3][0] : rscbDetails[3][1],
             rscbDetails[4][0] : rscbDetails[4][1],
             rscbDetails[5][0] : rscbDetails[5][1],
             pubmedID[0] : pubmedID[1]
         } 

        df = pd.DataFrame(data_aggregated, index = [1])
        master_df = pd.concat([master_df, df])
    
    master_df = master_df.reset_index(drop=True)
    
    # pd.set_option("display.max_rows", None, "display.max_columns", None)    
    print(master_df)
    master_df.to_excel("test.xlsx", sheet_name="Sheet 1")
    # master_df.to_csv("test.csv")







    
    # cont_type = "application/json"
    # test = req_by_id(server, pdb_identifiers[0], cont_type)
    # # pp(test)
    
    # jsonParser = modules.ParseRcsbJson(test, varsList)
    # jsonParser.printJson()
    
    # print("\n\n\n")
    
    # # jsonParser.printVarList()
    
    # id = jsonParser.extractId()
    # # print(id)
    
    # ph = jsonParser.extractPh()
    # # print(ph)
    
    # rObs = jsonParser.extractRobs()
    # rFree = jsonParser.extractRfree()
    
    # pdbxDeets = jsonParser.extractPdbxDetails()
    
    # print("\n\n")
    
    # # print(pdbxDeets)
    
    # # PdbxDetails()
    
    # data_aggregated = {
    #     id[0] : id[1],
    #     ph[0] : ph[1],
    #     rFree[0] : rFree[1],
    #     rObs[0] : rObs[1],
    #     pdbxDeets[0] : pdbxDeets[1]
    # }

    # df = pd.DataFrame(data_aggregated, index = [1])
    
    
    # print(df)
    
if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))