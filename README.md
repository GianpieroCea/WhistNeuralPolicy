# About

This project tries to see if it is possible to learn a neural policy that can learn 
a very basic variant of Whist for two players where all cards are visible.

Whist is a classic trick-taking game. Despite its simple rule, the game mechanics can be very interesting.


# Project scope

The idea for this project is to be very lean and to work in terms of milestones.

These are:

- [x] Coding up the game logic (game.py)
- [x] Coding up the minmax algorith with alpha-beta
- [] Use the alpha-beta minmax to generate a dataset to train on
- [] Create a neural network to learn both optimal playing but also learn a latent representation of the state
- [] (Optional) Different directions - trying to explain the results? Bayesian regression using the compressed features?
- [] (Optional) Code up a basic UI where a human can analyse his play against optimal play?



# Goal

The goal is to understand if it is possible to generate simple heuristics to determine the best action in Whist-variants


# Whist

The variant we code up works as follow:

- two players are handed 13 cards each from a standard deck of 52
- The game is played with no trump (but optionally trump can be specified)

- -At each turn the two player each chose one card. The player following the lead player must respond with a card of same suit and the trick is won by whoever has the higher card.
If the follower does not have a card in the lead suit, he can throw whatever card and he loses the trick. If a trump suit is selected then the follower can still win the trick in this case if he is able to "trump" the leader's card using a card of trump suit.

- The next to lead is the winner of the previous trick.

- For this variant, all 26 cards are avaialble to both players, making this game more amenable to analysis thanks to the full information it provides.


# No AI generated code

For this repo we follow a policy that no AI generate code can be use.
While I will allow myself to use AI for quick buck fixing anf brainstorming, all the core algorithms and decisions are all human made.