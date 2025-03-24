import numpy as np
import pandas as pd
import sys
import pickle
from music21 import stream, converter
from entropy import streamEntropy


def extractPhrases(score: stream.Stream, weights: tuple[float]) -> list[list[stream.Stream]]:
    '''
    Extracts phrases from a score using the LBDM.
    '''

    phraseLists = []

    for part in score.parts:
        print(f"Creating phrases for {part.id} part...")

        df, _ = calculateStrengths(part, weights)
        flat = part.flatten()
        phrases = []
        n = 1
        start = 0
        for b in df.query("IsBoundary")["Offset"]:

            phrase = flat.getElementsByOffset(start, b, includeEndBoundary=False).stream()
            start = b
            
            phrase.id = f"{part.id}_{n}"
            n += 1

            phrase.entropy = streamEntropy(phrase)
            phrases.append(phrase)
        
        phraseLists.append(phrases)
        print(f"{len(phrases)} phrases created!")

    return phraseLists

def calculateStrengths(stream: stream.Stream, weights: tuple[float]) -> tuple[pd.DataFrame, float]:
    '''
    Returns a table of calculate boundary strengths.
    '''

    df = pd.DataFrame()
    noteStream = stream.flatten().notes

    for n in noteStream:

        offset = n.offset
        # If chord use the top note
        if hasattr(n, "notes"):
            n = n.notes[-1]

        pitch = n.pitch.ps
        
        new_row = pd.DataFrame({
            "Pitch": [pitch],
            "Offset": [offset]
            })

        df = pd.concat([df, new_row])

    degreeOfChange = lambda x1, x2 : abs(x1 - x2) / (x1 + x2)
    strength = lambda x1, x2, x3 : x2 * (degreeOfChange(x1, x2) + degreeOfChange(x2, x3))
    normalise = lambda data : (data - np.min(data)) / (np.max(data) - np.min(data))

    df["Pitch strength"] = normalise(np.array(
        [0] +
        [strength(df["Pitch"].iloc[i-1], df["Pitch"].iloc[i], df["Pitch"].iloc[i+1]) for i in range(1, len(df["Pitch"])-1)] +
        [0]))
    
    df["Offset strength"] = normalise(np.array(
        [0] +
        [strength(df["Offset"].iloc[i-1], df["Offset"].iloc[i], df["Offset"].iloc[i+1]) for i in range(1, len(df["Offset"])-1)] +
        [0]))

    df.eval("Strength = @weights[0]*`Pitch strength` + @weights[1]*`Offset strength`", inplace=True)

    threshold = df["Strength"].max() / 4
    df.eval("IsBoundary = Strength >= @threshold", inplace=True)

    return df, threshold


def hasOverlap(s1: stream.Stream, s2: stream.Stream) -> bool:
    '''
    Returns `True` if two streams have overlapping notes.
    '''

    start = lambda s : s.flatten().notes.stream().first().offset
    end = lambda s : s.flatten().notes.stream().last().offset + s.flatten().notes.stream().last().duration.quarterLength

    return start(s1) < end(s2) and start(s2) < end(s1)


if __name__ == "__main__":

    identifier = sys.argv[1]

    path = f"../Pickles/{identifier}/{identifier}_"

    score = converter.parse(path + "score.musicxml")

    phrases = extractPhrases(score, (0.33, 0.66))
    pickle.dump(phrases, open(path + "phrases.pkl", "wb"))