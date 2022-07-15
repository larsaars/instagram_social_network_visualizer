"""
execute all scripts at once
"""

import os

# create .env file
ig_user = input('Enter your IG username: ')
ig_pass = input('Enter your IG password: ')

with open('.env', 'w') as f:
    f.write(f'''
    IG_USERNAME={ig_user}
    IG_PASSWORD={ig_pass}
    ANALYZE_DEPTH=2
    MAX_FOLLOWERS=1000''')

# install requirements
os.system('python3 -m pip install -r requirements.txt')
# load instagram network
os.system('python3 load_network.py')
# analyze network
os.system('python3 analyzer.py')
# inform user
print('Import edges.csv in a software like Gephi')
