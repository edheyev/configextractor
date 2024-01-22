import pandas as pd
from io import StringIO


def split_tables(df):
    # Identify the empty rows which indicate separation between tables
    mask = df.isnull().all(axis=1)
    tables = []
    start = 0
    for end in mask[mask].index:
        tables.append(df[start:end])
        start = end + 1
    tables.append(df[start:])  # Append the last table
    return tables


def create_config_from_dataframe(df, table_index):
    # Extracting row names and column headings
    row_names = df.iloc[:, 0].tolist()
    column_headings = df.columns[1:].tolist()

    # Creating the configuration structure
    config = {
        "table_name": f"fantasy_config_{table_index}",
        "row_names": row_names,
        "column_headings": column_headings,
    }

    return config


def write_config_to_file(config, filename):
    with open(filename, "a") as file:  # 'a' for append mode
        file.write(f'{config["table_name"]} = ')
        file.write(str(config))
        file.write("\n\n")


def main():
    # Sample fantasy/sci-fi themed data
    excel_data = StringIO(
        """
Starship,Class,Max Speed,Crew Capacity,Galaxy
Odyssey,Explorer,9.5 Warp,1000,Andromeda
Eclipse,Stealth,8.7 Warp,300,Milky Way
Nebula,Carrier,7.8 Warp,5000,Triangulum

Creature,Origin Realm,Power Level,Alignment,Notable Feature
Dragon,Mythica,High,Chaotic,Fire-Breathing
Phoenix,Aether,Medium,Neutral,Rebirth
Unicorn,Enchanted,Low,Good,Healing Powers
"""
    )

    # Read the data into a DataFrame
    df = pd.read_csv(excel_data)

    # Split the DataFrame into individual tables
    tables = split_tables(df)

    # Process each table and write config to a file
    for i, table in enumerate(tables):
        if not table.empty:
            config = create_config_from_dataframe(table, i)
            write_config_to_file(config, "fantasy_config.py")


if __name__ == "__main__":
    main()
