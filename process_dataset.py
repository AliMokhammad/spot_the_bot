"""
## install required packages ##
pip install camel-tools

## get camel tools database ##
camel_data -i all
"""


import os

from utils import prepare_arabic_text, check_dir



## define root folder ##
root_folder = '.'
print(f'root folder is: {root_folder}')

clean_dataset_dir = os.path.join(root_folder,'Clean_Dataset')
drocessed_dataset_dir = os.path.join(root_folder,'Processed_Dataset')

check_dir(clean_dataset_dir)
check_dir(drocessed_dataset_dir)


def process_single_file(j):
    i = 0 + (1300 * j)
    txt_file = os.path.join(clean_dataset_dir,'txt_{}.txt'.format(i))
    print(txt_file)
    with open(txt_file, 'r') as file:
        lines = file.readlines()
    processed_arabic_text, lemmas = prepare_arabic_text(lines)
    print(j, len(lemmas))

    txt_file = os.path.join(drocessed_dataset_dir,'txt_{}.txt'.format(i))
    with open(txt_file, 'w') as file:
        file.write(processed_arabic_text)  

for j in range(1314):
    process_single_file(j)