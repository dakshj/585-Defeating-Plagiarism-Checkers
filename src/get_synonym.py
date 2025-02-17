import os
import pickle
import nltk

from nltk.corpus import wordnet as wn

INDEX_PATH = "./../datasets/index.sense"
MANUAL_MAP = "./../datasets/manual_map.txt"
ALGO_MAP = "./../datasets/algorithmic_map.txt"
FILE_SENSE_INDEX = './../datasets/sense_index.pkl'
FILE_NOAD_TO_WN = './../datasets/noad_to_wn.pkl'


class Synonym:

    def __init__(self):
        nltk.download('wordnet')
        sense_dict = {}
        noad_to_wn = {}

        if os.path.isfile(FILE_SENSE_INDEX) and os.path.isfile(FILE_NOAD_TO_WN):
            with open(FILE_SENSE_INDEX, 'rb') as f:
                sense_dict = pickle.load(f)
            with open(FILE_NOAD_TO_WN, 'rb') as f:
                noad_to_wn = pickle.load(f)
        else:
            with open(INDEX_PATH, 'r') as f:
                for line in f:
                    lst = line.split()
                    sense_dict[lst[0]] = lst[1]

            with open(MANUAL_MAP, 'r') as f:
                for line in f:
                    lst = line.split()
                    noad_to_wn[lst[0]] = lst[1].split(',')

            with open(ALGO_MAP, 'r') as f:
                for line in f:
                    lst = line.split()
                    noad_to_wn[lst[0]] = lst[1].split(',')

            with open('sense_index.pkl', 'wb') as f:
                pickle.dump(sense_dict, f, pickle.HIGHEST_PROTOCOL)
            with open('noad_to_wn.pkl', 'wb') as f:
                pickle.dump(noad_to_wn, f, pickle.HIGHEST_PROTOCOL)

        self.sense_dict = sense_dict
        self.noad_to_wn = noad_to_wn

    @staticmethod
    def get_synsets(offsets):
        syns = list(wn.all_synsets())
        offsets_list = [(s.offset(), s) for s in syns]
        offsets_dict = dict(offsets_list)
        return map(lambda off: offsets_dict[off], offsets)

    def get_synonym(self, sense):

        if sense not in self.noad_to_wn:
            return []

        wn_senses = self.noad_to_wn[sense]
        offsets = []
        for wn_sense in wn_senses:
            if ';' not in wn_sense and wn_sense in self.sense_dict:
                offsets.append(self.sense_dict[wn_sense])
            else:
                continue
        ss = Synonym.get_synsets(map(lambda off: int(off), offsets))

        # for s in ss:
        #     print(s)
        #     print(s.pos())
        #     print(s.definition())
        #     print(s.lemma_names())
        #     print()

        return map(lambda sst: (sst.pos(), sst.lemma_names()), ss)
