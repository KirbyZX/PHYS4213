# Quantum annealing for music arrangement

## Abstract

Quantum annealing is an adiabatic quantum computing technique that has the potential to solve optimisation problems much faster than classical algorithms. This study proposes the novel application of quantum annealing to music arrangement—the adaptation of previously-written compositions—by framing arrangement as an optimisation problem. A musical score is transformed into a graph of vertices and edges, which can then be solved as a graph colouring problem by a quantum computer. The original framework is applied to two scores: Quartet No. 1 in B-flat major, Op. 1, by Joseph Haydn, and Symphony No. 5 in C minor, Op. 67, I. Allegro con brio, by Ludwig van Beethoven. It is shown that a quantum annealer successfully produces arrangements meeting the imposed conditions. Whilst often performing on par with classical algorithms, the quantum method displays optimisation and time advantages at some problem sizes.

## Overview

|Folder|Description|
|---|---|
|`Code`|Python files and Jupyter notebooks used to create the framework|
|`Data`|Solutions returned from both quantum and classical solvers|
|`Examples`|Graphic and audio files of original scores and arrangements|
|`Figures`|Report figures in SVG format|
|`Pickles`|Configuration and data files for the arrangement process|
|`Thesis`|Report and bibliography in LaTeX format