def obj_to_txt(input_obj_file, output_txt_file):
    with open(input_obj_file, 'r') as obj_file:
        with open(output_txt_file, 'w') as txt_file:
            for line in obj_file:
                if line.startswith('v '):  # Check if the line represents a vertex
                    # Extract the vertex coordinates
                    _, x, y, z = line.strip().split()
                    # Write the coordinates to the .txt file, formatted to five decimal places
                    txt_file.write(f"{float(x):.5f} {float(y):.5f} {float(z):.5f}\n")

# Example usage:
input_obj_file = 'path/to/your/input.obj'
output_txt_file = 'path/to/your/output.txt'

obj_to_txt(input_obj_file, output_txt_file)
