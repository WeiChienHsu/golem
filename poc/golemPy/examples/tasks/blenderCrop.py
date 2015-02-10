import bpy

for scene in bpy.data.scenes:

    scene.render.resolution_x = 800
    scene.render.resolution_y = 600
    scene.render.use_border = True
    scene.render.use_crop_to_border = True
    scene.render.border_max_x = 1.0
    scene.render.border_min_x = 0.0
    scene.render.border_min_y = 0.0
    scene.render.border_max_y = 1.0
#then render:
bpy.ops.render.render()