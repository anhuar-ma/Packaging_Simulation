include("pacman.jl")
using Genie, Genie.Renderer.Json, Genie.Requests, HTTP
using UUIDs

instances = Dict()

route("/simulations", method=POST) do
    payload = jsonpayload()

    model = initialize_model()
    id = string(uuid1())
    instances[id] = model

    agents = []
    for robots in allagents(model)
        push!(agents, robots)
    end

    sort!(agents, by=x -> x.id)

    save_model_info(model, "model_info.txt")

    json(Dict("Location" => "/simulations/$id", "agents" => agents))
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

    save_model_info(model, "model_info.txt")
    json(Dict("agents" => agents))
end


Genie.config.run_as_server = true
Genie.config.cors_headers["Access-Control-Allow-Origin"] = "*"
Genie.config.cors_headers["Access-Control-Allow-Headers"] = "Content-Type"
Genie.config.cors_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
Genie.config.cors_allowed_origins = ["*"]

up()