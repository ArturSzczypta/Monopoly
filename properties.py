import csv

# Create Property class
class Property:
    def __init__(self, number, names, set_name, in_set, price, mortgage, rent, buildinng_cost, house_1, houses_2, houses_3, houses_4, hotel):
        self.number = number
        self.names = names
        self.set = set_name
        self.in_set = in_set
        self.price = price
        self.mortgage = mortgage
        self.base_rent = rent
        self.rent = rent
        self.buildinng_cost = buildinng_cost
        self.house_1 = house_1
        self.houses_2 = houses_2
        self.houses_3 = houses_3
        self.houses_4 = houses_4
        self.hotel = hotel
        self.status = 0 # All: 0 - not full set, 1 - full set, -1 - morgaged
        # Station: 0 - 1 station, 0.33 - 2 stations, 0.67 - 3 stations, 1 - 4 stations
        # Utility: 0 - 1 utility, 1 - 2 utilities
        # Preperties: 1.25 - 1 house, 1.5 - 2 houses, 1.75 - 3 houses, 2 - 4 houses, 3 - hotel
        self.owner = None

    def details(self):
        ''' Return all property attributes as a dictionary'''
        return vars(self)
    
    def buy(self, player):
        '''Buy property if player has enough funds'''
        if self.price <= player.funds:
            self.owner = player.number
            player.funds -= self.price
    
    def change_owner(self, player, buyer):
        '''Change property owner'''
        if self.owner == player.number:
            self.owner = buyer.number
            player.properties -= 1
            buyer.properties += 1
        else:
            print('unable to change owner')
    
    def morgage(self, player):
        '''Morgage property if player has enough funds'''
        if self.status != -1:
            self.status = -1
            player.funds += self.mortgage
        else:
            player('unable to morgage')
    
    def unmorgage(self, player):
        '''Unmorgage property if player has enough funds'''
        if self.status == -1 and player.funds >= self.mortgage:
            self.status = 0
            player.funds -= self.mortgage
        else:
            print('unable to unmorgage')

    def calculate_rent(self, dice_roll):
        '''Calculate rent for property'''
        if self.set == 'Station':
            if self.status == 0:
                self.rent = 25
            elif self.status == 0.33:
                self.rent = 100
            elif self.status == 0.67:
                self.rent = 150
            elif self.status == 1:
                self.rent = 200
        elif self.set == 'Utility':
            if self.status == 0:
                self.rent = dice_roll * 4
            elif self.status == 1:
                self.rent = dice_roll * 10
        else:
            # Streets
            if self.status > 0 and self.status < 1:
                self.rent = self.base_rent
            elif self.status == 1:
                self.rent == self.base_rent * 2
            elif self.status == 1.25:
                self.rent = self.house_1
            elif self.status == 1.5:
                self.rent = self.houses_2
            elif self.status == 1.75:
                self.rent = self.houses_3
            elif self.status == 2:
                self.rent = self.houses_4
            elif self.status == 3:
                self.rent = self.hotel
        if self.status == -1:
                self.rent = 0

def field_list(dice_roll=None):
    '''Create list of all fields'''
    # Create list of 40 fields
    fields = [None] * 40
    fields[0] = 'Start'
    fields[10] = 'Jail'
    fields[20] = 'Free Parking'
    fields[30] = 'Go to Jail'
    fields[2] = 'Community Chest'
    fields[17] = 'Community Chest'
    fields[33] = 'Community Chest'
    fields[7] = 'Chance'
    fields[22] = 'Chance'
    fields[36] = 'Chance'
    fields[4] = 'Income Tax'
    fields[38] = 'Luxury Tax'

    # Save properties.csv content list of dictionaries
    with open('properties.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_dict = {header: value for header, value in row.items()}
            fields[int(row_dict['number'])] = Property(**row_dict)
    return fields

if __name__ == '__main__':
    # Print all fields
    fields = field_list()
    for field in fields:
        print(type(field))
        if isinstance(field, Property):
            print(field.details())
        else:
            print(field)
        print('-' * 20)
