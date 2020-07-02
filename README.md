# Artificial-intelligence-A-star-algorithm
### Informed search techniques: A *
The A * algorithm is used to find a minimum cost path from a start node to a target node in a graph with weighted edges / arcs (with costs).

### Defining the challenge
A little wizard set out to find a magic stone. The magic stone is found in an equally magical cave. The cave is rectangular in shape divided into square plots, each of a certain color. 

At the entrance to the cave an old wizard offers him a pair of boots the color of the plot that is at the entrance to the cave, and tells him never to step on a pair of one-color boots on a plot of another color because he will surely die. 

The little wizard can also carry an extra pair of boots (a pair of spare boots). The old man also warns him that due to the energy of the enchanted land, the boots will be damaged after 3 plots, and if he does not change them until they are completely damaged, he will remain barefoot in the next plot and will die. 

Some plots may contain a pair of boots. The little wizard can take that pair of boots and put them in the sack or change his current boots to enter a new plot of another color (when changing the boots, if he has an empty sack he will put the old ones in the sack, otherwise he has to choose between throwing them away or throwing them out of the sack and putting them in their place). It is considered that the change of boots is made after leaving the current plot but immediately before entering a new plot (so, say, intermediate, on the border - but there is no need to consider the border as a special state; the step and change of boots will be seen as a unitary transition). When he has an empty sack, the little wizard will always take the boots from the plot to put them in the sack; he will also not throw the boots out of the sack if he does not have others to put in place (either the shoes or the ones found in the plot). But if the boots in the sack are the same color as those in the plot and are not worn (the number of wears is 0) then do not change them (it does not matter, it reaches 2 possible identical successor states).
