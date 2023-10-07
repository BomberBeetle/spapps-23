extends Node3D


# Called when the node enters the scene tree for the first time.
func _ready():
	
	var SpatialObject = load("res://SpatialObject.tscn")
	
	var json_text = FileAccess.get_file_as_string("res://objects.json");
	var objs_dict = JSON.parse_string(json_text);
	for obj_idx in objs_dict.keys():
		var img = Image.load_from_file("res://objects/object{i}.png".format({"i": obj_idx}))
		var texture = ImageTexture.create_from_image(img)
		var new_object = SpatialObject.instantiate()
		var size = objs_dict[obj_idx]["w"] * objs_dict[obj_idx]["h"]
		new_object.get_node("Sprite3D").texture = texture;
		
		new_object.transform.origin = Vector3((objs_dict[obj_idx]["x"]-100)/100, (objs_dict[obj_idx]["y"]-100)/100, size/4000)
		add_child(new_object)
		

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
