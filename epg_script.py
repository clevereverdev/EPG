import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# URL of the website with the EPG data
url = 'https://www.dthhelp.net/epg/sony_max_tv_guide.html'

# Send a GET request to the website
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table rows containing program information
rows = soup.select('table tr')

# Define the channel ID and channel name
channel_id = 'sonymaxhd'
channel_name = 'Sony Max HD'

# Create the root element of the XML
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>'

# Iterate over the rows and extract program information
for row in rows:
    # Extract the program start time and title
    cols = row.find_all('td')
    if len(cols) >= 2:
        try:
            start_time = datetime.strptime(cols[0].text, '%H:%M')  # Assuming the time format is HH:MM
            title = cols[1].text
            
            # Generate the program end time by adding 1 hour to the start time
            end_time = (start_time + timedelta(hours=1)).strftime('%H:%M')
            
            # Generate the XML for the program
            xml += f'\n  <programme start="{start_time.strftime("%Y%m%d%H%M%S")}" stop="{end_time}" channel="{channel_id}">\n    <title lang="en">{title}</title>\n  </programme>'
        
        except ValueError:
            # Skip rows with invalid time data
            continue

# Close the root element of the XML
xml += '\n</tv>'

# Write the XML to a file
filename = 'epg.xml'
with open(filename, 'w', encoding='utf-8') as file:
    file.write(xml)

print(f'EPG data has been saved to {filename}')
