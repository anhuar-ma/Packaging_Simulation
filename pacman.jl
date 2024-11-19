

using Agents
using CairoMakie
using PyCall

@agent struct Robot(GridAgent{2,})
    type::String = "Robot"
    # direction[1] = 1 up , -1 down ; direction[2] ,1 = foward, -1 = backward
    direction::Vector{Int} = [1, 1]
    #limit , the first value is the first limit, the second the right limit
    limit::NTuple{2,Int} = (0, 0)

    # 90 is up, 270 is down, 0 is right, 180 is left
    looking_at::Int = 0

    finished::Bool = false

    #0 significa no hay una caga, 1 significa que vamos a acomodar una caga y el 2
    #que estamos regresando a nuestra posición inical
    found_box::Int = 0

    #Past postiion para poder ir a dejar la caja y regresar a la posición anterior
    past_position::Vector{Int} = [-1, -1]
    #movientos de robot
    movimientos::Int = 0
end


@agent struct Box(GridAgent{2})
    type::String = "Box"
    #tiene dimensiones
    dimension::Vector{Int} = [1, 1, 1]
    ordered_position::Vector{Int} = [1, 1, 1]
end

@agent struct Estante(GridAgent{2})
    type::String = "Estante"
    cantidad_cajas::Int = 0
end

function agent_step!(agent::Box, model)
    # print(agent.pos)
end
function agent_step!(agent::Estante, model)
    # print(agent.pos)
end

function agent_step!(agent::Robot, model)
    if agent.finished && agent.found_box == 0
        return
    else
        # print(agent.pos)
        #Cada movimento voy a buscar la id del estante y le voy a sumar uno al contador

        agent.movimientos += 1

        if agent.found_box > 0

            #Si ya encontró la caja, entonces la lleva a la posición 49, 49
            if agent.found_box == 1
                if (agent.pos[1] < 50)
                    agent.direction[1] = 1
                    move_agent!(agent, (agent.pos[1] + 1, agent.pos[2]), model)


                    #durante este trayecto hacia arriba, el robot va a estar viendo hacia arriba
                    agent.looking_at = 90

                else

                    #Se agrega caja a estante
                    #se busca la id del estante
                    agents_at_pos = agents_in_position((1, 1), model)
                    estante_id = -1
                    for agent_in_pos in agents_at_pos
                        if agent_in_pos.type == "Estante"
                            estante_id = agent_in_pos.id
                            # println("---------------------------------")
                        end
                    end

                    model[estante_id].cantidad_cajas += 1

                    agent.found_box = 2

                end
            elseif agent.found_box == 2

                if (agent.pos[1] > agent.past_position[1])
                    agent.direction[1] = -1
                    #Si ya llegó a la posición 50 entonces regresa a la posición anterior

                    move_agent!(agent, (agent.pos[1] - 1, agent.pos[2]), model)

                    #durante este trayecto de regresar a su anterior posición, el robot va a estar viendo hacia abajo
                    agent.looking_at = 270
                else
                    agent.found_box = 0
                    # agent.past_position = [-1, -1]
                end

            end


        else

            # randomwalk!(agent, model)
            # Determine the new position
            # y is 1 and x is 2

            #checking if is in the limits of y
            #if i'm going down and I have reach 1,the floor, then go up
            if (agent.pos[1] == 1 && agent.direction[1] == -1)
                agent.direction[1] = 1
                #if i'm going up and I have reach 50, then go down
            elseif (agent.pos[1] == 50 && agent.direction[1] == 1)
                agent.direction[1] = -1
            end


            new_pos = agent.pos
            # Checar si esta en los límites de x
            # Si choco con los límites cambiar la dirección
            if (agent.pos[2] == agent.limit[1] && agent.direction[2] == -1) || (agent.pos[2] == agent.limit[2] && agent.direction[2] == 1)
                agent.direction[2] *= -1
                # agent.move = true

                #si llege al limite me voy a mover hacia arriba o hacia abajo

                if agent.direction[1] == 1
                    agent.looking_at = 90
                else
                    agent.looking_at = 270
                end

                new_pos = (agent.pos[1] + (1 * agent.direction[1]), agent.pos[2])
            else

                #si no estoy en el limite entonces me muevo hacia la dirección que estoy viendo

                if agent.direction[2] == 1
                    agent.looking_at = 0
                else
                    agent.looking_at = 180
                end

                new_pos = (agent.pos[1], agent.pos[2] + agent.direction[2])
            end


            #Verificar si hay una caja en la posición en la que estamos
            for box in nearby_agents(agent, model, 1)
                if box.type == "Box"
                    # println("Hay una caja en la posición: ", agent.pos)
                    remove_agent!(box, model)
                    agent.found_box = true
                    agent.past_position = [agent.pos[1], agent.pos[2]]
                end
            end


            # Mover el agente a la nueva posición
            move_agent!(agent, new_pos, model)

        end



    end

    if agent.pos[1] == 1 && agent.pos[2] == agent.limit[1]
        agent.finished = true
    end

end

function initialize_model()
    # Se crea una grid de 50x50
    space = GridSpace((50, 50); periodic=false, metric=:manhattan)
    model = StandardABM(Union{Robot,Box,Estante}, space; agent_step!)
    #Se agregan los robots
    #Supongamos que solo hay uno
    add_agent!(Robot, limit=(1, 10), direction=[1, -1], pos=(50, 1), model)
    add_agent!(Robot, limit=(11, 20), direction=[1, -1], pos=(50, 11), model)
    add_agent!(Robot, limit=(21, 30), direction=[1, -1], pos=(50, 21), model)
    add_agent!(Robot, limit=(31, 40), direction=[1, -1], pos=(50, 31), model)
    add_agent!(Robot, limit=(41, 50), direction=[1, -1], pos=(50, 41), model)

    # #Se agregan las cajas

    for i in 1:10
        add_agent!(Box, pos=(rand(1:50), rand(1:50)), model)
    end
    #Se agrega el estante teniendo la ultima id
    add_agent!(Estante, pos=(1, 1), model)

    #Se crean aleatoramiente las dimiensiones de las cajas
    for box in allagents(model)
        if box.type == "Box"
            box.dimension = [rand(1:5), rand(1:5), rand(1:5)]
        end
    end

    open("box_dimensions.txt", "w") do file
        # Iterate through the box and send the dimensions to the file
        for agent in allagents(model)
            if (agent.type == "Box")
                print(file, "$(agent.id) ")
                println(file, agent.dimension)
                # println(file)  # Blank line for readability
            end
            # println(file)  # Blank line for readability
        end
    end
    #Se ejecuta el script de python que nos dira las posiciones de las cajas

    #se declara el ejecutable de python
    python_executable = "/home/anhuar/anaconda3/envs/my_anaconda_env/bin/python"

    #se ejecuta el script de python
    run(`$python_executable myexample.py`)




    # Read the file created by the python script
    lines = readlines("box_dimensions.txt")

    # Process each line
    for line in lines
        # Split the line into two parts: the number and the list
        parts = split(line, r"\s+\[")  # Split by whitespace followed by [

        #parts[1] is the id of the box
        println(parts[1])
        #position is the orderede position of the box
        position = eval(Meta.parse("[" * parts[2]))
        println(position)
        model[parse(Int, parts[1])].ordered_position = position

        # println("Number: $number, Array: $array")
    end



    return model
end

