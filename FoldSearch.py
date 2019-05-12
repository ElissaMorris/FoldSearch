#!/usr/bin/python

import nltk.data
import os
import re
import textwrap

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'fig'])
sentence_splitter = PunktSentenceTokenizer(punkt_param)


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def scan(database, mode):
        RAW = 1
        DESCRIBE = 2
        IGNORE = 3

        descriptive_words = ['pattern', 'patterns', 'tiles', 'mosaic', 'rotational', 'rotate', 'rotates', 'lattice', 'array', 'grid', 'tessellation', 'packing', 'vertex', 'vertices', 'symmetry', 'translation', 'reflection', 'divide', 'division', 'network', 'geometry', 'angle', 'angles', 'profile', 'arrangement', 'behind', 'under', 'over', 'below', 'above', 'forward', 'forwards', 'backward', 'backwards', 'inward', 'inwards', 'outward', 'outwards', ' up', 'upward', 'upwards', 'down', 'downward', 'downwards', 'towards', 'beneath', 'against', 'structure', 'structures', 'its', 'it', 'itself', 'their', 'his', 'her', 'origami', 'leaf', 'leaves', 'seedling', 'seedlings', 'plant', 'plants', 'stem', 'stems', 'flower', 'flowers', 'petal', 'petals', 'wing', 'wings', 'proboscis', 'proboscises', 'tail', 'tails', 'antennae', 'fin', 'fins', 'back', 'web', 'webs', 'muscle', 'muscles', 'tissue', 'scales', 'denticles', 'tendrils', 'shape', 'shapes', 'form', 'forms', 'body', 'size', 'rigid', 'rigidity', 'oblate', 'jointed', 'flat', 'flattened', 'thickness', 'spherical', 'sphere', 'spheres', 'square', 'squares', 'hexagon', 'hexagons', 'hexagonal', 'octagon', 'octagons', 'pentagon', 'pentagons', 'pentagonal', 'triangle', 'triangles', 'triangular', 'cylinder', 'cylindrical', 'cylinders', 'round', 'circle', 'cirlces', 'circular', 'shell', 'ball', 'balls', 'interlock', 'interlocks', 'mesh', 'architecture', 'barb', 'surface', 'ridge', 'movement', 'movements', ' crease', 'flex', 'flexible', 'flexibility']
        stop_words = ("protein","amino acid", "molecule", "polypeptide", "proteins", "DNA", "RNA", "mRNA", "molecules", "molecular", " gene ", " ion ", " ions", "wild type", "wild-type", "bond", "bonds", "bonding", "dimer", "syndrome", "nano", "in-", "de-", "change", "difference", "increase", "decrease", "higher", " lower ", " more ", "genome", "chain", "hairpin", "jelly roll", "chromatid", "chromatids", "chromosome", "chromosomes", "helix", "helices", "helical", "bind", "binding", "domain", "domains", "mR", "sequence", "sequences", "topology", "jelly-roll", "cytoplasm", "periplasm", "cofactor", "co-factor", "reductase", " domain", " protein", "substrate", "kinase", "in vivo", "putative", "lipid", "substrates", "strand", "-strands", "strands", "-strand", "mutant", "septin", "monomer", "antibodies", "antibody", "actin", "tubulin", "tubule", "residue", "thread", "collagen", "procollagen", "VPS", "mitotic", "chromatin", "cells", "cell")

        journals = os.listdir(database)
        os.chdir(database)
        kword_re = chooseword()
        count = 0

        rows,columns=24,40
        cols = int(columns) - 1

        for journal in journals:
                print(color.BOLD+journal+color.END)
                with open(journal, 'r') as j:
                        journal = j.read()
                if not quicksearch(journal, kword_re):
                        print("skipping")
                        continue
                sentences = sentence_splitter.tokenize(journal)

                for sentence in sentences:
                        found = []
                        found_descriptive_words = []
                
		#Raw Search Mode: Returns all passages containing any form of the selected keyword
                        if mode==RAW:
                            thissentences = textwrap.wrap(sentence, width=cols, break_long_words=False)
                            counted=False

                            for kw in kword_re:
                                    found += kw.findall(' '+sentence)
                                    found = [ a.strip().rstrip('.?!"\')]') for a in found ]

                            for thissentence in thissentences:
                                if (found):

                                        for hit in found:
                                            	thissentence = thissentence.replace(hit, color.RED+hit+color.END)
                                        print(thissentence)
                                        if not counted:
                                            counted=True
                                            count += 1
                            if counted:
                                print()

                #Descriptive Search Mode: Returns only passages containing any form of the selected keyword AND the descriptive words
                        if mode==DESCRIBE: 
                            thissentences = textwrap.wrap(sentence, width=cols, break_long_words=False)
                            counted=False

                            for kw in kword_re:
                                    found += kw.findall(' '+sentence)
                                    found = [a.strip().rstrip('.?!"\')]') for a in found]

                            for dsc in descriptive_words:
                                    found_descriptive_words += re.findall('\\b'+dsc+'\\b', sentence)
                            
                            for thissentence in thissentences:
                                if (found) and (found_descriptive_words):

                                        for hit in found:
                                            	thissentence = thissentence.replace(hit, color.RED+hit+color.END)

                                        for dsc in found_descriptive_words:
                                                thissentence = thissentence.replace(dsc, color.DARKCYAN+dsc+color.END)
                                        print(thissentence)
                                        if not counted:
                                            counted=True
                                            count += 1
                            if counted:
                                print()

               #Ignore Search Mode: Returns passages containing any form of the selected keyword AND NOT the stop words
                        if mode==IGNORE:
                            thissentences = textwrap.wrap(sentence, width=cols, break_long_words=False)
                            counted=False

                            for kw in kword_re:
                                found += kw.findall(' '+sentence)
                                found = [ a.strip().rstrip('.?!"\')]') for a in found ]

                            for stop in stop_words:
                                t=sentence.find(stop)       
                                if t!=-1:
                                    found=[]

                            if (found):
                                for thissentence in thissentences:
                                    for hit in found:
                                    	thissentence = thissentence.replace(hit,color.RED+hit+color.END)
                                    print(thissentence)
                                    if not counted:
                                        counted=True
                                        count += 1
                                if counted:
                                         print()

        return count


