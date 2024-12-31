# Towards Automated Music Arrangement via Quantum Annealing

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```
Quantum Instrument Rearrangement By Expression (Entropy?) Evaluation

## Classical methods

Classical methods of producing music normally revolves around expansion from a simple melody line or chord progression.
Extra parts can be added in line with the desired style to create an arrangement of any size.

## Digital interpretation

- Using MusicXML over MIDI as it is more useful when interpreting arrangements to a human-readable format
- Retains score information and formatting
- More useful libraries e.g. `music21`


## Segmentation

Separation of digital music files into individual parts.

## Phrase identification

Identifying distinct musical phrases that must either be played in their entirety or not at all.

## Variable definition

Defining binary variables based on the identified phrases.
Weight phrases by musical entropy?

## Clause definition

Defining satisfiability clauses constructed from the binary variables.

## Constraints

Implementation of constraints on the binary variables.

Playability rules (Huang et al 2012)
- Pitch range
- Duration
- Polyphony
- Physical pitch/overlapping constraint

## Solve

Solve as a maximum independent set (MIS) problem.

## MIDI wrapper

- Take MIDI track
- Associate into phrase objects
- Number phrases via dictionary
- Create graph edges from overlap
- Solve
- Rearrange node solutions back together