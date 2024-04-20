# Import necessary libraries: pandas for data handling, matplotlib for plotting, and SQLAlchemy for database interactions.
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def load_data(engine):
    """Load data from the database."""
    # Fetch training data from the database into a DataFrame.
    train_df = pd.read_sql('train', con=engine)
    # Fetch selected ideal functions data from the database into a DataFrame.
    ideal_functions_df = pd.read_sql('selected_ideal_functions', con=engine)
    # Fetch test data mappings from the database into a DataFrame.
    mappings_df = pd.read_sql('test_mappings', con=engine)
    return train_df, ideal_functions_df, mappings_df

def plot_training_and_ideal(train_df, ideal_functions_df):
    """Plot training data and ideal functions."""
    # Initialize the plot with specified figure size.
    plt.figure(figsize=(10, 6))
    x = train_df['x']
    
    # Plot training data
    plt.scatter(x, train_df['y1'], color='blue', label='Training Y1')
    plt.scatter(x, train_df['y2'], color='green', label='Training Y2')
    plt.scatter(x, train_df['y3'], color='red', label='Training Y3')
    plt.scatter(x, train_df['y4'], color='cyan', label='Training Y4')
    
    # Plot ideal functions
    for i in range(1, len(ideal_functions_df.columns)):
        plt.plot(ideal_functions_df['x'], ideal_functions_df.iloc[:, i], '--', label=f'Ideal Func {i}')
    
    # Set the title, labels, and enable the legend and grid for the plot.
    plt.title('Training Data and Selected Ideal Functions')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_test_mappings(test_df, mappings_df):
    """Plot test data with mappings to ideal functions."""
    # Initialize the plot with specified figure size.
    plt.figure(figsize=(10, 6))
    # Plot the test data as gray scatter points.
    plt.scatter(test_df['x'], test_df['y'], color='gray', label='Test Data')
    
    # Highlight mapped points
    for index, row in mappings_df.iterrows():
        plt.scatter(row['x'], row['y'], color='magenta', edgecolors='black', label='Mapped Test Data' if index == 0 else "")
    
    # Set the title, labels, and enable the legend and grid for the plot.
    plt.title('Test Data and Mapped Ideal Functions')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Create a database engine.
    engine = create_engine('sqlite:///data_analysis.db')
    # Load all necessary data using the created engine
    train_df, ideal_functions_df, mappings_df = load_data(engine)
    # Plot training data alongside ideal functions.
    plot_training_and_ideal(train_df, ideal_functions_df)
    # Fetch test data and plot it along with its mappings.
    plot_test_mappings(pd.read_sql('test', con=engine), mappings_df)

if __name__ == "__main__":
    main()
