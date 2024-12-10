

using Agents, Agents.Pathfinding
using CairoMakie
using PyCall
using DataStructures
queue_cajas = Queue{Int}()
queue_cajas_checador = Queue{Int}()
n_grid_model_size = [100, 100]

@agent struct Robot(GridAgent{2})
    type::String = "Robot"
    # direction[1] = 1 up , -1 down ; direction[2] ,1 = foward, -1 = backward
    direction::Vector{Int} = [1, 1]
    #limit , the first value is the first limit, the second the right limit
    limit::NTuple{2,Int} = (0, 0)

    # 90 is up, 270 is down, 0 is right, 180 is left
    angle::Int = 0

    finished::Bool = false

    #0 significa no hay una caga, 1 significa que vamos a encontrar una caga,el 2 que estamos recojiendo la caja y el 3 que estamos acomondando la caja y el 4 que estamos dejando la caja
    state::Int = 0

    #Past postiion para poder ir a dejar la caja y regresar a la posición anterior
    past_position::Vector{Int} = [-1, -1]
    #movientos de robot
    movimientos::Int = 0

    objective_position::Vector{Int} = [50, 1]

    #la caja que el robot esta manipulando
    box_id::Int = -1

    #counter para las iteraciones
    platformHeight::Int = -150
end


@agent struct Box(GridAgent{2})
    type::String = "Box"
    #tiene dimensiones
    dimension::Vector{Int} = [1, 1, 1]
    ordered_position::Vector{Int} = [1, 1, 1]
    #si la caja va a ser manejada por un robot, es la id del robot
    # robot_id::Int = 0
    #rotacion de la caja dadaba por package bin
    rotation::Int = 0

end


#Hacer que el estante guarde una variable que permita decir cuantas cajas tiene
@agent struct Contenedor(GridAgent{2})
    type::String = "Contenedor"
    cantidad_cajas::Int = 0
    position::Vector{Int} = [0, 0]
    dimension::Vector{Int} = [1, 1, 1]
end

function agent_step!(agent::Box, model)
    # print(agent.pos)
end
function agent_step!(agent::Contenedor, model)
    # print(agent.pos)
end




function find_safe_position(agent, next_pos_robot, current_robot_pos, model)
    # Calculate the direction of the robot's movement
    direction = (next_pos_robot[1] - current_robot_pos[1], next_pos_robot[2] - current_robot_pos[2])

    # Determine a list of potential safe positions based on the direction
    potential_safe_positions = []
    if direction == (1, 0)  # Moving right
        push!(potential_safe_positions, (agent.pos[1], agent.pos[2] - 1))  # Move down
        push!(potential_safe_positions, (agent.pos[1], agent.pos[2] + 1))  # Move up
        push!(potential_safe_positions, (agent.pos[1] - 1, agent.pos[2]))  # Move left
        push!(potential_safe_positions, (agent.pos[1] + 1, agent.pos[2]))  # Move right
    elseif direction == (-1, 0)  # Moving left
        push!(potential_safe_positions, (agent.pos[1], agent.pos[2] + 1))  # Move up
        push!(potential_safe_positions, (agent.pos[1], agent.pos[2] - 1))  # Move down
        push!(potential_safe_positions, (agent.pos[1] - 1, agent.pos[2]))  # Move left
        push!(potential_safe_positions, (agent.pos[1] + 1, agent.pos[2]))  # Move right
    elseif direction == (0, 1)  # Moving up
        push!(potential_safe_positions, (agent.pos[1] - 1, agent.pos[2]))  # Move left
        push!(potential_safe_positions, (agent.pos[1] + 1, agent.pos[2]))  # Move right
        push!(potential_safe_positions, (agent.pos[1], agent.pos[2] - 1))  # Move down
        push!(potential_safe_positions, (agent.pos[1], agent.pos[2] + 1))  # Move up
    elseif direction == (0, -1)  # Moving down
        push!(potential_safe_positions, (agent.pos[1] + 1, agent.pos[2]))  # Move right
        push!(potential_safe_positions, (agent.pos[1] - 1, agent.pos[2]))  # Move left
        push!(potential_safe_positions, (agent.pos[1], agent.pos[2] + 1))  # Move up
        push!(potential_safe_positions, (agent.pos[1], agent.pos[2] - 1))  # Move down
    else
        push!(potential_safe_positions, agent.pos)  # No movement, stay in the current position
    end

    # Check if the potential safe positions are within the limits of the model
    for safe_pos in potential_safe_positions
        if safe_pos[1] >= 1 && safe_pos[1] <= n_grid_model_size[1] && safe_pos[2] >= 1 && safe_pos[2] <= n_grid_model_size[2]
            return safe_pos
        end
    end

    return agent.pos  # If no valid safe position is found, stay in the current position
