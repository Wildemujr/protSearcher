#!/usr/bin/env python3

from pprint import pprint as pp



class ParseRcsbJson:
    """
    A set of method determined on isolating specific attributes from RCSB JSON
    output using the python requests library.
    """

    def __init__(self, json_output, variable_list):
        self.json_output = json_output
        self.variable_list = variable_list


    def checkKey(self, test_dict, key):
        try:
            value = test_dict[key]
            return True
        except KeyError:
            return False


    def extractId(self):
        id_l = []
        id_tag = "entry"
        if id_tag in self.json_output.keys() and "id" in self.json_output[id_tag]:
            id_l.append( ("PDB_ID", self.json_output[id_tag]["id"]) )
        id_l.append( ("PDB_ID", "NA") )
        
        yield id_l[0]


    def extractPh(self):
        ph_l = []
        ph_tag = "exptl_crystal_grow"
        if ph_tag in self.json_output.keys() and "p_h" in self.json_output[ph_tag][0]:
            ph_l.append( ("pH", self.json_output[ph_tag][0]["p_h"]) )
        ph_l.append( ("pH", "NA") )

        yield ph_l[0]


    def extractTemp(self):
        temp_l = []
        temp_tag = "exptl_crystal_grow"
        if temp_tag in self.json_output.keys() and "temp" in self.json_output[temp_tag][0]:
            temp_l.append( ("Temperature", self.json_output[temp_tag][0]["temp"]) )
        temp_l.append( ("Temperature", "NA") )

        yield temp_l[0]


    def extractRcsbEntryInfo(self):
        rcsb_l = []
        rcsb_tag = "rcsb_entry_info"
        rcsb_attr_list = [
                "deposited_atom_count", 
                "deposited_modeled_polymer_monomer_count",
                "deposited_nonpolymer_entity_instance_count",
                "disulfide_bond_count",
                "molecular_weight",
                "nonpolymer_bound_components"]

        for rcsb_attr in rcsb_attr_list:
            if rcsb_tag in self.json_output.keys() and self.checkKey(self.json_output[rcsb_tag], rcsb_attr):
                if isinstance(self.json_output[rcsb_tag][f"{rcsb_attr}"], list):
                    rcsb_l.append( (f"{rcsb_attr}", ", ".join(self.json_output[rcsb_tag][f"{rcsb_attr}"])) )
                else:
                    rcsb_l.append( (f"{rcsb_attr}", self.json_output[rcsb_tag][f"{rcsb_attr}"]) )
            else:
                rcsb_l.append( (f"{rcsb_attr}", "NA") )

        yield rcsb_l


    def extractPubMedRecord(self):
        pubmed_tag = "rcsb_primary_citation"
        if pubmed_tag in self.json_output.keys() and self.checkKey(self.json_output[pubmed_tag], "pdbx_database_id_pub_med"):
            yield  ( ("pdbx_database_id_pub_med", self.json_output[pubmed_tag]["pdbx_database_id_pub_med"]) )
        yield ( ("pdbx_database_id_pub_med", "NA") )


    def extractRfree(self):
        rFree_l = []
        rFree_tag = "refine"
        if rFree_tag in self.json_output.keys() and "ls_rfactor_rfree" in self.json_output[rFree_tag][0]:
            rFree_l.append( ("rfactor_rfree", self.json_output[rFree_tag][0]["ls_rfactor_rfree"]) )
        rFree_l.append( ("rfactor_rfree", "NA") )

        yield rFree_l[0]


    def extractRobs(self):
        rObs_l = []
        rObs_tag = "refine"
        if rObs_tag in self.json_output.keys() and "ls_rfactor_obs" in self.json_output[rObs_tag][0]:
            rObs_l.append( ("rfactor_obs", self.json_output[rObs_tag][0]["ls_rfactor_obs"]) )
        rObs_l.append( ("rfactor_obs", "NA") )

        yield rObs_l[0]


    def extractPdbxDetails(self):
        pdbxDeets_l = []
        pdbxDeets_tag = "exptl_crystal_grow"
        if pdbxDeets_tag in self.json_output.keys() and "pdbx_details" in self.json_output[pdbxDeets_tag][0]:
            pdbxDeets_l.append( ("pdbx_details", "".join(self.json_output[pdbxDeets_tag][0]["pdbx_details"])) )
        pdbxDeets_l.append( ("pdbx_details", "NA") )

        yield pdbxDeets_l[0]


    def printJson(self):
        pp(self.json_output)

    def printVarList(self):
        pp(self.variable_list)

