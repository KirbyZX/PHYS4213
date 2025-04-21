# Quantum annealing for music arrangement

## Abstract

Quantum annealing is an adiabatic quantum computing technique that has the potential to solve optimisation problems much faster than classical algorithms. This study proposes the novel application of quantum annealing to music arrangement—the adaptation of previously-written compositions—by framing arrangement as an optimisation problem. A musical score is transformed into a graph of vertices and edges, which can then be solved as a graph colouring problem by a quantum computer. The original framework is applied to two scores: Quartet No. 1 in B-flat major, Op. 1, by Joseph Haydn, and Symphony No. 5 in C minor, Op. 67, I. Allegro con brio, by Ludwig van Beethoven. It is shown that a quantum annealer successfully produces arrangements meeting the imposed conditions. Whilst often performing on par with classical algorithms, the quantum method displays optimisation and time advantages at some problem sizes.

## Overview

`scoreWriter.py`
`boundaryDetection.py`
`graphConstructor.py`
`qubo.py`
`embedding.py`

### TODO

- [x] Rewrite quantum annealing
- [x] Rewrite music arrangement
- [x] Write results
- [x] Write conclusion
- [x] Write introduction
- [x] Check formatting of plots (SVG, dpi=600, 4:3, text, colours)
- [x] Write appendices (tables of arrangement instruments, scores, problem graphs)
- [x] Write abstract 
- [x] Write scientific summary
- [x] Check references
- [x] Rename repository
- [ ] Tidy repository
