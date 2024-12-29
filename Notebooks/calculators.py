from music21 import stream, note
import math
import numpy as np

def noteDistribution(stream: stream.Stream) -> tuple:
    '''
    Returns the distribution of notes in a stream as a tuple of two dictionaries.
    '''

    pitchCount = {}
    durationCount = {}

    for n in stream.recurse().getElementsByClass("Note"):

        if n.name not in pitchCount:
            pitchCount[n.name] = 1
        else:
            pitchCount[n.name] += 1
    
        if n.duration.quarterLength not in durationCount:
            durationCount[n.duration.quarterLength] = 1
        else:
            durationCount[n.duration.quarterLength] += 1

    return pitchCount, durationCount


def noteEntropy(note: note.Note, distribution: tuple) -> float:
    '''
    Calculates the entropy of a note based on the distribution of notes in a stream.
    '''

    pitch = note.name
    duration = note.duration.quarterLength

    pitchCount = distribution[0]
    durationCount = distribution[1]
    totalNotes = sum(pitchCount.values())

    pitchEntropy = - (pitchCount[pitch] / totalNotes) * math.log2(pitchCount[pitch] / totalNotes)
    durationEntropy = - (durationCount[duration] / totalNotes) * math.log2(durationCount[duration] / totalNotes)

    return pitchEntropy + durationEntropy


def streamEntropy(stream: stream.Stream, distribution: tuple) -> float:
    return sum([noteEntropy(n, distribution) for n in stream.recurse().getElementsByClass("Note")])
