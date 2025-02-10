import urllib.request
import logging
import argparse
import csv
from datetime import datetime

def downloadData(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

def processData(data):
    personData = {}
    logger = logging.getLogger("Assignment2")
    lines = data.splitlines()
    reader = csv.reader(lines)
    next(reader)  # Skip header
    
    for i, row in enumerate(reader, start=1):
        try:
            id_num = int(row[0])
            name = row[1]
            birthday = datetime.strptime(row[2], "%d/%m/%Y").date()
            personData[id_num] = (name, birthday)
        except (ValueError, IndexError):
            logger.error(f"Error processing line #{i} for ID #{row[0] if row else 'Unknown'}")
    
    return personData

def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday}")
    else:
        print("No user found with that id")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL of the CSV file")
    args = parser.parse_args()
    
    if not args.url:
        print("Error: --url argument is required.")
        return
    
    logging.basicConfig(filename="errors.log", level=logging.ERROR)
    
    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
    
    personData = processData(csvData)
    
    while True:
        try:
            user_input = int(input("Enter an ID to lookup (0 to exit): "))
            if user_input <= 0:
                break
            displayPerson(user_input, personData)
        except ValueError:
            print("Invalid input. Please enter a valid integer ID.")
    
if __name__ == "__main__":
    main()
