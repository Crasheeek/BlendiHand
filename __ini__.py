# Version 1.0.6
#
# Previous versions: NULL
#
# Last update: 30.1.2024 11:01 PM
#
# made by Crash & X_X_X_BRINGER_OF_WAR_X_X_X
#

print("Version 1.0.4 \n\nPrevious versions: NULL \n\nLast update: 30.1.2024 11:01 PM")
import bpy
import serial
import math
import time

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
armature_name = "Armature"
bpy.data.objects[armature_name].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[armature_name]

# Setting up interaction mode
bpy.ops.object.mode_set(mode='POSE')




class ModalTimerOperator(bpy.types.Operator):
    "Operator which runs its self from timer"
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    # Class Variable
    i = 0
    
    # Serial variables
    ser = None
    PORT = 'COM7'
    BANDRATE = '115200'
    
    # Blender Variables
    _timer = None
    
    # Finger Sys Variables
      
    maxLimit        = [1023,   1023,   1023,   1023,   1023]
    minLimit        = [   0,      0,    223,      0,      0]
    
    # Prsty         = [Thmb,   Indx,    Mid,   Ring,   Pink]
    goal_degrees    = [ 100,    170,    140,    120,    90]
    
    
    # Axis          = ['X',    'Z',    'X',    'X',    'X' ]        X= 0, Y = 1, Z = 2
    axis            = [0,       2,      0,      0,      0  ]

    #Declaring bones representing fingers
    R_Hand = bpy.data.objects["Armature"]
    fingerBones = [
        R_Hand.pose.bones["Pinky_Bone"],
        R_Hand.pose.bones["Thumb_Bone"],
        R_Hand.pose.bones["Index_Bone"],
        R_Hand.pose.bones["Middle_Bone"],
        R_Hand.pose.bones["Ring_Bone"]
        ]
    
    fixed = []
    fixed_axis = []
        
        
    
    # Setting up rotation_mode for every bone and reseting fingers
    #for fing in range(5):
    #    fingerBones[fing].rotation_mode = 'XYZ'
    #    print("YUP")

#\------------------------------------------INIT-----------------------------------------------------/ 
    
    # Inicialization of code/ Basic setup
    def __init__(self):
        print("init start")
        self.ser = serial.Serial('COM7', '115200')
        time.sleep(2)
        print("init done")

#\------------------------------------------MODAL-----------------------------------------------------/ 

    # Start of Modal Timer
    def modal(self, context, event):
        # If statment for canceling serial comunication and code
        if event.type in {'ESC'}:
            self.cancel(context)
            self.ser.close()
            self.ser.flush()
            return {'CANCELLED'}
        
        # Using Timer even.type
        if event.type == 'TIMER':
            try:
                if self.R_Hand:
                    self.ser.write(b'1')
                    data = self.ser.readline().decode('utf-8').strip().split(",")
                    print(data)
                    #self.fixed = [int(ele) for ele in data]
                    #self.fixed = list(map(int, data))
                    #self.fixed = int(data[self.i])
                    self.fixed = list(map(int, data))
                    
                    
                    self.fixed[2] = self.fixed[2] + 223
                    self.fixed[3] = self.fixed[3] + 123
                    degrees = ((self.maxLimit[self.i]  - self.fixed[self.i]) * self.goal_degrees[self.i] / self.maxLimit[self.i])
                         
                    # Testing math formula
                    # degrees = ((self.max - data) * self.goal_degrees / self.max)
                    


                    

                    # Preventing for bugs
                    if (degrees < 0):
                        degrees = 0
                    
                    if self.i >= 4:
                        self.i = -1
                    self.i +=1
                    
                    rads =  math.radians(degrees)
                    
                    self.fingerBones[self.i].rotation_euler[self.axis[self.i]] = -rads
                    
                    '''if (self.i == 1):
                        self.fingerBones[self.i].rotation_euler[self.axis[self.i]] = rads
                    else:
                        self.fingerBones[self.i].rotation_euler[self.axis[self.i]] = -rads'''
                    

#\----------------------------------------------GARBAGE-----------------------------------------------------------------------------------/
                    #self.R_Hand.pose.bones["Point_Bone"].rotation_euler[2] = math.radians(current)
                    #bpy.data.objects['Armature'].pose.bones["Bone"].rotation_euler.rotate_axis('Z', math.radians(current - self.last))
                    #self.last = current
#\----------------------------------------------Finish-----------------------------------------------------------------------------------/
            except Exception as e:
                raise RuntimeError(f"Error occurred during comunication: {e}")
                self.ser.close()
                
        return{'PASS_THROUGH'}
    
    # Execution of code
    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.002, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    # Stopping code
    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        
        #for loop in range(5):
        #    fingerBones[loop].rotation_euler[2] = 0
        #    
        #R_Hand.pose.bones["Thumb_Bone"].rotation_euler[0] = 0
        
def register():
    bpy.utils.register_class(ModalTimerOperator)
    
def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)
    
if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
