# Import necessary libraries: pandas for data manipulation and SQLAlchemy for database interaction.
import pandas as pd
from sqlalchemy import create_engine

# Define a function to compute the sum of squared differences between two series.
def sum_of_squared_differences(series1, series2):
    return ((series1 - series2) ** 2).sum()


# Define a function to select ideal functions from a dataset based on the sum of squared differences.
def select_ideal_functions(engine):
    # Connection to the SQLite database.
    engine = create_engine('sqlite:///data_analysis.db')

    # Load the training and ideal data from the database.
    train_df = pd.read_sql('train', con=engine)
    ideal_df = pd.read_sql('ideal', con=engine)

    # Initialize a dictionary to store the best matching ideal function for each train function.
    selected_ideal_functions = {}

    # Iterate over the function indices in the training data (assuming functions y1 to y4).
    for i in range(1, 5):
        min_ssd = float('inf')
        best_match = None

        # Iterate over the function indices in the ideal data (assuming functions y1 to y50).
        for j in range(1, 51):
            # Ensure both columns exist in the respective DataFrames before calculating the sum of squared differences(SSD).
            if f'y{i}' in train_df.columns and f'y{j}' in ideal_df.columns:
                ssd = sum_of_squared_differences(train_df[f'y{i}'], ideal_df[f'y{j}'])
                # print(f'Checking Y{i} against y{j}, SSD: {ssd}')  # Debugging line
                # Check if the current the sum of squared differences is the smallest found so far, and if so, update the best match.
                if ssd < min_ssd:
                    min_ssd = ssd
                    best_match = j
            else:
                # If columns are missing, indicate an error or missing data issue.
                return True
                # print(f'Missing column y{i} in train_df or y{j} in ideal_df')  # Debugging line

        # Store the best match for each train function in the dictionary.
        selected_ideal_functions[f'y{i}'] = best_match
        
    # Check if any valid matches were found.
    if any(v is not None for v in selected_ideal_functions.values()):
        # Construct the DataFrame only if there are valid matches
        selected_columns = ['x'] + [f'y{selected_ideal_functions[f"y{i}"]}' for i in range(1, 5) if selected_ideal_functions[f"y{i}"] is not None]
        selected_df = ideal_df[selected_columns]
        # Save the DataFrame of selected ideal functions to the database.
        selected_df.to_sql('selected_ideal_functions', con=engine, if_exists='replace', index=False)
        print("Selected ideal functions have been saved to the database.")
    else:
        # If no valid matches were found, inform the user.
        print("No valid ideal functions were selected due to missing data or other issues.")


if __name__ == "__main__":
    select_ideal_functions()
