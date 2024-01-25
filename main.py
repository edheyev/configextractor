import pandas as pd
import re

def extract_tables_from_sheet(df):
    """
    Extract tables from the given DataFrame by using 'Measure' as table names
    and 'Level' as row names. Skips the row if 'Measure' field is 'Measure' itself.
    """
    tables = {}
    current_table = None
    seen_tables = set()  # To keep track of already seen table names

    for i, row in df.iterrows():
        measure, level = row[0], row[1]

        # Skip the row if 'Measure' field is just 'Measure'
        if measure == 'Measure':
            continue

        if pd.notnull(measure) and measure not in seen_tables:
            current_table = measure
            tables[current_table] = []
            seen_tables.add(measure)
        
        if pd.notnull(level) and current_table is not None:
            tables[current_table].append(level)

    return tables



def create_configs_from_tables(tables, sheet_name):
    """
    Create configurations from the extracted tables. Each config will have a 
    'placeholder_text' dictionary with keys as row names and values as 'todo'.
    """
    configs = []
    for table_name, row_names in tables.items():
        # Creating a placeholder_text dictionary
        placeholder_text = {row_name: "todo" for row_name in row_names}

        config = {
            "sheet_name": sheet_name,
            "table_name": table_name,
            "row_names": row_names,
            "placeholder_text": placeholder_text
        }
        configs.append(config)
    return configs


def valid_python_identifier(name):
    """
    Converts a name to a valid Python identifier by removing or replacing invalid characters.
    """
    # Replace spaces and invalid characters with underscores
    name = re.sub(r'\W|^(?=\d)', '_', name)
    return name

def write_config_to_file(config, filename):
    """
    Writes a configuration dictionary to a file as a Python variable.
    """
    with open(filename, "a") as file:
        # Convert the table name to a valid Python identifier
        var_name = valid_python_identifier(config["table_name"])
        file.write(f'{var_name} = ')
        file.write(str(config))
        file.write("\n\n")

def main(file_path='MymupMonthly1.xlsx'):
    xls = pd.ExcelFile(file_path)
    all_configs = []
    config_variable_names = []  # List to store the names of config variables

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Extract tables from the sheet
        tables = extract_tables_from_sheet(df)

        # Create configurations for each table
        configs = create_configs_from_tables(tables, sheet_name)
        all_configs.extend(configs)

    # Write configs to a file and accumulate config variable names
    with open("data_config.py", "a") as file:
        for config in all_configs:
            var_name = valid_python_identifier(config["table_name"])
            file.write(f'{var_name} = ')
            file.write(str(config))
            file.write("\n\n")
            config_variable_names.append(var_name)  # Add the variable name directly

        # Construct the line for all_configs and write it
        all_configs_line = f'all_configs = [{", ".join(config_variable_names)}]'
        file.write(all_configs_line)

if __name__ == "__main__":
    main()
