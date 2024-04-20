# Import pandas for data manipulation and SQLAlchemy for database interaction.
import pandas as pd
from sqlalchemy import create_engine

# Define a function to map test data points to ideal functions.
def map_test_data():
    # Connect to the SQLite database.
    engine = create_engine('sqlite:///data_analysis.db')
    
    # Load necessary data from the database
    test_df = pd.read_sql('test', con=engine)
    selected_ideal_functions_df = pd.read_sql('selected_ideal_functions', con=engine)

    # Assuming a simple distance criterion for mapping test points to ideal functions
    threshold = 0.5  # This value should be adjusted based on specific project requirements

    # Initialize a list to store mappings.
    mappings = []
    
    # Loop through each column in the selected ideal functions DataFrame.
    for index, test_row in test_df.iterrows():
        x, y = test_row['x'], test_row['y']
        closest_function = None
        min_deviation = float('inf')
        
        # Compare against each selected ideal function
        for col in selected_ideal_functions_df.columns:
            if col == 'x':  # Skip the 'X' column as it's just the independent variable
                continue
            # Ensure there is a corresponding y-value at the same x in the ideal function data
            ideal_row = selected_ideal_functions_df[selected_ideal_functions_df['x'] == x]
            if ideal_row.empty:
                continue  # Skip if no corresponding x value is found
            
            ideal_y = ideal_row[col].values[0]
            deviation = abs(ideal_y - y)    # Calculate the deviation between y-values.

            # Update the closest function if the current one has a smaller deviation.
            if deviation < min_deviation:
                min_deviation = deviation
                closest_function = col

        # If the minimum deviation found is within the threshold, save this mapping
        if min_deviation <= threshold and closest_function is not None:
            mappings.append({
                'x': x,
                'y': y,
                'DeltaY': min_deviation,
                'IdealFuncNo': closest_function.replace('Ideal_', '')  # Remove 'Ideal_' prefix if present
            })

    # Convert the list of mappings to a DataFrame.
    mapping_df = pd.DataFrame(mappings)
    mapping_df.columns = ['x', 'y', 'DeltaY', 'IdealFuncNo']

    # Save the DataFrame to the database in a new table.
    mapping_df.to_sql('test_mappings', con=engine, if_exists='replace', index=False)
    print("Test data mappings have been saved to the database.")

# Execute the function if the script is run directly.
if __name__ == "__main__":
    map_test_data()
