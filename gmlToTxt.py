import re

def convert_edges(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        # Reading the entire file as a single string
        data = f_in.read()
        # Using regular expression to find all matches
        matches = re.findall(r'\[\s*source\s*(\d+)\s*\n\s*target\s*(\d+)\s*\]', data)
        for match in matches:
            source = match[0]
            target = match[1]
            f_out.write(f"{source} {target}\n")

# Replace 'input.txt' and 'output.txt' with your file paths
convert_edges('karate.gml', 'karate.txt')

