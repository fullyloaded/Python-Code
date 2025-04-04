# Python-Code
Networked Power Field: A Case Study on the Dissolution of the Soviet Union (1991)

A political system can be conceptualized as a dynamic network, where nodes represent key actors (e.g., national leaders, military forces, external powers), and edges signify the interactions or relationships between them (e.g., alliances, conflicts, resource exchanges). In the case of the Soviet Union's dissolution in 1991, the interplay of these actors formed a network of power transitions. This analysis employs a networked power field, nonlinear dynamics, and self-organized criticality (SOC) to explain the complex process of the Soviet collapse, while integrating the factor of Soviet financial bankruptcy to enhance the model's realism.
 Modeling Approach
The traditional field 𝜙(𝑥,𝑡) (field strength in space and time) is extended to a networked power field 𝜙ᵢ(𝑡), where node 𝑖 represents an actor and 𝑡 denotes historical evolution. The dynamics are governed by the following equation:
∂ₜ²𝜙ᵢ + 𝛾∂ₜ𝜙ᵢ + 𝜆𝜙ᵢ(𝜙ᵢ² − 𝑎²) = ∑ⱼ 𝐴ᵢⱼ(𝜙ⱼ − 𝜙ᵢ) + 𝐹ᵢ(𝑡)
- 𝐴ᵢⱼ: Adjacency matrix, reflecting the power influence between nodes 𝑖 and 𝑗 (positive for cooperation, negative for opposition).
- ∑ⱼ 𝐴ᵢⱼ(𝜙ⱼ − 𝜙ᵢ): Network diffusion term, simulating the transmission and competition of power among actors.
- 𝐹ᵢ(𝑡): External forcing term, capturing time-dependent influences such as financial bankruptcy.
 1. Complex Systems Perspective of the Networked Power Field
This model views the political system as a dynamic network, with nodes as actors and edges as their relationships, making it well-suited to analyze the Soviet Union's dissolution in 1991. The collapse resulted from the interactions of multiple internal and external actors, ultimately leading to the breakdown and reconfiguration of the power field.
 Actors and Network Nodes
Key political actors in the Soviet dissolution process are identified as follows:
Node 𝑖 Role
 1 Soviet Government (Gorbachev)
 2 Russian Federation (Yeltsin)
 3 Eastern European States (Poland, Czech Republic, etc.)
 4 United States (Cold War rival)
 5 Soviet Military (hardliners)
 6 Communist Party Conservatives (1991 coup plotters)
These six actors encompass the critical roles in the process. Soviet financial bankruptcy is introduced as an external shock 𝐹ᵢ(𝑡) or noise term 𝜂ᵢ(𝑡), significantly impacting the power field 𝜙ᵢ(𝑡) of all actors.
 Adjusting the Adjacency Matrix 𝐴ᵢⱼ
To account for financial bankruptcy, the adjacency matrix is adjusted to reflect how economic pressure weakened the Soviet government (Node 1) and amplified the influence of other actors. For example:
 𝐴₁₁ (internal stability of the Soviet government) shifts from 0 to −0.2 due to financial bankruptcy eroding cohesion.
 𝐴₁₄ (U.S. pressure on the Soviet government) increases from −0.7 to −0.9, as the U.S. exacerbated the fiscal crisis through sanctions and the arms race.
 𝐴₁₂ (Soviet government vs. Russian Federation) remains at −0.6, but the Russian Federation benefits from the central authority's decline.
Adjusted adjacency matrix:
𝐴 = 
[
−0.2  −0.6  −0.5  −0.9   0.3  −0.4
−0.6   0     0.2   0.4   0.1  −0.2
−0.5   0.2   0     0.5  −0.3  −0.1
−0.9   0.4   0.5   0     0.2  −0.6
 0.3   0.1  −0.3   0.2   0    −0.5
−0.4  −0.2  −0.1  −0.6  −0.5   0
]
 Dynamics Equation with Financial Bankruptcy
