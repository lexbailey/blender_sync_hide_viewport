bl_info = {
    "name": "Sync hide-render and hide-viewport",
    "blender": (3, 3, 1),
    "author": "Lex Bailey",
    "category": "Animation",
    "description":"Provides convenient operations for synchronising an objects 'Disable in Viewports' curve with its 'Disable in Renders' curve for convenient fast previews",
}

"""
This add-on provides two new operations.
One of them copies the "Disable in Renders" animation curve for all selected objects to the "Disable in Viewports" animation curve, allowing you to instantly get a preview of the final render visibility of objects in normal viewports.
The other deletes the whole of the hide-viewports curve, ensuring that you can always see an object in the viewports.
To use this add-on, simply select some objects that have the "Disable in Renders" property animated, and then opent the context menu (right click by default) and click "Copy Disable-in-Renders to Disable-in-Viewports" or "Always show in viewports".

The source code for this plugin is distributed under the terms of the MIT Open Source Software Licence.

Copyright Lex Bailey 2022

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import bpy

class ViewportsHideOp(bpy.types.Operator):
    bl_idname = "wm.auto_hide_in_viewport"
    bl_label = "Copy Disable-in-Renders to Disable-in-Viewports"
        
    def execute(self, context):
        for o in context.selected_objects:
            o.hide_viewport = False
            if o.animation_data is None:
                continue
            if o.animation_data.action is None:
                continue
            curves = o.animation_data.action.fcurves
            if curves is None:
                continue
            hide_render = curves.find('hide_render')
            hide_viewport = curves.find('hide_viewport')
            if hide_render is None:
                if hide_viewport is not None:
                    curves.remove(hide_viewport)
            else:
                if hide_viewport is None:
                    hide_viewport = curves.new('hide_viewport')
                hide_viewport.keyframe_points.clear()
                for p in hide_render.keyframe_points:
                    # Copy all information for each keyframe from hide_render to hide_viewport
                    frame, value = p.co
                    f = hide_viewport.keyframe_points.insert(frame, value)
                    f.easing = p.easing
                    f.back = p.back
                    f.interpolation = p.interpolation
            o.hide_viewport = o.hide_render
        return {'FINISHED'}
    
def show_objects(objs):
    for o in objs:
        o.hide_viewport = False
        if o.animation_data is None:
            continue
        if o.animation_data.action is None:
            continue
        curves = o.animation_data.action.fcurves
        if curves is None:
            continue
        hide_viewport = curves.find('hide_viewport')
        if hide_viewport is not None:
            curves.remove(hide_viewport)

class ViewportsShowAlways(bpy.types.Operator):
    bl_idname = "wm.always_show_in_viewport"
    bl_label = "Always show in viewports"
        
    def execute(self, context):
        show_objects(context.selected_objects)
        return {'FINISHED'}

class ViewportsShowAllAlways(bpy.types.Operator):
    bl_idname = "wm.always_show_all_in_viewport"
    bl_label = "Always show ALL objects in viewports"
        
    def execute(self, context):
        show_objects(context.scene.objects)
        return {'FINISHED'}
            
def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(ViewportsHideOp.bl_idname, text=ViewportsHideOp.bl_label)
    self.layout.operator(ViewportsShowAlways.bl_idname, text=ViewportsShowAlways.bl_label)
    self.layout.operator(ViewportsShowAllAlways.bl_idname, text=ViewportsShowAllAlways.bl_label)
    
def register():
    bpy.utils.register_class(ViewportsHideOp)
    bpy.utils.register_class(ViewportsShowAlways)
    bpy.utils.register_class(ViewportsShowAllAlways)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
    bpy.types.OUTLINER_MT_object.append(menu_func)
    
def unregister():
    bpy.types.OUTLINER_MT_object.remove(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(ViewportsShowAllAlways)
    bpy.utils.unregister_class(ViewportsShowAlways)
    bpy.utils.unregister_class(ViewportsHideOp)
    
if __name__ == "__main__":
    register()

