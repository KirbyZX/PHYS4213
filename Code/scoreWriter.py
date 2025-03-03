from music21 import corpus, metadata
import sys


if __name__ == "__main__":
    
    identifier = sys.argv[1]
    
    # https://www.music21.org/music21docs/about/referenceCorpus.html#referencecorpus
    score = corpus.parse("haydn/opus1no1/movement1.mxl")
    score.insert(0, metadata.Metadata())
    score.metadata.movementName = "Quartet No. 1 in B♭ major"
    score.metadata.composer = "Joseph Haydn"
    score.write(fmt="musicxml", fp=f"../Pickles/{identifier}/{identifier}_score")
    score.show()