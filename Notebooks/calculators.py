from music21 import stream, note
import math
import numpy as np

def noteDistribution(stream: stream.Stream) -> tuple[dict, dict]:
    '''
    Returns the distribution of notes in a stream as a tuple of two dictionaries.
    '''

    pitchCount = {}
    durationCount = {} # TODO: Change to IOI

    for n in stream.recurse().getElementsByClass("Note"):

        if n.name not in pitchCount:
            pitchCount[n.name] = 1
        else:
            pitchCount[n.name] += 1
    
        if n.duration.quarterLength not in durationCount:
            durationCount[n.duration.quarterLength] = 1
        else:
            durationCount[n.duration.quarterLength] += 1

    pitchDistribution = {k: v / sum(pitchCount.values()) for k, v in pitchCount.items()}
    durationDistribution = {k: v / sum(durationCount.values()) for k, v in durationCount.items()}

    return pitchDistribution, durationDistribution


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


def streamEntropy(stream: stream.Stream) -> float:

    pitchCount, durationCount = noteDistribution(stream)
    
    pitchEntropy = -sum([x * math.log2(x) for x in pitchCount.values()])
    durationEntropy = -sum([x * math.log2(x) for x in durationCount.values()])
     
    return pitchEntropy + durationEntropy