from music21 import corpus
import sys


if __name__ == "__main__":
    
    identifier = sys.argv[1]
    
    # https://www.music21.org/music21docs/about/referenceCorpus.html#referencecorpus
    score = corpus.parse("haydn/opus1no1/movement1.mxl")
    score.write(fmt="musicxml", fp=f"../Pickles/{identifier}/{identifier}_score")
    score.show()