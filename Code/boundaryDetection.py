import numpy as np
import pandas as pd
import sys
import pickle
from music21 import stream, converter
from entropy import streamEntropy


def extractPhrases(score: stream.Score, weights: tuple[float]) -> pd.DataFrame:
    '''
    Extracts phrases from a score using the LBDM.
    '''
    
    phrases = pd.DataFrame()

    for part in score.parts:
        print(f"Creating phrases for {part.id} part...")

        df, _ = calculateStrengths(part, weights)
        flat = part.flatten()

        boundaries = df.query("IsBoundary")["Offset"]

        ids = [f"{part.id}_{n+1}" for n in range(len(boundaries))]
        starts = list(boundaries)
        ends = starts[1:] + [part.duration.quarterLength]
        entropies = [streamEntropy(flat.getElementsByOffset(s, e, includeEndBoundary=False).stream()) for s,e in zip(starts, ends)]

        index = pd.MultiIndex.from_product([[part.id], range(1, len(boundaries) + 1)], names=["Instrument","No"])
        partPhrases = pd.DataFrame({
            "ID": ids,
            "Start": starts,
            "End": ends,
            "Entropy": entropies
        }, index=index)
        
        phrases = pd.concat([phrases, partPhrases])
        print(f"{len(phrases)} phrases created!")

    return phrases

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


if __name__ == "__main__":

    identifier = sys.argv[1]

    path = f"../Pickles/{identifier}/{identifier}_"

    score = converter.parse(path + "score.musicxml")

    phrases = extractPhrases(score, (0.33, 0.66))
    pickle.dump(phrases, open(path + "phrases.pkl", "wb"))