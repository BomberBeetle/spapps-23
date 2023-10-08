extends Node3D

@export var speed = 0.25;
# Called when the node enters the scene tree for the first time.
func _ready():

	var SpatialObject = load("res://SpatialObject.tscn")
	
	var json_text = FileAccess.get_file_as_string("res://objects.json");
	var objs_dict = JSON.parse_string(json_text);
	var min_x = 999999999999;
	var max_x = 0;
	var min_y = 999999999999;
	var max_y = 0;
	for obj_idx in objs_dict.keys():
		if(objs_dict[obj_idx]["x"] < min_x):
			min_x = objs_dict[obj_idx]["x"]
		
		if(objs_dict[obj_idx]["x"] > max_x):
			max_x = objs_dict[obj_idx]["x"]	
			
		if(objs_dict[obj_idx]["y"] < min_y):
			min_y = objs_dict[obj_idx]["y"]
		
		if(objs_dict[obj_idx]["y"] > max_y):
			max_y = objs_dict[obj_idx]["y"]	
		
	for obj_idx in objs_dict.keys():
		
		var img = Image.load_from_file("res://objects/object{i}.png".format({"i": obj_idx}))
		var texture = ImageTexture.create_from_image(img)
		
		var wav = load("res://objects/object{i}.wav".format({"i": obj_idx}))
		wav.set_loop_end((wav.data.size()-1)/8)
		wav.set_loop_mode(AudioStreamWAV.LOOP_PINGPONG)
		
		
		var new_object = SpatialObject.instantiate()
		var size = objs_dict[obj_idx]["w"] * objs_dict[obj_idx]["h"]
		new_object.get_node("Sprite3D").texture = texture;
		
		new_object.get_node("AudioStreamPlayer3D").stream = wav
		
		new_object.transform.origin = Vector3((objs_dict[obj_idx]["x"]-((max_x - min_x)/2) - min_x)/100, -(objs_dict[obj_idx]["y"]-(max_y/2))/100, -size/20000)
		add_child(new_object)
	
		new_object.get_node("AudioStreamPlayer3D").stream_paused = false
		new_object.get_node("AudioStreamPlayer3D").play()
		

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	$Camera3D.position = Vector3($Camera3D.position.x, $Camera3D.position.y, $Camera3D.position.z+speed*delta);
	pass
