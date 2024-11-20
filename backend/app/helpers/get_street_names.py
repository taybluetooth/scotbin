from councils.edinburgh import get_possible_addresses_by_letter
import json

def get_edinburgh_streets():
    alphabet = list(map(chr, range(97, 123)))
    page_num = 1
    output_data = {}
                
    with open("data/edin_streets.json", "w", encoding="utf-8") as jsonfile: 
        for letter in alphabet:
            page_num = 1
            output_data[letter] = []  # Initialize an empty list for each letter
            while True:
                streets = get_possible_addresses_by_letter(letter, page_num)
                if streets is not None:
                    output_data[letter].extend(streets)  # Add streets to the list
                else:
                    break  # Exit the loop if no more streets are found
                page_num += 1
        
        json.dump(output_data, jsonfile, ensure_ascii=False, indent=4)  # Write to JSON file
