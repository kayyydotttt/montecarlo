# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

class Die():
    """A die has N sides, or “faces”, and W weights, and can be rolled to select
a face.
W defaults to 1.0 for each face but can be changed after the
object is created.
Note that the weights are just numbers, not a normalized
probability distribution.
The die has one behavior, which is to be rolled one or more
times.
    """
    #Takes an array of faces as an argument. The array's
    #data type (dtype) may be strings or numbers
    def __init__(self, faces):
        """
Takes an array of faces as an argument. The array's
data type (dtype) may be strings or numbers.
Internally iInitializes the weights to 1.0 for each face.
Saves both faces and weights into a private
dataframe that is to be shared by the other methods

        """
        # Saves both faces and weights into a private
        # dataframe that is to be shared by the other methods.
        #Internally iInitializes the weights to 1.0 for each face.

        self.df = pd.DataFrame({'face': faces, 'weight': [1.0] * len(faces)})

    # Takes two arguments: the face value to be changed
    # and the new weight. 
    def change_weight(self, face, weight):
        """Takes two arguments: the face value to be changed
and the new weight.
Checks to see if the face passed is valid; is it in the
array of weights?
Checks to see if the weight is valid; is it a float? Can it
be converted to one?
        """
        # Checks to see if the face passed is valid; is it in the
        # array of weights?
        if face not in self.df['face'].values:
            raise ValueError("Error face")
        if not isinstance(weight, float) and not np.can_cast(type(weight), 'float'):
            raise ValueError( "Error weight")
        self.df.loc[self.df['face']==face, 'weight'] = weight
        
    # Takes a parameter of how many times the die is to be
    # rolled; defaults to 1.
    def roll(self, rolls=1):
        """Takes a parameter of how many times the die is to be
rolled; defaults to 1.
This is essentially a random sample from the vector of
faces according to the weights.
Returns a list of outcomes.
Does not store internally these results.
        """

        # a random sample from the vector of
        # faces according to the weights.
        outcomes_list = np.random.choice(self.df['face'], size = rolls, p=self.df['weight']/self.df['weight'].sum())
        # Returns a list of outcomes.
        # Does not store internally these results.
        return list(outcomes_list)
    #  user the die’s current set of faces and
    # weights (since the latter can be changed).
    def show(self):
        """Returns the dataframe created in the initializer.

        """

        # Returns the dataframe created in the initializer.
        return self.df

class Game():
    """Each game is initialized with one or more of similarly defined
dice (Die objects).
By “same kind” and “similarly defined” we mean that each die
in a given game has the same number of sides and associated
faces, but each die object may have its own weights.
The class has a behavior to play a game, i.e. to rolls all of the
dice a given number of times.
The class keeps the results of its most recent play. 
    """
    # Die as an argument
    def __init__(self, dice):
        """Takes a single parameter, a list of already instantiated
similar Die objects.
        """
        self.dice = dice
        self.results_df = pd.DataFrame(columns=['roll number', 'die number', 'face'])

    def play(self, rolls):
        """Takes a parameter to specify how many times the
dice should be rolled.
Saves the result of the play to a private dataframe of
shape N rolls by M dice.
The private dataframe should have the roll number is
a named index.
This results in a table of data with columns for roll
number, the die number (its list index), and the face
rolled in that instance.
        """
        for i in range(rolls):
            for x, die in enumerate(self.dice):
                face = die.roll()
                self.results_df = self.results_df.append({'roll number':i+1, 'die number':x, 'face':face[0]}, ignore_index = True)
        return self.results_df
    
    def show(self, form='wide'):
        """This method just passes the private dataframe to the
user.
Takes a parameter to return the dataframe in narrow
or wide form.
This parameter defaults to wide form.
This parameter should raise an exception of
the user passes an invalid option.
The narrow form of the dataframe will have a twocolumn index with the roll number and the die number,
and a column for the face rolled.
The wide form of the dataframe will a single column
index with the roll number, and each die number as a
column
        """
        if form not in ['wide','narrow']:
            raise ValueError("form must be wide or narrow")
        if form == 'wide':
            wide_df = self.results_df.pivot(index='roll number', columns='die number', values='face')
            return wide_df
        else:
            narrow_df = self.results_df.set_index(['roll number', 'die number'])['face']
            return narrow_df
        
class Analyzer():
    """An analyzer takes the results of a single game and computes various
descriptive statistical properties about it. These properties results are
available as attributes of an Analyzer object. Attributes (and associated
methods) include:
A face counts per roll, i.e. the number of times a given face
appeared in each roll. For example, if a roll of five dice has all
sixes, then the counts for this roll would be 6 for the face value
'6' and 0 for the other faces.
A jackpot count, i.e. how many times a roll resulted in all faces
being the same, e.g. all one for a six-sided die.
A combo count, i.e. how many combination types of faces
were rolled and their counts.
    """
    def __init__(self, game):
        """Takes a game object as its input parameter.
At initialization time, it also infers the data type of the
die faces used.
        """
        self.game = game
        self.jackpot_results_df = None
        self.combo_results_df = None
        self.value_counts = None
        
        
    def jackpot(self):
        """Returns an integer for the number times to the user.
Stores the results as a dataframe of jackpot results in
a public attribute.
The dataframe should have the roll number as a
named index.
        """
        wide_df = self.game.results_df.pivot(index='roll number', columns='die number', values='face')
        mask_df = (wide_df == wide_df.iloc[0]).all(axis=1)
        self.jackpot_results_df = mask_df.to_frame(name='jackpot')
        return self.jackpot_results_df['jackpot'].sum()

    def combo(self):
        """ A combo method to compute the distinct combinations of faces
rolled, along with their counts.
Combinations should be sorted and saved as a multicolumned index.
Stores the results as a dataframe in a public attribute.
        """
        wide_df = self.game.results_df.pivot(index='roll number', columns='die number', values='face')
        self.combo_results_df = wide_df.value_counts().reset_index(name='count')

        return self.combo_results_df
    
    def face_counts_roll(self):
        """Stores the results as a dataframe in a public attribute.
The dataframe has an index of the roll number and
face values as columns (i.e. it is in wide format).
        """

        wide_df = self.game.results_df.pivot(index='roll number', columns='die number', values='face')
        self.value_counts = wide_df.apply(pd.Series.value_counts, axis=1).fillna(0)
        return self.value_counts