The dynamics equation effectively describes the evolution of the power field. Financial bankruptcy is incorporated as 𝐹₁(𝑡) (external force acting on the Soviet government):
𝐹₁(𝑡) = −𝑘 ⋅ 𝐸(𝑡)
where 𝐸(𝑡) is a function of growing fiscal pressure over time (e.g., falling oil prices and excessive military spending in the late 1980s), and 𝑘 is a positive coefficient representing the negative impact of bankruptcy on the power field.
2. Nonlinear and Chaotic Dynamics
The inclusion of financial bankruptcy enhances the system's nonlinearity. The Soviet economic collapse was a rapidly deteriorating process, consistent with chaotic dynamics.
Simulating Historical Evolution
1985–1990: The Soviet government (𝜙₁) under Gorbachev attempted to maintain power through reforms, but rising fiscal pressure (𝐸(𝑡)) weakened its control. 𝜙₁ gradually declined from 1, while other nodes (e.g., 𝜙₂, 𝜙₄) rose.
August 1991 Coup: Communist Party conservatives (𝜙₆) briefly surged in power during the coup attempt but failed due to lack of economic support and internal unity. Financial bankruptcy further diminished 𝜙₁ and 𝜙₆.
December 1991 Dissolution: 𝜙₁ collapsed to 0, with power shifting to the Russian Federation (𝜙₂), Eastern European states (𝜙₃), and the U.S. (𝜙₄).
Random Noise 𝜂ᵢ(𝑡)
Financial bankruptcy can be treated as part of 𝜂₁(𝑡), simulating unpredictable economic shocks (e.g., sharp drops in oil revenue and foreign debt crises in 1991 as random pulses).
3. Self-Organized Criticality (SOC)
The Soviet government's pressure 𝑃₁(𝑡) accumulated with financial bankruptcy, reaching a critical threshold 𝑃ₓ, consistent with SOC theory:
Pressure Accumulation: 𝑃₁(𝑡+1) = 𝑃₁(𝑡) + Δ𝑃₁, where Δ𝑃₁ includes economic decline (financial bankruptcy), nationalist movements, and external pressures.
Critical Collapse: In 1991, 𝑃₁ > 𝑃ₓ, triggering a collapse of the power field. 𝑃₁ plummeted, with power partially transferring to 𝑃₂ (Russian Federation) and 𝑃₃ (Eastern European states).
Financial bankruptcy accelerated this process by undermining the Soviet government's capacity to respond to challenges.
4. Emergent Behavior and New Order
Monte Carlo simulations illustrate the power field's transition from chaos to stability:
December 1991: 𝜙₁ → 0, marking the completion of the Soviet dissolution.
1992–1995: The Russian Federation (𝜙₂) stabilized at a moderate level but was constrained by economic weaknesses from fully replacing the Soviet position. The U.S. (𝜙₄) emerged as the dominant global power, while Eastern European states (𝜙₃) integrated into the West.
The long-term effect of financial bankruptcy was that Russia (𝜙₂) inherited a weakened economic base, limiting its power field expansion.
Conclusion and Integration of Financial Bankruptcy
Using network dynamics, chaos theory, and SOC, this model reconstructs the dynamic process of the Soviet Union's dissolution. Incorporating financial bankruptcy reveals:
Financial bankruptcy, as an external shock (𝐹₁(𝑡) or 𝜂₁(𝑡)), accelerated the collapse of the Soviet government (𝜙₁).
It altered the power field structure by weakening internal stability (𝐴₁₁) and amplifying external pressure (𝐴₁₄).
Post-dissolution, the Russian Federation (𝜙₂) inherited partial power but was constrained by economic fragility.
Future steps could simulate post-Cold War global power shifts, such as adding China as a new node to analyze its rise and its impact on 𝜙₄ (U.S.) and 𝜙₂ (Russia). Python simulations could numerically solve these equations to visualize the evolution curves of 𝜙ᵢ(𝑡).
