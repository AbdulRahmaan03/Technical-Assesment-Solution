# Task 2 - Part A
import pymysql
import csv

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="admin12345",
    database="bgp_data",
)

cursor = connection.cursor()


# Question 1: How many IP Prefixes [v4/v6] are there in total?
cursor.execute("SELECT COUNT(*) AS total_rows FROM bgp_table;")
total_rows = cursor.fetchone()[0]
print(f"Total IP Prefixes: {total_rows}")
# For IPV4
cursor.execute("SELECT COUNT(*) AS total_rows FROM bgp_table_ipv4;")
total_rows_ipv4 = cursor.fetchone()[0]
print(f"Total IPV4 Prefixes: {total_rows_ipv4}")
# For IPV6
cursor.execute("SELECT COUNT(*) AS total_rows FROM bgp_table_ipv6;")
total_rows_ipv6 = cursor.fetchone()[0]
print(f"Total IPV6 Prefixes: {total_rows_ipv6}")

# Question 2: How many IP prefixes [v4/v6] are coming from Transit?
# Creating a temporary table with transit ASNs
cursor.execute(
    """
    CREATE TEMPORARY TABLE transit_asn (
        asn INT
    );
"""
)

# Inserting the transit ASNs
cursor.execute(
    """
    INSERT INTO transit_asn (asn) VALUES
    (2914), (6762), (1299), (3257), (3356), (174);
"""
)

# Updating the Path field to remove unwanted characters
cursor.execute("UPDATE bgp_table SET Path = TRIM(TRAILING 'i' FROM Path);")
cursor.execute("UPDATE bgp_table SET Path = TRIM(TRAILING 'e' FROM Path);")
cursor.execute("UPDATE bgp_table SET Path = TRIM(TRAILING '?' FROM Path);")
cursor.execute("UPDATE bgp_table SET Path = REPLACE(Path, '{', '');")
cursor.execute("UPDATE bgp_table SET Path = REPLACE(Path, '}', '');")
cursor.execute("UPDATE bgp_table SET Path = REPLACE(Path, ',', ' ');")

# Counting how many IP prefixes are coming from Transit
cursor.execute(
    """
    SELECT COUNT(*) AS transit_prefixes
    FROM bgp_table
    WHERE EXISTS (
        SELECT 1
        FROM transit_asn
        WHERE LOCATE(CAST(asn AS CHAR), Path) = 1
    );
"""
)
transit_prefixes = cursor.fetchone()[0]
non_transit_prefixes = total_rows - transit_prefixes
print(f"IP Prefixes from Transit: {transit_prefixes}")
print(f"IP Prefixes not from Transit: {non_transit_prefixes}")
# For IPV4
cursor.execute(
    """
    SELECT COUNT(*) AS transit_prefixes
    FROM bgp_table_ipv4
    WHERE EXISTS (
        SELECT 1
        FROM transit_asn
        WHERE LOCATE(CAST(asn AS CHAR), Path) = 1
    );
"""
)
transit_prefixes_ipv4 = cursor.fetchone()[0]
non_transit_prefixes_ipv4 = total_rows_ipv4 - transit_prefixes_ipv4
print(f"IPV4 Prefixes from Transit: {transit_prefixes_ipv4}")
print(f"IPV4 Prefixes not from Transit: {non_transit_prefixes_ipv4}")
# For IPV6
cursor.execute(
    """
    SELECT COUNT(*) AS transit_prefixes
    FROM bgp_table_ipv6
    WHERE EXISTS (
        SELECT 1
        FROM transit_asn
        WHERE LOCATE(CAST(asn AS CHAR), Path) = 1
    );
"""
)
transit_prefixes_ipv6 = cursor.fetchone()[0]
non_transit_prefixes_ipv6 = total_rows_ipv6 - transit_prefixes_ipv6
print(f"IPV6 Prefixes from Transit: {transit_prefixes_ipv6}")
print(f"IPV6 Prefixes not from Transit: {non_transit_prefixes_ipv6}")

# Question 3: How many IP prefixes have [1/2/3/4/... No. of hops]
# Calculating hops and count prefixes by hops
cursor.execute(
    """
    SELECT 
        CASE 
            WHEN Path IS NULL OR Path = '' THEN 0 -- Assign 0 hops for empty or NULL paths
            ELSE LENGTH(Path) - LENGTH(REPLACE(Path, ' ', '')) -- Calculate hops for valid paths
        END AS hops,
        COUNT(*) AS prefixes
    FROM bgp_table
    GROUP BY hops
    ORDER BY hops;
"""
)
hop_counts = cursor.fetchall()

print("IP Prefixes by Number of Hops:")

output_file = "bgp_analysis_1.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["No. of Hops", "Count of IP Prefixes"])
    print("No. of Hops, Count of IP Prefixes")
    for row in hop_counts:
        print(row[0], ",", row[1])
        writer.writerow([row[0], row[1]])
    writer.writerow([])

connection.close()
