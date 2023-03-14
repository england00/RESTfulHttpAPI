# Python - IoT Inventory - API HTTP RESTful

This project is a simple implementation of an API HTTP RESTful server, which takes the 
information of all the resource of different remote pick and place systems from a linked 
local MySQL database.

The implementation is based on the following Python Frameworks 
- Flask: https://flask.palletsprojects.com/en/2.0.x/
- Flask RESTful: https://flask-restful.readthedocs.io/en/latest/index.html

The API server is configured with the following parameters (/config/file/database.yaml):
- endpoint_prefix: "/api/iot"
- localhost: "127.0.0.1"
- broadcastIp: "0.0.0.0"
- port: 7070
- ssl_context: "adhoc"
- enable_writing: False

The local database is linked with the following parameters (/config/file/database.yaml):
- host: "localhost"
- user: "MQTT_client"
- password: "HakertzDB64!"
- charset: "utf8"
- chosen_database: "api_database"

There are also other two configuration file:
- /config/file/systems.yaml, giving the right configuration when database is built and also to setting the systems managing data structure, the system mapper;
- /config/file/resources.yaml, giving the right configuration when database is built and also to setting the resources managing data structure, the resource mapper.

## Modeled REST Resources

The resources off all the systems are available at the following topics:
- Start Stop Cycle (endpoint_prefix + "/" + system_name + "/" + "production/cycle/signals/start_stop_cycle");
- Done Bags (endpoint_prefix + "/" + system_name + "/" + "production/cycle/signals/done_bags");
- Total Bags (endpoint_prefix + "/" + system_name + "/" + "production/cycle/signals/total_bags");
- Placed Object (endpoint_prefix + "/" + system_name + "/" + "production/cycle/signals/placed_objects");
- Cycle Time (endpoint_prefix + "/" + system_name + "/" + "production/cycle/time");
- Current Object (endpoint_prefix + "/" + system_name + "/" + "production/cycle/signals/current_object");
- Selected Recipes (endpoint_prefix + "/" + system_name + "/" + "production/cycle/recipes/selected_recipe");
- Recipe Objects Types (endpoint_prefix + "/" + system_name + "/" + "production/cycle/recipes/objects_types");
- Recipe End Effector Indexes (endpoint_prefix + "/" + system_name + "/" + "production/cycle/recipes/end_effector_indexes");
- Recipe Object Types Box Positions (endpoint_prefix + "/" + system_name + "/" + "production/cycle/recipes/object_types_box_positions");
- Recipe Object Types Numbers (endpoint_prefix + "/" + system_name + "/" + "production/cycle/recipes/object_types_numbers");
- Cobot State Cycle (endpoint_prefix + "/" + system_name + "/" + "cobot/states/cobot_state_cycle");
- Robot Mode (endpoint_prefix + "/" + system_name + "/" + "cobot/states/robot_mode");
- Power On Robot (endpoint_prefix + "/" + system_name + "/" + "cobot/states/power_on_robot");
- Safety (endpoint_prefix + "/" + system_name + "/" + "cobot/states/safety");
- Joint Angles (endpoint_prefix + "/" + system_name + "/" + "cobot/joints/sensors/angles");
- Joint Angles Velocities (endpoint_prefix + "/" + system_name + "/" + "cobot/joints/sensors/velocities");
- Joint Current Consumption (endpoint_prefix + "/" + system_name + "/" + "cobot/joints/sensors/current_consumptions");
- Joint Temperatures (endpoint_prefix + "/" + system_name + "/" + "cobot/joints/sensors/temperatures");
- TCP (endpoint_prefix + "/" + system_name + "/" + "cobot/states/tcp");
- 6D Pose Estimation (endpoint_prefix + "/" + system_name + "/" +  "ai_on_edge/inference/6d_pose_estimation");
- Confidence (endpoint_prefix + "/" + system_name + "/" + "ai_on_edge/inference/scores/confidence");
- Cosine Similarity (endpoint_prefix + "/" + system_name + "/" + "ai_on_edge/inference/scores/cosine_similarity");
- Inference Time (endpoint_prefix + "/" + system_name + "/" + "ai_on_edge/inference/time").

For each resource are available the following attributes:
- uuid (Identifier);
- version;
- name;
- unit;
- topic;
- qos;
- retained;
- frequency;
- value;
- picking_system.