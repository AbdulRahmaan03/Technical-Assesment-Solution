# Task 1
import pymysql
import re

# MySQL Configuration
connection = pymysql.connect(
    host="localhost", user="root", password="admin12345", database="bgp_data"
)

# Initialize MySQL
cursor = connection.cursor()

# Dropping if the table already exits
cursor.execute("DROP TABLE IF EXISTS bgp_table")

# Defining Table Schema
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS bgp_table (
    Network VARCHAR(100),
    Next_Hop VARCHAR(50),
    Metric VARCHAR(10),
    LocPrf VARCHAR(10),
    Weight VARCHAR(10),
    Path TEXT
)
"""
)

# Commiting the query to the database
connection.commit()


# Function to parse, clean and insert the IP prefixes into MySQL
def parse_and_insert_bgp_data(file_path):
    entries = []
    temp_entry = None
    parsing_table = False
    field_starts = []
    field_names = []
    status_pattern = r"^([*>sdhrSR]+i?)"
    previous_line = None
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Define expected field names
    expected_fields = ["Network", "Next Hop", "Metric", "LocPrf", "Weight", "Path"]

    # Parse through each line
    for line_number, line in enumerate(lines, start=1):
        line = line.rstrip("\n")

        # Identify the header line and extract field positions
        if "Network" in line and "Next Hop" in line and not parsing_table:
            parsing_table = True

            # Extract field positions
            field_positions = []
            for field in expected_fields:
                index = line.find(field)
                if index != -1:
                    field_positions.append((field, index))

            # Sort the fields based on their positions
            field_positions.sort(key=lambda x: x[1])

            # Get field names and positions
            field_names = [field for field, pos in field_positions]
            # print(field_names)
            field_starts = [pos for field, pos in field_positions]
            # print(field_starts)
            field_ends = field_starts[1:] + [None]
            # print(field_ends)

            # break
            continue  # Skip the header line

        # End of BGP table
        if "Total number of prefixes" in line:
            previous_line = None
            parsing_table = False
            continue

        # Skip lines outside the BGP table or empty lines
        if not parsing_table or not line.strip():
            continue

        # Handle continuation lines
        if line.startswith(" ") or line.startswith("\t"):
            # This is a continuation line
            if temp_entry:
                # Extract values based on positions
                values = []
                for start, end in zip(field_starts, field_ends):
                    value = line[start:end].strip() if start < len(line) else ""
                    values.append(value)
                # Map field names to values
                entry = dict(zip(field_names, values))
                # Update temp_entry with new values
                for field in ["Next Hop", "Metric", "LocPrf", "Weight", "Path"]:
                    if entry.get(field):
                        temp_entry[field] = entry[field]
                    match = re.match(status_pattern, previous_line)
                    if match:
                        status_code = match.group(1)
                        network = previous_line[len(status_code) :].strip()
                        temp_entry["Status"] = status_code
                        temp_entry["Network"] = network
                    # temp_entry['Network'] = previous_line.strip()
                continue
            else:
                continue  # Skip continuation line if no temp_entry
        else:
            # New entry
            if temp_entry:
                entries.append(temp_entry)
            temp_entry = {}

            # Extract values based on positions
            values = []
            previous_line = line
            for start, end in zip(field_starts, field_ends):
                value = line[start:end].strip() if start < len(line) else ""
                values.append(value)
            # Map field names to values
            entry = dict(zip(field_names, values))

            # Handle the Status and Network fields
            match = re.match(status_pattern, entry.get("Network", ""))
            if match:
                status_code = match.group(1)
                network = entry["Network"][len(status_code) :].strip()
                temp_entry["Status"] = status_code
                temp_entry["Network"] = network
            else:
                temp_entry["Status"] = ""
                temp_entry["Network"] = entry.get("Network", "").strip()

            # Copy other fields
            for field in ["Next Hop", "Metric", "LocPrf", "Weight", "Path"]:
                temp_entry[field] = entry.get(field, "").strip()

    if temp_entry:
        entries.append(temp_entry)

    # Insert into MySQL
    for entry in entries:
        print(entry)
        # Map the extracted fields to your database columns
        mapped_entry = {
            "Network": entry.get("Network", ""),
            "Next_Hop": entry.get("Next Hop", ""),
            "Metric": entry.get("Metric", ""),
            "LocPrf": entry.get("LocPrf", ""),
            "Weight": entry.get("Weight", ""),
            "Path": entry.get("Path", "").strip(),
        }

        # Insert into database
        cursor.execute(
            """
        INSERT INTO bgp_table (Network, Next_Hop, Metric, LocPrf, Weight, Path)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (
                mapped_entry["Network"],
                mapped_entry["Next_Hop"],
                mapped_entry["Metric"],
                mapped_entry["LocPrf"],
                mapped_entry["Weight"],
                mapped_entry["Path"],
            ),
        )

    connection.commit()


# Calling the function to parse both the data files
parse_and_insert_bgp_data("data_file/typescript.IPV4.RR")
parse_and_insert_bgp_data("data_file/typescript.IPV6.RR")

# Close MySQL connection
cursor.close()
connection.close()
