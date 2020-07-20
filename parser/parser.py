import requests
from pdfminer.high_level import extract_text
from shutil import copyfileobj
import tempfile
from re import search, sub, IGNORECASE
from .util import rlstrip_dot, composite_function

# {
# 	"region": {
# 		"name": "Region name",
# 		"counties": [
# 			{
# 				"name": "County Name",
# 				"areas":[
# 					{
# 						"name": "Area name",
# 						"details": {
# 							"date": "Date",
# 							"time": "Time",
# 							"locations": ["location"]
# 						}
# 					}
# 				]
# 			}
# 		]
# 	}
# }

def get_text(url):
    r = requests.get(url, stream=True)
    temFile = tempfile.TemporaryFile()
    copyfileobj(r.raw, temFile)
    text = extract_text(temFile)
    text = text.replace("\n", '.')
    text = sub(r"[\s]{2,}", ' ', text)
    return text


def get_regions(text):
    regions = dict()
    regex = r"[.]([a-zA-Z\s]+?REGION)(.+?)[.](?:[a-zA-Z\s]+?REGION)"
    region_search = search(regex, text, IGNORECASE)
    while region_search:
        # Get the top regio
        region = dict()
        region["name"] = region_search.group(1).strip()
        region_key = '_'.join(region["name"].lower().split(' '))
        region["counties"] = get_counties(region_search.group(2), regions, region_key)
        regions[region_key] = region
        # Remove the region
        text = text.replace(region_search.group(1), '')
        text = text.replace(region_search.group(2), '')

	# Do the region search again
        region_search = search(regex, text, IGNORECASE)

    last_region_check = search(r"[.]([a-zA-Z\s]+?REGION)(.+?customers)", text, IGNORECASE)
    if last_region_check:
        # Get the last region
        region = dict()
        region["name"] = last_region_check.group(1).strip()
        region_key = '_'.join(region["name"].lower().split(' '))
        region["counties"] = get_counties(last_region_check.group(2), regions, region_key)
        regions[region_key] = region
    return regions

def get_counties(text, regions, region_key):
    counties = list()
    regex = r"[.]([a-zA-Z\s]+?COUNTY)(.+?)[.]([a-zA-Z\s]*?COUNTY)"
    county_search = search(regex, text, IGNORECASE)
    while county_search:
        # Get the top county
        county = dict()
        county["name"] = county_search.group(1).strip()
        county["areas"] = get_areas(county_search.group(2))

        # Check if the region already exists
        if region_key in regions.keys():
            regions[region_key]["counties"].append(county)
        else:
            counties.append(county)

        # Remove the county
        text = text.replace(county_search.group(1), '')
        text = text.replace(county_search.group(2), '')

        # Do the county search again
        county_search = search(regex, text, IGNORECASE)

    last_county_check = search(r"[.]([a-zA-Z\s]+?COUNTY)(.+?)$", text, IGNORECASE)
    if last_county_check:
        # Get the last county
        county = dict()
        county["name"] = last_county_check.group(1).strip()
        county["areas"] = get_areas(last_county_check.group(2))

        # Check if the region already exists
        if region_key in regions.keys():
            regions[region_key]["counties"].append(county)
        else:
            counties.append(county)

    return counties

def get_areas(text):
	areas = list()
	regex = r"(AREA:[a-zA-Z\s,]+[.])(DATE.+?)AREA"
	area_search = search(regex, text, IGNORECASE)
	while area_search:
		# Get the top area
		area = dict()
		area["name"] = area_search.group(1)
		area["details"] = get_details(area_search.group(2))
		areas.append(area)

		# Remove the area
		text = text.replace(area_search.group(1), '')
		text = text.replace(area_search.group(2), '')

		# Do the county search again
		area_search = search(regex, text, IGNORECASE)

	last_area_check = search(r"(AREA:[a-zA-Z\s,]+[.])(DATE.+?)$", text, IGNORECASE)
	if last_area_check:
		# Get the last area
		area = dict()
		area["name"] = last_area_check.group(1)
		area["details"] = get_details(last_area_check.group(2))
		areas.append(area)

	return areas

def get_details(text):
	details = dict()
	date_search = search(r"(DATE:)(.+?)TIME", text, IGNORECASE)
	if date_search:
		details["date"] = date_search.group(2).strip()
		text = text.replace(date_search.group(1), '')
		text = text.replace(date_search.group(2), '')

	time_search = search(r"(TIME:)(.+?P[.]M[.])", text, IGNORECASE)
	if time_search:
		details["time"] = time_search.group(2).strip()
		text = text.replace(time_search.group(1), '')
		text = text.replace(time_search.group(2), '')

	details["locations"] = get_locations(text)

	return details

def get_locations(text):
	stripSpaces = lambda location : location.strip()
	return list(map(composite_function(stripSpaces, rlstrip_dot), text.split(',')))

def parse(url):
    return get_regions(get_text(url))
