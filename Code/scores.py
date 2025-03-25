from music21 import stream, clef, chord


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