def chooseword():
        kwords = [('Bend', 'Bending', 'Bends', 'Bended', 'Bent',),
                 ('Coil', 'Coiled', 'Coils', 'Uncoil', 'Uncoiled', 'Uncoils',),
                 ('Compact', 'Compacts', 'Compacted',),
                 ('Curl', 'Curls', 'Curling', 'Curled', 'Uncurl', 'Uncurls', 'Uncurled', 'Curvature'),
                 ('Curve', 'Curves', 'Curved', 'Curving', 'Curvature'),
                 ('Elongate', 'Elongation', 'Elongated', 'Elongates',),
                 ('Expand', 'Expands', 'Expanded', 'Expandable', 'Expanding',),
                 ('Extend', 'Extends', 'Extended', 'Extending',),
                 ('Flex', 'Flexes', 'Flexing', 'Flexed', 'Flexure',),
                 ('Fold', 'Folds', 'Folded', 'Folding', 'Foldable', 'Unfold', 'Unfolds', 'Unfolded', 'Unfolding',),
                 ('Inflate', 'Inflates', 'Inflated', 'Inflating', 'Inflatable',),
                 ('Retract', 'Retracts', 'Retracting', 'Retracted', 'Retractable',),
                 ('Roll', 'Rolled', 'Rolls', 'Rolling', 'Unroll', 'Unrolled', 'Unrolls', 'Unrolling',),
                 ('Shape change', 'Shape-change', 'Shape-changing', 'Shape changing', 'Changes shape', 'Changed shape', 'Changing shape', 'Change shape', 'Change its shape', 'Change their shape',),
                 ('Snap', 'Snaps', 'Snapped', 'Snapping',),
                 ('Stack', 'Stacks', 'Stackable', 'Stacking', 'Stacked',),
                 ('Stretch', 'Stretchable', 'Stretches', 'Stretching', 'Stretched',),
                 ('Tuck', 'Tucks', 'Tucked', 'Tucking',),
                 ('Twist', 'Twists', 'Twisting', 'Twisted',),
                 ('Wrap', 'Wrapping', 'Wraps', 'Wrapped',)]

        print()

        for a in range(0, len(kwords)):
                print(str(a+1)+") "+kwords[a][0])
        choice = int(input("Enter a number: "))
        kword =  [ a.lower() for a in kwords[choice-1] ]
        return [re.compile('[^a-zA-Z0-9-]'+kw+'\\b') for kw in kword ]
    

def quicksearch(journal, kword_re): 
        found = []
        for word in kword_re:
                if (word.search(journal)):
                        return True
        return False


if __name__ == '__main__':
        mode = int(input(("\nSearch Mode:\n1) Raw Search Mode\n2) Descriptive Search Mode\n3) Ignore Search Mode\n> ")))
        while (mode not in range(1,4)): mode = int(input("> "))
        count = scan('TextFiles',mode)
        print("\nFOUND "+color.PURPLE+color.BOLD+str(count)+color.END+" Occurences\n")
