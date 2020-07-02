# Artificial-intelligence-A-star-algorithm
### Informed search techniques: A *
The A * algorithm is used to find a minimum cost path from a start node to a target node in a graph with weighted edges / arcs (with costs).

### Defining the challenge
A little wizard set out to find a magic stone. The magic stone is found in an equally magical cave. The cave is rectangular in shape divided into square plots, each of a certain color. 

At the entrance to the cave an old wizard offers him a pair of boots the color of the plot that is at the entrance to the cave, and tells him never to step on a pair of one-color boots on a plot of another color because he will surely die. 

The little wizard can also carry an extra pair of boots (a pair of spare boots). The old man also warns him that due to the energy of the enchanted land, the boots will be damaged after 3 plots, and if he does not change them until they are completely damaged, he will remain barefoot in the next plot and will die. 

Some plots may contain a pair of boots. The little wizard can take that pair of boots and put them in the sack or change his current boots to enter a new plot of another color (when changing the boots, if he has an empty sack he will put the old ones in the sack, otherwise he has to choose between throwing them away or throwing them out of the sack and putting them in their place). It is considered that the change of boots is made after leaving the current plot but immediately before entering a new plot (so, say, intermediate, on the border - but there is no need to consider the border as a special state; the step and change of boots will be seen as a unitary transition). When he has an empty sack, the little wizard will always take the boots from the plot to put them in the sack; he will also not throw the boots out of the sack if he does not have others to put in place (either the shoes or the ones found in the plot). But if the boots in the sack are the same color as those in the plot and are not worn (the number of wears is 0) then do not change them (it does not matter, it reaches 2 possible identical successor states).

It is considered that if the boots were taken from a plot, after the wizard left, magically a new pair of the same color appears in the same place (so if he took a pair from there, but after a few steps he also reached that plot would find a pair of boots the same as those taken previously, and could use them). However, he cannot take more than one pair of boots from a plot (that is, he cannot change the boots in the sack and the ones he had worn with those found in the plot). The boots found in a plot are always new.

The wizard tends to renew his boots. If he has boots in the color of the ones found in the plot, or wears boots in the color of those found in the plot, he will renew them if they are not new.

In order not to get 2 identical successors for certain conditions, keep in mind that it does not make sense to change the boots in the bag with the ones worn if they are the same color and have the same number of wears.

At the entrance to the cave it is considered that a step has been taken, so the boots in the initial state have the number of wears equal to 1.

The wizard can only move on the line and the column, not on the diagonal. Attention, the goal is not only to reach the stone but also to get out of the cave with it (return to the initial node).

As you can see, the little wizard is under heavy test and only you can help him find his way to the magic stone.
