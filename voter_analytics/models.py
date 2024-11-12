# blog/models.py
# Definte the data objects for our application
from django.db import models
from tqdm import tqdm

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data for Voters
    '''
    # identification
    id = models.TextField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    dob = models.TextField()
    dor = models.TextField()
    precinct = models.TextField()
    party = models.TextField()
    voter_score = models.IntegerField()


    # address
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment = models.TextField(default=None)
    zip = models.IntegerField()


    # participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)



    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} (Party: {self.party}, {self.precinct}), {self.dor}'
        # return (f'first_name: {self.first_name} \n'
        #     f'last_name: {self.last_name}\n'
        #     f'dob: {self.dob} \n'
        #     f'dor: {self.dor}\n'
        #     f'precinct: {self.precinct}\n'
        #     f'party: {self.party}\n'
        #     f'street_number: {self.street_number} \n'
        #     f'street_name: {self.street_name}\n'
        #     f'apartment: {self.apartment}\n'
        #     f'zip: {self.zip}\n'
        #     f'v20state: {self.v20state} \n'
        #     f'v21town: {self.v21town}\n'
        #     f'v21primary: {self.v21primary}\n'
        #     f'v22general: {self.v22general}\n'
        #     f'v23town: {self.v23town}\n'
        #     f'voter_score: {self.voter_score}\n')

    

def load_data():
    '''Load data records from a CSV file into model instances.'''
    # Delete all records: clear out the database
    Voter.objects.all().delete()

    filename = "C:\\Users\\Anna\\Downloads\\cs412\\newton_voters.csv"
    f = open(filename)

    f.readline() # read/discard the headers

    total_lines = sum(1 for line in open(filename)) - 1  

    for line in tqdm(f, total=total_lines, desc="Loading Voters"):
        try:
            fields = line.split(',')  # Create a list of fields
            # print(f"Attempting to insert: {fields}")

            result = Voter(
                id=fields[0],
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3] ,
                street_name=fields[4],
                apartment=fields[5],
                zip=fields[6],
                dob=fields[7],
                dor=fields[8],
                party=fields[9],
                precinct=fields[10],
                v20state=fields[11].strip().upper() == 'TRUE',
                v21town=fields[12].strip().upper() == 'TRUE',
                v21primary=fields[13].strip().upper() == 'TRUE',
                v22general=fields[14].strip().upper() == 'TRUE',
                v23town=fields[15].strip().upper() == 'TRUE',
                voter_score=fields[16],
            )

            result.save()  # Commit to the database
            # print(f'Created result: {result}')
        
        except Exception as e:
            print(f"Exception on {fields}: {e}")
