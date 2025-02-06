from music21 import stream
import math


def streamEntropy(stream: stream.Stream) -> float:
    '''
    Calculates the entropy of a stream.
    '''
    pitchCount, durationCount = noteDistribution(stream)
    
    pitchEntropy = -sum([x * math.log2(x) for x in pitchCount.values()])
    durationEntropy = -sum([x * math.log2(x) for x in durationCount.values()])
     
    return pitchEntropy + durationEntropy

def noteDistribution(stream: stream.Stream) -> tuple[dict, dict]:
    '''
    Calculates the pitch and duration distributions of a stream.
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