bl_info = {
    "name": "Copy Vertex Color Channel",
    "blender": (3, 60, 3),
    "category": "Object",
}

import bpy

copy_from_attr = "Gradient"
copy_to_attr = "Gradient"
from_channel = 0
to_channel = 3
class ObjectCopyVertexColorChannel(bpy.types.Operator):
    """Copy Vertex Color Channel"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.copy_vertex_color_channel"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Copy Vertex Color Channel"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        active_mesh = context.active_object.data
        for v_index in range(len(active_mesh.vertices)):
            active_mesh.color_attributes[copy_to_attr].data[v_index].color[to_channel] =\
            active_mesh.color_attributes[copy_from_attr].data[v_index].color[from_channel]

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(ObjectCopyVertexColorChannel.bl_idname)

def register():
    bpy.utils.register_class(ObjectCopyVertexColorChannel)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(ObjectCopyVertexColorChannel)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()