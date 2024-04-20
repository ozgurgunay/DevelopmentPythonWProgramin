import unittest
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# Import the functions to be tested from their respective modules.
from select_ideal_functions import sum_of_squared_differences, select_ideal_functions
from map_test_data import map_test_data

# Define a class for testing the data analysis functions, inheriting from unittest.TestCase.
class TestDataAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """set up a temporary database and load it with sample data."""
        # Create an in-memory SQLite database which is faster and doesn't require clean-up.
        cls.engine = create_engine('sqlite:///:memory:')
        # Generate sample training data using numpy functions to simulate real data.
        cls.sample_train_data = pd.DataFrame({
            'x': np.linspace(0, 10, 100),
            'y1': np.sin(np.linspace(0, 10, 100)),
            'y2': np.cos(np.linspace(0, 10, 100)),
            'y3': np.sin(np.linspace(0, 10, 100)) + np.cos(np.linspace(0, 10, 100)),
            'y4': np.sin(np.linspace(0, 10, 100)) * np.cos(np.linspace(0, 10, 100))
        })
        # Generate sample ideal function data, with each function differing by a constant shift.
        cls.sample_ideal_data = pd.DataFrame({
            'x': np.linspace(0, 10, 100),
            **{f'y{i}': np.sin(np.linspace(0, 10, 100)) + i for i in range(1, 51)}
        })
        # Load these DataFrames into the temporary database.
        cls.sample_train_data.to_sql('train', con=cls.engine, index=False)
        cls.sample_ideal_data.to_sql('ideal', con=cls.engine, index=False)


    def test_sum_of_squared_differences(self):
        """Test the sum of squared differences function."""
        # Create sample series with identical entries and test if SSD is zero.
        series1 = pd.Series([1, 2, 3])
        series2 = pd.Series([1, 2, 3])
        self.assertEqual(sum_of_squared_differences(series1, series2), 0)

        # Create sample series with different entries and test if SSD is calculated correctly.
        series3 = pd.Series([1, 2, 3])
        series4 = pd.Series([3, 2, 1])
        self.assertEqual(sum_of_squared_differences(series3, series4), 8)

    def test_select_ideal_functions(self):
        """Test the selection of ideal functions."""
        # Run the function to select ideal functions based on the sample data and ensure results are stored correctly.
        select_ideal_functions(self.engine)
        results_df = pd.read_sql('selected_ideal_functions', con=self.engine)
        self.assertTrue(not results_df.empty)
        self.assertTrue('Ideal_Y1' in results_df.columns)

    def test_map_test_data(self):
        """Test the mapping of test data."""
        # Assuming 'map_test_data' has been modified to accept 'engine' as a parameter
        map_test_data(self.engine)
        results_df = pd.read_sql('test_mappings', con=self.engine)
        self.assertTrue(not results_df.empty)
        self.assertTrue('DeltaY' in results_df.columns)

if __name__ == '__main__':
    unittest.main(exit=False)