end



# Move the agent along the route and update its rotation
function move_along_route_with_angle!(agent::Robot, model, pathfinder)


    move_along_route_bool = true
    past_pos = agent.pos

    if (!isempty(pathfinder.agent_paths[agent.id]))
        #obtenemos la siguient posicion en la ruta
        next_pos = first(pathfinder.agent_paths[agent.id])

        for robot in agents_in_position(next_pos, model)
            #si hay un robot en la siguiente posicion y no es el mismo robot y el id del robot es mayor
            if robot.type == "Robot" && robot.id != agent.id && agent.id > robot.id
                #Tengo que moverme a un lugar en donde no este en la ruta del otro robot
                next_pos_robot = (0, 0)
                if (!isempty(pathfinder.agent_paths[robot.id]))
                    next_pos_robot = first(pathfinder.agent_paths[robot.id])
                    current_robot_pos = robot.pos

                    safe_pos = find_safe_position(agent, next_pos_robot, current_robot_pos, model)

                    if (safe_pos != agent.pos)
                        # Move the agent to the safe position
                        move_agent!(agent, safe_pos, model)
                        println("--------HOLAAAAAA-----------------------------------")
                        move_along_route_bool = false
                    end
                end


                println(agent.id)
                break
            end
        end

    end

    if move_along_route_bool || (!isempty(pathfinder.agent_paths[agent.id]))
        move_along_route!(agent, model, pathfinder)
    end

    dx = agent.pos[1] - past_pos[1]
    dy = agent.pos[2] - past_pos[2]
    if dx == -1
        agent.angle = 0   # Right
    elseif dx == 1
        agent.angle = 180 # Left
    elseif dy == 1
        agent.angle = 90  # Up
    elseif dy == -1
        agent.angle = 270 # Down
    end


end



function agent_step!(agent::Robot, model)
    # println("fuaaaaaaaaaaaaa")
    # println("agent.state")
    # println(agent.state)
    #Se esta buscando una caja para recoger
    deltaHeight = 2
    if agent.state == 0
        #Se busca la caja de la queue(la caja que sigue)
        if (!isempty(queue_cajas))
            #Cambio de lugar a que se elimine de la pila cuando se recoja
            box = model[dequeue!(queue_cajas)]
            # box = model[first(queue_cajas)]
            agent.state = 1
            agent.objective_position = collect(box.pos)
            # box.robot_id = agent.id
            agent.box_id = box.id
            println("------------------------------------")
            println("Box")
            println(box.id)
            println(box.pos)
            plan_route!(agent, box.pos, pathfinder)
        end
    elseif agent.state == 1
        #si ya encontró la caja, se mueve a ella
        move_along_route_with_angle!(agent, model, pathfinder)

        #si ya llegó a la caja se cambia de estado y se elimina la caja
        # println("agent pos")
        # println(agent.pos)
        # println("objective pos")
        # println(agent.objective_position)

        if agent.pos[1] == agent.objective_position[1] && agent.pos[2] == agent.objective_position[2]
            agent.state = 2
            agent.objective_position = [1, 60 - ((agent.id - 1) * 5)] #Aquí deja las cajas
            remove_agent!(model[agent.box_id], model)
            # dequeue!(queue_cajas)
            plan_route!(agent, (agent.objective_position[1], agent.objective_position[2]), pathfinder)
            #la box id cambia a -1
            # agent.box_id = -1
        end
        #Se esta recogiendo la caja, levantanto la plataforma
    elseif agent.state == 2

        if agent.platformHeight >= 0
            agent.state = 3
        else
            agent.platformHeight += deltaHeight
        end
        #Se esta moviendo la caja a su posicion ordenada,es decir al camion
    elseif agent.state == 3
        #si ya encontró la caja, se mueve al carro para ordenarla
        move_along_route_with_angle!(agent, model, pathfinder)
        #si ya se llego al estante, se cambia de estado
        if agent.pos[1] == agent.objective_position[1] && agent.pos[2] == agent.objective_position[2] && agent.box_id == first(queue_cajas_checador)
            agent.state = 4
            dequeue!(queue_cajas_checador)
            agent.angle = 0
        end
        # println("algoooooooooooo")
        #estado 4 Se va a dejar caer la caja,bajando la plataforma
    else
        agent.angle = 0
        if agent.platformHeight <= -150
            agent.state = 0
        else
            agent.platformHeight -= deltaHeight
        end

    end
