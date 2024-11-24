include("pacman.jl")
using Genie, Genie.Renderer.Json, Genie.Requests, HTTP
using UUIDs

using Logging

# Set the global logging level to Warn
global_logger(ConsoleLogger(stderr, Logging.Warn))



instances = Dict()

route("/simulations", method=POST) do
    payload = jsonpayload()

    model, pathfinder = initialize_model()
    id = string(uuid1())
    instances[id] = model

    agents = []
    for robots in allagents(model)
        push!(agents, robots)
    end

    sort!(agents, by=x -> x.id)
    # println(size(queue_cajas))


    json(Dict("Location" => "/simulations/$id", "agents" => agents, "queue_front" => first(queue_cajas)))
end

route("/simulations/:id") do
    # println(payload(:id))
    model = instances[payload(:id)]
    run!(model, 1)
    agents = []
    for robots in allagents(model)
        push!(agents, robots)
    end

    sort!(agents, by=x -> x.id)
    if (!isempty(queue_cajas))
        json(Dict("agents" => agents, "queue_front" => first(queue_cajas)))
    else
        json(Dict("agents" => agents, "queue_front" => -1))
    end
    # json(Dict("agents" => agents))
end


Genie.config.run_as_server = true
Genie.config.cors_headers["Access-Control-Allow-Origin"] = "*"
Genie.config.cors_headers["Access-Control-Allow-Headers"] = "Content-Type"
Genie.config.cors_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
Genie.config.cors_allowed_origins = ["*"]

up()