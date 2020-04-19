import requests
from pdfminer.high_level import extract_text
from shutil import copyfileobj
import tempfile

keywords = ['REGION', 'COUNTY', 'TIME', 'DATE','AREA', ',' ]

class County:
    name = None
    area = None
    time = None
    date = None
    locations = []

    def serialize(self):
        if self.name == None:
            return

        return { 'name': self.name,
                 'area': self.area,
                 'time': self.time,
                 'date': self.date,
                 'locations': self.locations
        }

class Region:
    region = None
    counties = []

    def serialize(self):
        ser_counties = []
        for sc in self.counties:
            ser_counties.append(sc.serialize())

        return {'region': self.region,
                 'counties': ser_counties
         }

def download_file(url):
    r = requests.get(url, stream=True)
    temFile = tempfile.TemporaryFile()
    copyfileobj(r.raw, temFile)
    return temFile

def get_text(file_):
    return extract_text(file_)

def check_for_keyword(lines):
    new_lines = []
    for line in lines:
        for k in keywords:
            if k in line:
                new_lines.append(line)
                break
    return new_lines

def take_lines(contents):
    lines = []
    contents = contents.split('\n')
    lappend = lines.append
    for line in contents:
        if len(line) < 3: continue
        lappend(line)
    return check_for_keyword(lines[1:])

def parse_(lines):
    hit_county, hit_region, i = 0, 0, 0
    regions = []
    region = Region()
    county = County()
    rounds = len(lines)
    for line in lines:
        i += 1
        line = line.replace('\n', '').lstrip().rstrip()
        if 'REGION' in line:
            if hit_region == 0:
                region.region = line
                hit_region = 1
            elif hit_region == 1:
                # another region encountered store current
                region.counties.append(county)
                county = County()
                regions.append(region)
                region = Region()
                region.region = line

        elif 'COUNTY' in line:
            if hit_county == 0:
                county.name = line
                hit_county = 1
            else:
                region.counties.append(county)
                county = County()
                county.name = line

        elif 'DATE' in line and 'TIME' in line:
            date_str = ''
            for x in line:
                if x == ' ':
                    continue

                if x == 'T':
                    county.date = date_str.replace('\n', '')
                    date_str = x
                    continue

                date_str += x
            county.time = date_str
            county.locations = lines[i].replace('\n', '').rstrip().lstrip().split(',')

        elif 'DATE' in line:
            county.date = line[6:]

        elif 'TIME' in line:
            county.time = line[6:]
            county.locations = lines[i].replace('\n', '').rstrip().lstrip().split(',')

        elif 'AREA' in line:
            county.area = line[6:]

        if i == rounds-1:
            region.counties.append(county)
            regions.append(region)


    return regions


def parse(url):
    tempFile = download_file(url)
    file_data = take_lines(get_text(tempFile))
    all_data = parse_(file_data)
    serialized_data = []
    append = serialized_data.append
    for r in all_data:
        append(r.serialize())
    return serialized_data
