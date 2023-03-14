# Python - IoT Inventory - API HTTP RESTful

This project is a simple implementation of an API HTTP RESTful linked to a MySQL database, 
which stores all the resources an of different pick and place systems and location inventory through 
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

- Start Stop Cycle (/production/cycle/signals/start_stop_cycle);
- Done Bags (/production/cycle/signals/done_bags);
- Done Bag (/production/cycle/signals/done_bag);
- Total Bags (/production/cycle/signals/total_bags);
- Placed Object (/production/cycle/signals/placed_objects);
- Actual Done Bags (/production/cycle/signals/actual_done_bags);
- Actual Lost Objects (/production/cycle/signals/actual_lost_objects);
- Cycle Time (/production/cycle/time);
- Current Object (/production/cycle/signals/current_object);
- Selected Recipes (/production/cycle/recipes/selected_recipe);
- Recipe Objects Types (/production/cycle/recipes/objects_types);
- Recipe End Effector Indexes (/production/cycle/recipes/end_effector_indexes);
- Recipe Object Types Box Positions (/production/cycle/recipes/object_types_box_positions);
- Recipe Object Types Numbers (/production/cycle/recipes/object_types_numbers);
- Cobot State Cycle (/cobot/states/cobot_state_cycle);
- Robot Mode (/cobot/states/robot_mode);
- Power On Robot (/cobot/states/power_on_robot);
- Safety (/cobot/states/safety);
- Alarm Counter (/cobot/states/alarm_counter);
- Joint Angles (/cobot/joints/sensors/angles);
- Joint Angles Velocities (/cobot/joints/sensors/velocities);
- Joint Current Consumption (/cobot/joints/sensors/current_consumptions);
- Joint Temperatures (/cobot/joints/sensors/temperatures);
- TCP (/cobot/states/tcp);
- 6D Pose Estimation (/ai_on_edge/inference/6d_pose_estimation);
- Request 6D Pose Estimation (/ai_on_edge/inference/request_6d_pose_estimation);
- Confidence (/ai_on_edge/inference/scores/confidence);
- Cosine Similarity (/ai_on_edge/inference/scores/cosine_similarity);
- Inference Time (/ai_on_edge/inference/time);
- RGB Image (/ai_on_edge/image/rgb_image);
- Detection Image (/ai_on_edge/image/detection_image);
- GD Pose Estimation Image (/ai_on_edge/image/6d_pose_estimation_image);
- Picking Point Image (/ai_on_edge/image/picking_point_image);

For each resource are available as attributes:
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