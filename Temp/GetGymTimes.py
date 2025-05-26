import requests
from bs4 import BeautifulSoup
import csv

def extract_timetable(url):
    # Fetch the webpage
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables on the page
    tables = soup.find_all('table')
    
    # Assuming the first table is the timetable
    timetable_table = tables[0]
    
    # Extract rows from the table
    rows = timetable_table.find_all('tr')
    
    # Initialize data list
    data = []
    
    # Iterate over each row
    for row in rows:
        cols = row.find_all(['th', 'td'])
        
        # Extract column values
        cols = [col.text.strip() for col in cols]
        
        # Skip empty rows
        if not cols:
            continue
        
        # Add day to the row if it's missing
        if len(cols) == 4:
            day = row.get('class')
            if day:
                day = day[0].capitalize()
                cols.insert(0, day)
        
        # Ensure all rows have the same number of columns
        if len(cols) < 5:
            cols.extend([''] * (5 - len(cols)))
        
        data.append(cols)
    
    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Day', 'Time', 'Class', 'Duration', 'Studio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in data:
            writer.writerow({
                'Day': row[0],
                'Time': row[1],
                'Class': row[2],
                'Duration': row[3],
                'Studio': row[4]
            })

# URL of the webpage
url = 'https://westwood.ie/fitness-classes/timetables/clontarf/live'

# Extract timetable data
data = extract_timetable(url)

# Write data to CSV file
write_to_csv(data, 'timetable.csv')

print("Timetable data has been saved to timetable.csv")
