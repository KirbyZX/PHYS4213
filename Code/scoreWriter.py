from music21 import corpus, converter, metadata
import sys


if __name__ == "__main__":
    
    identifier = sys.argv[1]
    
    # https://www.music21.org/music21docs/about/referenceCorpus.html#referencecorpus
    score = converter.parse("../beethoven.mxl")
    score.insert(0, metadata.Metadata())
    score.metadata.movementName = "Symphony No. 5 in C minor"
    score.metadata.composer = "Ludwig van Beethoven"
    score.write(fmt="musicxml", fp=f"../Pickles/{identifier}/{identifier}_score")
    score.show()