end



function initialize_model()
    # Se crea una grid de 50x50

    grid_n = 100 #Espacio del Grid
    grid = trues(grid_n, grid_n)
    space = GridSpace((grid_n, grid_n); periodic=false, metric=:manhattan)
    model = StandardABM(Union{Robot,Box,Contenedor}, space; agent_step!)
    #Se agregan los robots
    #Supongamos que solo hay uno
    add_agent!(Robot, limit=(1, 10), direction=[1, -1], pos=(100, 1), model)
    add_agent!(Robot, limit=(1, 10), direction=[1, -1], pos=(99, 1), model)
    add_agent!(Robot, limit=(1, 10), direction=[1, -1], pos=(98, 1), model)
    add_agent!(Robot, limit=(1, 10), direction=[1, -1], pos=(97, 1), model)
    add_agent!(Robot, limit=(1, 10), direction=[1, -1], pos=(96, 1), model)

    # #Se agregan las posiciones de las cajas
    x = rand(2:grid_n-1)
    y = rand(2:grid_n-1)

    lista_caja = [[1, 1, 1], [5, 5, 5], [7, 7, 7]]


    for i in 1:20
        while length((ids_in_position((x, y), model))) > 0
            x = rand(2:grid_n-1)
            y = rand(2:grid_n-1)
        end
        add_agent!(Box, pos=(x, y), model)
        println("Box pos", x, " ", y)
    end

    println("ids in 1,1")
    println(length((ids_in_position((1, 1), model))))

    #Se agrega el estante teniendo la ultima id
    #(W,H,D)
    #W = ancho
    #H = alto
    #D = largo

    add_agent!(Contenedor, model, position=[-30, 39], dimension=[30, 20, 22])

    #TODO: dar opciones de cajas en vez de random
    #Se crean aleatoramiente las dimiensiones de las cajas
    for box in allagents(model)
        if box.type == "Box"
            #dimensiones aletorias
            box.dimension = [rand(3:7), rand(3:7), rand(3:7)]

            #dimensiones del socio
            # box.dimension = lista_caja[rand(1:3)]

            #para indicar que el robot no pueda pasar por la caja
            grid[box.pos[1], box.pos[2]] = false
        end
    end

    # add_agent!(Box, pos=(1, 1), dimension=[20, 30, 10], model)

    pathfinder = AStar(space; walkmap=grid, diagonal_movement=false)
    # pathfinder = AStar(space; diagonal_movement=false)

    open("box_dimensions.txt", "w") do file
        # Iterate through the box and send the dimensions to the file
        for agent in allagents(model)
            if (agent.type == "Contenedor")
                print(file, agent.type, " ")
                print(file, agent.id, " ")
                println(file, agent.dimension)
            end
        end
        for agent in allagents(model)
            if (agent.type == "Box")
                print(file, "$(agent.id) ")
                println(file, agent.dimension)
            end
        end
    end
    #Se ejecuta el script de python que nos dira las posiciones de las cajas

    #se declara el ejecutable de python
    python_executable = "/home/anhuar/anaconda3/envs/my_anaconda_env/bin/python"
    # python_executable

    #se ejecuta el script de python
    run(`$python_executable main.py`)




    # Read the file created by the python script
    lines = readlines("box_positions.txt")

    #Se crea una queue para guardar el orden de las cajas

    global queue_cajas, queue_cajas_checador


    empty!(queue_cajas)
    empty!(queue_cajas_checador)

    # Process each line
    for line in lines
        # Split the line into two parts: the number and the list

        parts = split(line, r"\s*\[\s*|\s*\]\s*")  # Split by [ and ] with optional whitespace

        # println(parts)
        #parts[1] is the id of the box
        println(parts[1])
        enqueue!(queue_cajas, parse(Int, parts[1]))
        enqueue!(queue_cajas_checador, parse(Int, parts[1]))
        #position is the orderede position of the box
        position = eval(Meta.parse("[" * parts[2] * "]"))  # Convert the second part (the list) to a J
        println(position)
        model[parse(Int, parts[1])].ordered_position = [position[1], position[3], position[2]]

        #rotatcion de la caja, que se la 3 parte
        model[parse(Int, parts[1])].rotation = parse(Int, parts[3])
        # println("Number: $number, Array: $array")
    end
    #=
    Queue cajas checador es una copia de queue cajas que usaremos para saber si
    la caja que tenemos es la que sigue, si no , esperamos a que sea
    =#
    # println(grid)
    return model, pathfinder
end

model, pathfinder = initialize_model()

