# -*- coding: utf-8 -*-


import unittest
import numpy as np
import pandas as pd
from montecarlo import Die, Game, Analyzer


class TestDie(unittest.TestCase):
    """ This unittest will test the die class
    """
    def test_init(self):
        """ checks to ensure that the initializer is creating a 
        dataframe for the die object by taking the list of faces
        """
        # Test with valid input
        die = Die([1, 2, 3])
        self.assertIsInstance(die.df, pd.DataFrame)

        # Test with invalid input
        with self.assertRaises(TypeError):
            die = Die(1.5)

    def test_change_weight(self):
        """ checks to ensure that the change_weight method
        properly changes the weight of the correct face
        """        
        die = Die([1, 2, 3])
        die.change_weight(1, 2.5)
        self.assertEqual(die.df.loc[die.df['face'] == 1, 'weight'].iloc[0], 2.5)

        with self.assertRaises(ValueError):
            die.change_weight(4, 1.0)


    def test_roll(self):
        """ Tests to ensure rolls is returning a list of outcomes of "rolls"
        
        """
        die = Die([1, 2, 3])
        result = die.roll()
        self.assertIsInstance(result, list)
        self.assertIn(result[0], [1, 2, 3])
        
    def test_show(self):
        """ tests the show method to ensure that it is returning a data frame
        """
        die = Die([1, 2, 3])
        self.assertIsInstance(die.show(), pd.DataFrame)


class TestGame(unittest.TestCase):
    """tests class game to ensure that it is being initialized and executed properly
    """
    def test_game_init(self):
        """ tests to ensure that the initializer function is creating a list 
        instance of die object and raising an error if input is invalid
        """
        # Test with valid input
        die = Die([1, 2, 3])
        die_type = [die]
        game = Game(die_type)
        self.assertIsInstance(game.dice, list)

        # Test with invalid input
        with self.assertRaises(TypeError):
            die = Die(1.5)
        
    def test_play(self):
        """ tests play method to ensure that it is creating a dataframe
        from the dice
        """
        die1 = Die([1, 2, 3])
        die2 = Die([4, 5, 6])
        game = Game([die1, die2])
        game.play(2)
        self.assertIsInstance(game.results_df, pd.DataFrame)

    def test_show(self):
        """
        tests to ensure that show is creating the proper length of a data frame and 
        based on the input "wide"
        """
        die1 = Die([1, 2, 3])
        die2 = Die([4, 5, 6])
        game = Game([die1, die2])
        game.play(2)
        result = game.show(form='wide')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (2, 2))

class TestAnalyzer(unittest.TestCase):
    """ Tests the analyzer class to ensure that it is working properly 
    """
    def test__init__(self):
        ''' Tests to make sure that the game is being called correctly and 
        its df is useable
        '''
        die1 = Die([1,2,3])
        die2 = Die([4,5,6])
        game = Game([die1, die2])
        game.play(100)
        analyzer = Analyzer(game)
        self.assertIsInstance(analyzer.game.results_df, pd.DataFrame)


    def test_jackpot(self):
        """ Tests to make sure that jackpot is returning an int
        """
        die1 = Die([1, 2, 3])
        die2 = Die([1, 2, 3])
        game = Game([die1, die2])
        game.play(1000)
        result = Analyzer(game)
        self.assertIsInstance(result.jackpot(), np.int64)


    def test_combo(self):
        """tests the combo method to ensure that the method can call 
        combo correctly and  returns a dataframe
        """
        die1 = Die([1, 2, 3])
        die2 = Die([1, 2, 3])
        game = Game([die1, die2])
        game.play(2)
        analyzer = Analyzer(game)
        result = analyzer.combo()
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_face_counts_roll(self):
        """ tests to make sure that face_counts_roll 
        is creating a dataframe of the different faces 
        """
        die1 = Die([1, 2, 3])
        list_die = [die1]
        game = Game(list_die)
        game.play(2)
        analyzer = Analyzer(game)
        self.assertIsInstance(analyzer.face_counts_roll(), pd.DataFrame)

        
# Export to PDF
if __name__ == '__main__':
    with open('monte_test_results.txt', 'a') as f:

        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestDie))
        suite.addTest(unittest.makeSuite(TestGame))
        suite.addTest(unittest.makeSuite(TestAnalyzer))
        # Run the tests and append the results to the file
        runner.run(suite)