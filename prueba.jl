
# Set the PYTHON environment variable to use the specific Conda environment
#Se ejecuta el script de python que nos dira las posiciones de las cajas


# Read the file
lines = readlines("box_positions.txt")

# Process each line
for line in lines
  # Split the line into two parts: the number and the list
  parts = split(line, r"\s*\[\s*|\s*\]\s*")  # Split by [ and ] with optional whitespace
  number = parse(Int, parts[1])  # Convert the first part to an integer
  array = eval(Meta.parse("[" * parts[2] * "]"))  # Convert the second part (the list) to a Julia array

  # println("Number: $number")
  # println("Array: $array")

  # position = array
  # println("Position: $position")

  println(parts[1])
  println(parts[2])
  println(parts[3])
  println("")



  # println("Number: $number, Array: $array")
end
