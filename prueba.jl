
# Set the PYTHON environment variable to use the specific Conda environment
#Se ejecuta el script de python que nos dira las posiciones de las cajas

python_executable = "/home/anhuar/anaconda3/envs/my_anaconda_env/bin/python"
run(`$python_executable myexample.py`)




# # Read the file
# lines = readlines("box_dimensions.txt")

# # Process each line
# for line in lines
#   # Split the line into two parts: the number and the list
#   parts = split(line, r"\s+\[")  # Split by whitespace followed by [
#   # number = parse(Int, parts[>1])  # Convert the first part to an integer
#   # array = eval(Meta.parse(parts[2]))  # Convert the second part (the list) to a Julia array

#   println(parts[1])
#   # println("[" * parts[2])

#   position = eval(Meta.parse("[" * parts[2]))
#   println(position)

#   # println("Number: $number, Array: $array")
# end
