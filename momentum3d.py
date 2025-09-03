from ursina import *
from ursina.shaders import basic_lighting_shader
import math
m1 = float(input("mass of object 1 (kg) (0-20): "))
v1x = float(input("object 1 x component of velocity (m/s) (0-20): "))
v1y = float(input("object 1 y component of velocity (m/s) (0-20) "))
v1z = float(input("object 1 z component of velocity(m/s) (0-20)"))

m2 = float(input("mass of object 2 (kg) (0-20): "))
v2x = float(input("object 2 x component of velocity (m/s) (0-20): "))
v2y = float(input("object 2 y component of velocity (m/s) (0-20) "))
v2z = float(input("object 2 z component of velocity (m/s) (0-20)"))

v1 = Vec3(v1x/100, v1y/100, v1z/100)
v2 = Vec3(v2x/100, v2y/100, v2z/100)

def elastic_collision(m1, v1, m2, v2):
    new_v2_x = (2*m1*v1.x - m1*v2.x + m2*v2.x) / (m1+m2)
    new_v1_x = v2.x + new_v2_x - v1.x
    new_v2_y = (2*m1*v1.y - m1*v2.y + m2*v2.y) / (m1+m2)
    new_v1_y = v2.y + new_v2_y - v1.y
    new_v2_z = (2*m1*v1.z - m1*v2.z + m2*v2.z) / (m1+m2)
    new_v1_z = v2.z + new_v2_z - v1.z
    new_v1 = Vec3(new_v1_x, new_v1_y, new_v1_z)
    new_v2 = Vec3(new_v2_x, new_v2_y, new_v2_z)
    return new_v1, new_v2

app = Ursina()
window.borderless = False
window.size = (1920,1080)

sphere1 = Entity(model='sphere', color=color.red, scale=2,position=(-5,0,0), shader=basic_lighting_shader)
sphere2 = Entity(model='sphere', color=color.black, scale=2,position=(5,0,0), shader=basic_lighting_shader)

camera.position = (0,1.5,-20)
camera.rotation = (0,0,0)
vel1, vel2 = v1, v2

LEFT, RIGHT = -30, 30
UP, DOWN = 30, -30
FRONT, BACK = 30, -30

arena_size = RIGHT - LEFT


front = Entity(model='quad', scale=(arena_size, arena_size),position=(0, 0, 30), color=color.rgba(0,255,0,100), double_sided=True)
back = Entity(model='quad', scale=(arena_size, arena_size),position=(0, 0, -30), rotation_y=180, color=color.rgba(255,0,0,100), double_sided=True)
left = Entity(model='quad', scale=(arena_size, arena_size),position=(-30, 0, 0), rotation_y=90, color=color.rgba(0,0,255,100), double_sided=True)
right = Entity(model='quad', scale=(arena_size, arena_size), position=(30, 0, 0), rotation_y=-90, color=color.rgba(255,255,0,100), double_sided=True)
up = Entity(model='quad', scale=(arena_size, arena_size),position=(0, 30, 0), rotation_x=-90, color=color.rgba(0,255,255,100), double_sided=True)
down = Entity(model='quad', scale=(arena_size, arena_size),position=(0, -30, 0), rotation_x=90, color=color.rgba(255,0,255,100), double_sided=True)

t1 = Text(f"v1={vel1.x:.2f} px/frame", position=(-0.4,0.45), origin=(0,0), scale=2, background=True)
t2 = Text(f"v2={vel2.x:.2f} px/frame", position=(0.3,0.45), origin=(0,0), scale=2, background=True)

mouse.locked = True
mouse.visible = False
camera.fov = 100
def clamp_camera():
    camera.x=max(LEFT+1,min(RIGHT-1,camera.x))
    camera.y=max(DOWN+1,min(UP-1,camera.y))
    camera.z=max(BACK+1,min(FRONT-1,camera.z))
def update():
    global vel1, vel2
    sphere1.position += vel1
    sphere2.position += vel2

    
    ball_dist=math.dist(sphere1.position,sphere2.position)
    if ball_dist <= sphere1.scale_x:   
        vel1, vel2 = elastic_collision(m1, vel1, m2, vel2)

  
    r1 = sphere1.scale_x/2
    if sphere1.x <= LEFT+r1 or sphere1.x >= RIGHT-r1: vel1.x *= -1
    if sphere1.y <= DOWN+r1 or sphere1.y >= UP-r1:    vel1.y *= -1
    if sphere1.z <= BACK+r1 or sphere1.z >= FRONT-r1: vel1.z *= -1

  
    r2 = sphere2.scale_x/2
    if sphere2.x <= LEFT+r2 or sphere2.x >= RIGHT-r2: vel2.x *= -1
    if sphere2.y <= DOWN+r2 or sphere2.y >= UP-r2:    vel2.y *= -1
    if sphere2.z <= BACK+r2 or sphere2.z >= FRONT-r2: vel2.z *= -1

    
    speed = 0.2
    if held_keys['w']: camera.position += camera.forward * speed
    if held_keys['s']: camera.position -= camera.forward * speed
    if held_keys['a']: camera.position -= camera.right * speed
    if held_keys['d']: camera.position += camera.right * speed
    if held_keys['space']: camera.position += camera.up * speed
    if held_keys['shift']: camera.position -= camera.up * speed

   
    t1.text = f"v1=({vel1.x:.2f},{vel1.y:.2f},{vel1.z:.2f}) m/s"
    t2.text = f"v2=({vel2.x:.2f},{vel2.y:.2f},{vel2.z:.2f}) m/s"
    sensitivity = 40
    camera.rotation_y += mouse.velocity[0] * sensitivity
    camera.rotation_x -= mouse.velocity[1] * sensitivity
    camera.rotation_x = clamp(camera.rotation_x, -80, 80)
    clamp_camera()
app.run()
