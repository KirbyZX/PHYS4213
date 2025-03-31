import numpy as np
import pandas as pd
import sys
from music21 import stream, converter
from entropy import streamEntropy


def extractPhrases(score: stream.Score, threshold: float, weights: tuple[float]) -> pd.DataFrame:
    '''
    Extracts phrases from a score using the LBDM.
    '''
    
    phrases = pd.DataFrame()

    for part in score.parts:
        print(f"Creating phrases for {part.id} part...")

        df, _ = calculateStrengths(part, threshold, weights)
        print(df)
        flat = part.flatten()
        lastNote = flat.notes.stream().last()

        boundaries = df.query("IsBoundary")["Offset"]

        ids = [f"{part.id}_{n+1}" for n in range(len(boundaries))]
        starts = list(boundaries)
        ends = starts[1:] + [lastNote.offset + lastNote.duration.quarterLength]
        entropies = [streamEntropy(flat.getElementsByOffset(s, e, includeEndBoundary=False).stream()) for s,e in zip(starts, ends)]

        index = pd.MultiIndex.from_product([[part.id], range(1, len(boundaries) + 1)], names=["Instrument","No"])
        partPhrases = pd.DataFrame({
            "ID": ids,
            "Start": starts,
            "End": ends,
            "Entropy": entropies
        }, index=index)
        
        print(f"{len(partPhrases)} phrases created!")
        phrases = pd.concat([phrases, partPhrases])

    print(f"{len(phrases)} total phrases created!")

    return phrases

def calculateStrengths(stream: stream.Stream, threshold: float, weights: tuple[float]) -> tuple[pd.DataFrame, float]:
    '''
    Returns a table of calculated boundary strengths.
    '''

    df = pd.DataFrame()
    noteStream = stream.flatten().notes

    for n in noteStream:

        offset = n.offset
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
    # Set first and last notes as boundaries
    df.iat[0, 4] = 1
    df.iat[len(df)-1, 4] = 1

    df.eval("IsBoundary = Strength >= @threshold", inplace=True)

    return df, threshold


if __name__ == "__main__":

    identifier = sys.argv[1]
    threshold = float(sys.argv[2])

    path = f"../Pickles/{identifier}/{identifier}_"

    score = converter.parse(path + "score.musicxml")

    phrases = extractPhrases(score, threshold, (0.33, 0.66))
    phrases.to_csv(path + "phrases.csv")