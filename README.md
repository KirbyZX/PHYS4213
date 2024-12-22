# Towards Automated Music Arrangement via Quantum Annealing

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

## Segmentation

Separation of digital music files into individual parts.

## Phrase identification

Identifying distinct musical phrases that must either be played in their entirety or not at all.

## Variable definition

Defining binary variables based on the identified phrases.

## Clause definition

Defining satisfiability clauses constructed from the binary variables.

## Constraints

Implementation of constraints on the binary variables.

## Solve

Solve as a maximum independent set (MIS) problem.