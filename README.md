# Quantum annealing and its application to music arrangement

- Thermal fluctuations vs quantum tunnelling
- Quantum vs classical advantage

AQC is broader umbrella, universal, deterministic, can be applied to anything
annealing relaxes the adiabaticity, turns into stochastic, might end up with excited states
heuristic, not deterministic

change in scheduling time
look into minimum energy gap
"fast quenches"

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

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

$N_p * (N_i+1)$ logical variables in the BQM

`scoreWriter.py`
`boundaryDetection.py`
`graphConstructor.py`
`qubo.py`
`embedding.py`

Maximum connectivity of each node is 15 in Pegasus architecture
However, in the Haydn example we require worst-case connectivity of up to 16

$$
f(x)=A\sum_{v \in V}\left(s_v-\sum_{i=1}^{n} x_{v,i}\right)^2+A\sum_{(u,v) \in E}\sum_{i=1}^n x_{u,i}x_{v,i}-C\sum_{v \in V}\sum_{i=1}^n W_vx_{v,i}-D\sum_{(u,v)\in E}W_{uv}\sum_{i=1}^n\sum_{j=1}^n x_{u,i}x_{v,j}-E\sum_{v \in V}\sum_{i=1}^n\theta(S_v-S_{\text{th},i})x_{v,i}
$$
where $\theta$ is the Heaviside step function.

Set $C=D=1$ implies
$$
A>2\max(W)+E
$$

$A=B=E=\max(W)$ edge constraint broken, node constraint broken

Vary A to remove duplicates

Vary B to remove overlaps