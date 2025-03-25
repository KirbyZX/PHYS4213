from music21 import corpus, converter, metadata
import sys
from scores import flattenChords, flattenVoices


if __name__ == "__main__":
    
    identifier = sys.argv[1]
    
    # https://www.music21.org/music21docs/about/referenceCorpus.html#referencecorpus

    path = f"../Pickles/{identifier}/{identifier}_"
    score = converter.parse(path + "original.musicxml")

    flattenChords(score)
    print("Chords flattened!")

    flattenVoices(score)
    print("Voices flattened!")

    score.insert(0, metadata.Metadata())
    score.metadata.movementName = "Symphony No. 5 in C minor"
    score.metadata.composer = "Ludwig van Beethoven"

    score.write(fmt="musicxml", fp=f"../Pickles/{identifier}/{identifier}_processed")
    print("Score written!")