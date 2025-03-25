from music21 import stream, clef, chord, instrument, midi, analysis
import pandas as pd
from plots import extractChosen


def plotArrangement(sample: dict, score: stream.Score, phrases: pd.DataFrame, instruments: dict, midiPath: str = None) -> stream.Score:
    '''
    Create an arrangement score from a sample.
    '''

    scoreParts = {p.id: p.flatten() for p in score.parts}
    arrParts = {i: stream.Part() for i in instruments}

    for i in arrParts:
        arrParts[i].append(getattr(instrument, i)())
        arrParts[i].append(getattr(clef, instruments[i]["clef"])())

    chosen = extractChosen(sample) # Index : Assignment

    for index in chosen:
        
        flat = scoreParts[index[0]] # Original part
        phrase = flat.getElementsByOffset(phrases.loc[index, "Start"], phrases.loc[index, "End"], includeEndBoundary=False).stream()

        # Get lowest note of assigned instrument
        inst = getattr(instrument, chosen[index])()
        lowestNote = inst.lowestNote

        # Check ambitus
        p = analysis.discrete.Ambitus()
        pitchMin, _ = p.getPitchSpan(phrase)
            
        # Shift octaves to be in range
        while pitchMin.ps < lowestNote.ps or pitchMin.octave - lowestNote.octave > 1:
            shiftOctave(phrase, 1 if pitchMin.ps < lowestNote.ps else -1)

        # Merge with new part
        arrParts[chosen[index]].mergeElements(phrase) 

    arrangement = stream.Score(arrParts.values())
    arrangement.show()

    if midiPath: saveToMidi(arrangement, midiPath)

    return arrangement

def saveToMidi(s: stream.Stream, filepath: str) -> None:
    '''
    Export a stream to a MIDI file.
    '''

    mf = midi.translate.streamToMidiFile(s)
    mf.open(filepath, 'wb')
    mf.write()
    mf.close()

def shiftOctave(s: stream.Stream, o: int):
    '''
    Shift the octave of all notes in a stream.
    '''

    for el in s.recurse().notes:
        el.octave += o

def flattenVoices(score: stream.Score):
    '''
    Remove all voices except one for each part.
    '''
    
    for part in score.parts:
        v = part.voicesToParts().parts[0]

        oldClef = part.flatten().getElementsByClass(clef.Clef)[0]
        newClef = v.flatten().getElementsByClass(clef.Clef)[0]

        v.replace(newClef, oldClef, recurse=True)
        score.replace(part, v)

def flattenChords(stream: stream.Stream):
    '''
    Replace all chords with their highest note.
    '''

    for el in stream.recurse().notes:
        if isinstance(el, chord.Chord):
            # Replace the chord with the top note
            stream.replace(el, el.notes[-1], recurse=True)