# Python - IoT Inventory - Demo RESTful HTTP API

This project shows a demo implementation of a simple IoT device and location inventory through 
an HTTP RESTful API.

The implementation is based on the following Python Frameworks 

- Flask: https://flask.palletsprojects.com/en/2.0.x/
- Flask RESTful: https://flask-restful.readthedocs.io/en/latest/index.html

APIs are exposed through a configurable port (7070) and accessible locally at: 
- http://127.0.0.1:7070/api/iot/
- https://192.168.1.2:7070/api/iot/ - https://192.168.1.10:7070/api/iot/
- https://79.21.207.114:7070/api/iot/

## Modeled REST Resources

The IoT Inventory resources currently modeled are:

- Start Stop Cycke (/start_stop_cycle);
- Recipe Objects Types (/recipe_objects_types);
- Recipe End Effector Indexes (/recipe_end_effector_indexes);
- Recipe Object Types Box Positions (/recipe_object_types_box_positions);
- Recipe Object Types Numbers (/recipe_object_types_numbers);
- Total Bags (/total_bags);
- 6d Pose Estimation (/6d_pose_estimation);
- Selected Recipe (/selected_recipe);
- Placed Objects (/placed_objects);
- Done_bags (/done_bags);
- Current Object (/current_object);
- Cobot State Cycle (/cobot_state_cycle);
- Joints Current Consumption in mA (/joints_current_consumption_ma);
- Joint Temperature in °C (/joints_temperature_c);
- Safety (/safety).

For each resource are available as attributes:
- uuid (Identifier);
- version;
- unit;
- topic;
- qos;
- retained;
- frequency;
- value.




