import json

def extract_elements(input_file, output_file, n):
    # Read the given JSON file
    with open(input_file, 'r') as infile:
        data = json.load(infile)
    # Extract the first n elements
    extracted_data = data[:n]
    # Write the extracted data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(extracted_data, outfile, indent=2)

# The input JSON file
input_file = 'twitter_responses_2560.json'

# The target numbers of elements to extract
target_nums = [5, 10, 20, 40, 80, 160, 320, 640, 1280, 1500, 2560]
for i in target_nums:
    output_file = f'twitter_responses_{i}.json'
    extract_elements(input_file, output_file, i)
