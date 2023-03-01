# Spot the Bot

This project contains all code segments required to generate the dataset and train a model to identify whether a given text was written by a human or a machine.

## Steps to run the code

1. Create a virtual environment: `python -m venv myenv`
2. Activate the virtual environment: `source myenv/bin/activate`
3. Install the required libraries: `pip install -r requirements.txt`
4. Run the following command to download and preprocess the dataset: `python camel_data.py -i all`
5. Run the processing code to train and evaluate the model: `python process_dataset.py`
