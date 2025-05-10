#!/usr/bin/env python
# Autorship information
__author__ = "Hüsamettin Deniz Özeren"
__copyright__ = "Copyright 2024"
__credits__ = ["Hüsamettin Deniz Özeren"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Hüsamettin Deniz Özeren"
__email__ = "denizozeren614@gmail.com"

import json
from icalendar import Calendar

# File paths
ics_file = "bin_dates2025.ics"
output_json = "bin_dates2025.json"

# Initialize dictionaries to store dates
recycling_dates = []
general_waste_dates = []

# Read and parse the ICS file
with open(ics_file, 'r') as file:
    calendar = Calendar.from_ical(file.read())

    for component in calendar.walk():
        if component.name == "VEVENT":
            summary = component.get('SUMMARY')
            date = component.get('DTSTART').dt

            if "recycling" in summary.lower():
                recycling_dates.append(str(date))
            elif "general waste" in summary.lower():
                general_waste_dates.append(str(date))

# Save the dates to a JSON file
data = {
    "blue": recycling_dates,
    "green": general_waste_dates
}

with open(output_json, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data has been saved to {output_json}")