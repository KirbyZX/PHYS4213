import numpy as np
import sys
import pickle
from music21 import stream, note, converter
from entropy import streamEntropy


def extractPhrases(score: stream.Stream, threshold: float, weightings: tuple[float]) -> list[list[stream.Stream]]:
    '''
    Identifies phrases in a score using the LBDM.
    '''
    phraseLists = []
    for part in score.parts:
        print(f"Creating phrases for {part.id} part...")
        boundaries = identifyBoundaries(part, threshold, weightings)
        flat = part.flatten()
        phrases = []
        n = 1
        start = 0
        for b in boundaries:

            phrase = flat.getElementsByOffset(start, b, includeEndBoundary=False).stream()
            start = b
            
            phrase.id = f"{part.id}_{n}"
            n += 1

            phrase.entropy = streamEntropy(phrase)
            phrases.append(phrase)
        
        phraseLists.append(phrases)
        print(f"{len(phrases)} phrases created!")

    return phraseLists

def identifyBoundaries(stream: stream.Stream, threshold: float, weightings: tuple[float], annotate: bool = False) -> list[int]:
    '''
    Calculates the boundary strengths and returns notes above the threshold.
    '''

    noteStream = stream.recurse().getElementsByClass("Note").stream()
    pitchStrengths = np.empty(len(noteStream))
    offsetStrengths = np.empty(len(noteStream))

    for i,n in enumerate(noteStream):
        if i == 0 or i == len(noteStream) - 1:
            pitchStrengths[i] = 0
            offsetStrengths[i] = 0
            continue

        pitchStrengths[i] = n.pitch.ps * (pitchDegree(noteStream[i-1], n) + pitchDegree(n, noteStream[i+1]))
        offsetStrengths[i] = n.getOffsetInHierarchy(noteStream) * (offsetDegree(noteStream[i-1], n, noteStream) + offsetDegree(n, noteStream[i+1], noteStream))
    
    pitchStrengths = normalise(pitchStrengths)
    offsetStrengths = normalise(offsetStrengths)
    
    boundaries = []

    for i,n in enumerate(noteStream):
        total = weightings[0] * pitchStrengths[i] + weightings[1] * offsetStrengths[i]
        n.boundaryStrength = total

        if total >= threshold:
            boundaries.append(n.getOffsetInHierarchy(stream))
            
            if annotate:
                n.addLyric(round(total, 3))

    boundaries.append(stream.duration.quarterLength)

    return boundaries

def hasOverlap(s1: stream.Stream, s2: stream.Stream) -> bool:
    '''
    Returns `True` if two streams have overlapping notes.
    '''

    return start(s1) < end(s2) and start(s2) < end(s1)

def start(s: stream.Stream) -> float:
    return s.flatten().notes.stream().first().offset

def end(s: stream.Stream) -> float:
    return s.flatten().notes.stream().last().offset + s.flatten().notes.stream().last().duration.quarterLength

def normalise(data: np.array) -> np.array:
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def pitchDegree(n1: note.Note, n2: note.Note) -> float:
    return abs(n1.pitch.ps - n2.pitch.ps) / (n1.pitch.ps + n2.pitch.ps)

def offsetDegree(n1: note.Note, n2: note.Note, stream: stream.Stream) -> float:
    return abs(n1.getOffsetInHierarchy(stream) - n2.getOffsetInHierarchy(stream)) / (n1.getOffsetInHierarchy(stream) + n2.getOffsetInHierarchy(stream))


if __name__ == "__main__":

    identifier = sys.argv[1]
    path = f"../Pickles/{identifier}/{identifier}_"

    score = converter.parse(path + "score.musicxml")

    phrases = extractPhrases(score, 0.3, (0.33, 0.66))
    pickle.dump(phrases, open(path + "phrases.pkl", "wb"))