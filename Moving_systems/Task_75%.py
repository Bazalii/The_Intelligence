from Moving_systems.Manipulator_class import Manipulator
# Markers
Marker_Center = None
Radius_Vector_of_Marker = None
Size_of_Marker = None
# OBJECTS
# Platform
Platform_Marker_1_id = None
Platform_Marker_2_id = None
Platform_Center = None
Platform_Length_between_Markers = None
Platform_Height_of_Capture = None
Platform_Deflection_Angle = None
# Motor_1
Motor_1_Marker_1_id = None
Motor_1_Marker_2_id = None
Motor_1_Center = None
Motor_1_Length_between_Markers = None
Motor_1_Height_of_Capture = None
Motor_1_Deflection_Angle = None
# Motor_2
Motor_2_Marker_1_id = None
Motor_2_Marker_2_id = None
Motor_2_Center = None
Motor_2_Length_between_Markers = None
Motor_2_Height_of_Capture = None
Motor_2_Deflection_Angle = None
# Motor_3
Motor_3_Marker_1_id = None
Motor_3_Marker_2_id = None
Motor_3_Center = None
Motor_3_Length_between_Markers = None
Motor_3_Height_of_Capture = None
Motor_3_Deflection_Angle = None
# Motor_4
Motor_4_Marker_1_id = None
Motor_4_Marker_2_id = None
Motor_4_Center = None
Motor_4_Length_between_Markers = None
Motor_4_Height_of_Capture = None
Motor_4_Deflection_Angle = None
# Electronic_module
Electronic_module_Marker_1_id = None
Electronic_module_Marker_2_id = None
Electronic_module_Center = None
Electronic_module_Length_between_Markers = None
Electronic_module_Height_of_Capture = None
Electronic_module_Deflection_Angle = None
# Top_part
Top_part_Marker_1_id = None
Top_part_Marker_2_id = None
Top_part_Center = None
Top_part_Length_between_Markers = None
Top_part_Height_of_Capture = None
Top_part_Deflection_Angle = None
# Table
Table_Size = None
Table_Start_Point = None
# Head
Head_Camera_Legnth = None
Head_Length_from_Start_Point_to_Capture_point = None
#Points for 75% Task
Motor_1_x_pick = None
Motor_1_y_pick = None
Motor_1_z_pick = None
Motor_1_angle_pick = None
Motor_1_x = None
Motor_1_y = None
Motor_1_z = None
Motor_1_angle = None
Motor_2_x_pick = None
Motor_2_y_pick = None
Motor_2_z_pick = None
Motor_2_angle_pick = None
Motor_2_x = None
Motor_2_y = None
Motor_2_z = None
Motor_2_angle_pick = None
Motor_3_x_pick = None
Motor_3_y_pick = None
Motor_3_z_pick = None
Motor_3_angle = None
Motor_3_x = None
Motor_3_y = None
Motor_3_z = None
Motor_3_angle = None
Motor_4_x_pick = None
Motor_4_y_pick = None
Motor_4_z_pick = None
Motor_4_angle_pick = None
Motor_4_x = None
Motor_4_y = None
Motor_4_z = None
Motor_4_angle = None
Electronic_module_x_pick = None
Electronic_module_y_pick = None
Electronic_module_z_pick = None
Electronic_module_angle_pick = None
Electronic_module_x = None
Electronic_module_y = None
Electronic_module_z = None
Electronic_module_angle = None
Top_part_x_pick = None
Top_part_y_pick = None
Top_part_z_pick = None
Top_part_angle_pick = None
Top_part_x = None
Top_part_y = None
Top_part_z = None
Top_part_angle = None
# ---------------------------------------------------------------------------------------------------#

manipulator = Manipulator()
manipulator.set_zero()
manipulator.move_to_point(Motor_1_x_pick, Motor_1_y_pick)
manipulator.move_to_point(Motor_1_z_pick)
manipulator.pick()
manipulator.move_to_point(Motor_1_x, Motor_1_y)
manipulator.move_to_point(Motor_1_z)
manipulator.setup()
manipulator.move_to_point(Motor_2_x_pick, Motor_2_y_pick)
manipulator.move_to_point(Motor_2_z_pick)
manipulator.pick()
manipulator.move_to_point(Motor_2_x, Motor_2_y)
manipulator.move_to_point(Motor_2_z)
manipulator.setup()
manipulator.move_to_point(Motor_3_x_pick, Motor_3_y_pick)
manipulator.move_to_point(Motor_3_z_pick)
manipulator.pick()
manipulator.move_to_point(Motor_3_x, Motor_3_y)
manipulator.move_to_point(Motor_3_z)
manipulator.setup()
manipulator.move_to_point(Motor_4_x_pick, Motor_4_y_pick)
manipulator.move_to_point(Motor_4_z_pick)
manipulator.pick()
manipulator.move_to_point(Motor_4_x, Motor_4_y)
manipulator.move_to_point(Motor_4_z)
manipulator.setup()
manipulator.move_to_point(Electronic_module_x_pick, Electronic_module_y_pick)
manipulator.move_to_point(Electronic_module_z_pick)
manipulator.pick()
manipulator.move_to_point(Electronic_module_x, Electronic_module_y)
manipulator.move_to_point(Electronic_module_z)
manipulator.setup()
manipulator.move_to_point(Top_part_x_pick, Top_part_y_pick)
manipulator.move_to_point(Top_part_z_pick)
manipulator.pick()
manipulator.move_to_point(Top_part_x, Top_part_y)
manipulator.move_to_point(Top_part_z)
manipulator.setup()