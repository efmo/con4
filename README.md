# con4

This is a simple experiment designed to train a small neural network to play a connect-four-like game, inspired by the recent rise of [Alphago][alphago] in the news. 

To generate a dataset, a primitive AI just slightly ahead of random) plays itself a couple thousand times, generating about 11 or 12 moves per game on average. After each game with a winner, each snapshot of the board is labeled either RED or BLUE accordingly. Each sample can only have one label. The max amount of duplicate samples allowed is defined by the user. Two samples may have identical boards but different labels.

The model itself is defined using Keras in c4trainer.py to be a 3-layer convolutional neural network. Before training, the model win rate should be about 50% as RED (first) and 33% as BLUE (second). After training, the model should be around 95% RED and 90% BLUE. Training with default values should take about 5 minutes.

The epoch, layer node, max duplicate, and dataset sample counts were all determined by mostly arbitrary experiment. No configuration with a dataset over 10,000 achieved >80% validation accuracy while maintaining a >90% win rate. 

Things to try:
 - changing init function for model weights
 - better nondeterministic model play
 - experiment with bigger board size and win length
 - ?

Thanks for looking!

[alphago]: <https://deepmind.com/alpha-go.html>