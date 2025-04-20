# Quantum annealing for music arrangement

AQC is broader umbrella, universal, deterministic, can be applied to anything
annealing relaxes the adiabaticity, turns into stochastic, might end up with excited states
heuristic, not deterministic

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```


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

### TODO

- [x] Rewrite quantum annealing
- [x] Rewrite music arrangement
- [x] Write results
- [x] Write conclusion
- [x] Write introduction
- [x] Check formatting of plots (SVG, dpi=600, 4:3, text, colours)
- [x] Write appendices (tables of arrangement instruments, scores, problem graphs)
- [ ] Write abstract 
- [ ] Write scientific summary
- [ ] Check references
- [x] Rename repository
- [ ] Tidy repository
