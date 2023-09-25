bl_info = {
    "name": "Copy Vertex Color Channel",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import functools

def getGreyscaleAverage(color_data):
    return list(map(lambda v :
         (v.color[0] + v.color[1] + v.color[2]) * v.color[3] / 3, color_data))
         
def getGreyscaleNoAlpha(color_data):
    return list(map(lambda v :
         (v.color[0] + v.color[1] + v.color[2]) / 3, color_data))

def getChannelData(color_data, channel_index):
    return list(map(lambda v: v.color[channel_index], color_data))
        
class CopyVertexColorChannel(bpy.types.Operator):
    """Copy Vertex Color Channel"""
    bl_idname = "object.copy_vertex_color_channel"        
    bl_label = "Copy Vertex Color Channel"         
    bl_options = {'REGISTER', 'UNDO'}  
        
    from_channel: bpy.props.EnumProperty(
            #(identifier, name, description, icon, number)
    items = [('0','Red','Red','',0), 
             ('1','Green','Green','',1),
             ('2','Blue','Blue','',2),
             ('3','Alpha','Alpha','',3),
             ('greyscale','Greyscale average','Greyscale average',4),
             ('greyscale_no_alpha','Greyscale average (no alpha)',
                'Greyscale average (no alpha)',5)],
    name = "Copy From Channel",
    default = '0')

    def execute(self, context):        # execute() is called when running the operator.
        active_mesh = context.active_object.data
        active_color =  active_mesh.color_attributes.active_color
        
        bpy.types.WindowManager.vertex_color_clipboard = []
        bpy.types.WindowManager.vertex_color_copied_domain = active_color.domain
        
        if self.from_channel == 'greyscale_no_alpha':
             bpy.types.WindowManager.vertex_color_clipboard = getGreyscaleNoAlpha(
                active_color.data)
        elif self.from_channel == 'greyscale':
            bpy.types.WindowManager.vertex_color_clipboard = getGreyscaleAverage(
                active_color.data)
        else:
            bpy.types.WindowManager.vertex_color_clipboard = getChannelData(
                active_color.data, int(self.from_channel))
                
        return {'FINISHED'}            
    
    def invoke(self, context, event) :
        return context.window_manager.invoke_props_dialog(self)
    
class PasteVertexColorChannel(bpy.types.Operator):
    """Paste Vertex Color Channel""" 
    bl_idname = "object.paste_vertex_color_channel"       
    bl_label = "Paste Vertex Color Channel"        
    bl_options = {'REGISTER', 'UNDO'} 
        
    to_channel: bpy.props.EnumProperty(
            #(identifier, name, description, icon, number)
    items = [('0','Red','Red','',0), 
             ('1','Green','Green','',1),
             ('2','Blue','Blue','',2),
             ('3','Alpha','Alpha','',3),
             ('all', 'All', 'All', 4),
             ('all_no_alpha', 'All (No alpha)','All (No alpha)', 5)],
    name = "Paste To Channel",
    default = '0')

    def execute(self, context):        # execute() is called when running the operator.
        active_mesh = context.active_object.data
        active_color =  active_mesh.color_attributes.active_color
        
        if active_color.domain != bpy.types.WindowManager.vertex_color_copied_domain :
            self.report({'ERROR_INVALID_INPUT'},
             "source and destination must have the same domain ")
            return {'CANCELLED'}
        if len(active_color.data) != len(bpy.types.WindowManager.vertex_color_clipboard) :
            self.report({'ERROR_INVALID_INPUT'},
             "source and destination must have the same number of vertices")
            return {'CANCELLED'}
        
        if self.to_channel == 'all' :
            for v_index in range(len(active_color.data)):
                active_color.data[v_index].color =\
                [bpy.types.WindowManager.vertex_color_clipboard[v_index]] * 4
        elif self.to_channel == 'all_no_alpha' :
            for v_index in range(len(active_color.data)):
                active_color.data[v_index].color =\
                [bpy.types.WindowManager.vertex_color_clipboard[v_index]] * 3 +\
                 active_color.data[v_index].color[3]
        else:
            for v_index in range(len(active_color.data)):
                active_color.data[v_index].color[int(self.to_channel)] =\
                    bpy.types.WindowManager.vertex_color_clipboard[v_index]

        return {'FINISHED'} 
    
    def invoke(self, context, event) :
        return context.window_manager.invoke_props_dialog(self)   

def menu_func1(self, context):
    self.layout.operator(CopyVertexColorChannel.bl_idname)
    
def menu_func2(self, context):
    self.layout.operator(PasteVertexColorChannel.bl_idname)

def register():
    bpy.utils.register_class(CopyVertexColorChannel)
    bpy.utils.register_class(PasteVertexColorChannel)
    bpy.types.MESH_MT_color_attribute_context_menu.append(menu_func1)
    bpy.types.MESH_MT_color_attribute_context_menu.append(menu_func2)


def unregister():
    bpy.utils.unregister_class(CopyVertexColorChannel)
    bpy.utils.unregister_class(PasteVertexColorChannel)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()