from councils.edinburgh import get_possible_addresses_by_letter

def get_edinburgh_streets():
    alphabet = list(map(chr, range(97, 123)))
    page_num = 1

    with open('data/edin_streets.csv', 'w', newline='') as csvfile:
        for letter in alphabet:
            while True:
                streets = get_possible_addresses_by_letter(letter, page_num)
                if streets != None:
                    for street in streets:
                        csvfile.write(street + '\n')
                if streets == None:
                    page_num = 1
                    break
                print(streets)
                page_num += 1