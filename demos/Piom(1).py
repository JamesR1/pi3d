# Ponh using pi3d module
# =====================================
# Copyright (c) 2012 - Tim Skillman, Paddy Gaunt
# Version 0.02 - 20Aug12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
# $ sudo apt-get install python-imaging
#
# before running this example
#

import pi3d,math,random,glob,time

from pi3d.Display import Display
from pi3d.Texture import Textures
from pi3d.EnvironmentCube import EnvironmentCube
from pi3d.Light import Light
from pi3d.Matrix import Matrix
from pi3d.Mouse import Mouse
from pi3d.Key import Key

from pi3d.shape.Sphere import Sphere
from pi3d.shape.ElevationMap import ElevationMap

rads = 0.017453292512 # degrees to radians

#helpful messages
print "############################################################"
print "Mouse to move left and right and up and down"
print "############################################################"
print

# Setup display and initialise pi3d
display = Display()
display.create3D(10,10,1200,900, 0.5, 800.0, 60.0) # x,y,width,height,near,far,aspect
#display.create3D(10,10,1200,900, 0.5, 800.0, 60.0) # x,y,width,height,near,far,aspect
display.setBackColour(0.4,0.8,0.8,1) # r,g,b,alpha


# Load textures
texs=Textures()
# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'rockimg2.blend = False')
groundimg = texs.loadTexture("textures/piom2.jpg")
monstimg = texs.loadTexture("textures/piom3.jpg")
# environment cube
ectex = texs.loadTexture("textures/ecubes/skybox_stormydays.jpg")
myecube = EnvironmentCube(900.0,"CROSS")

#monster
radius = 1
ball = Sphere(radius,12,12,0.0,"sphere",-4,2,-7)

# Create elevation map
mapwidth=50.0                              
mapdepth=50.0
maphalf=23.0
mapheight=8
#set smooth to give proper normals
mymap = ElevationMap("textures/Piom1b.jpg",mapwidth,mapdepth,mapheight,64,64,128,"sub",0,0,0, smooth=True) ################### increased tiles to 32
# lighting. The default light is a point light but I have made the position method capable of creating
# a directional light and this is what I do inside the loop. If you want a torch you don't need to move it about
light = Light(0, 2, 2, 1, "", 1,2,3, 0.1,0.1,0.2) #yellowish 'torch' or 'sun' with low level blueish ambient
light.position(1,2,3,0) # set to directional light by settin position with 0 fourth parameter
light.on()

########## need to create instances of these before using them in the loop! #################
camera = Matrix() ####################

mykeys = Key() ####################
mymouse = Mouse() ####################
mymouse.start() ####################

omx=mymouse.x ####################
omy=mymouse.y ####################
xm, zm = 0, 0 ####################
avhgt = 2.0 ####################
ym = -(mymap.calcHeight(xm,zm)+avhgt) ####################
rot, tilt = 0.0, 0.0 ####################

sx, sy, sz = 5, 5, -5 ####################
dsx, dsy, dsz = 0.1, 0.0, -0.1 ####################
gravity = 0.02 ####################
#############################################################################################

while 1:
  display.clear()
  
  camera.identity()
  camera.rotate(tilt, 0, 0) ####################
  camera.rotate(0, rot, 0) ####################
  #camera.translate(xm,-2+ym-mapheight,-maphalf+2)
  # I think you want to walk around inside your map so need xm, ym and zm (like ForestWalk etc)
  camera.translate(xm, ym, zm) ###################
  
  myecube.draw(ectex,xm,ym,zm)
  mymap.draw(groundimg)
  
  ball.draw(monstimg)
  
  ###################### you haven't got a monster, you are using ball instead
  """
  #monster movement
  drx = sx - rx
  if abs(drx) > max_speed: drx = drx/abs(drx) * max_speed
  dry = sy - ry
  if abs(dry) > max_speed: dry = dry/abs(dry) * max_speed
  rx += drx
  ry += dry
  
  monster.position(rx, ry, -maphalf)
  """
  
  dsy -= gravity
  sx += dsx
  sy += dsy
  sz += dsz
  # now uses the clashTest method from elevationMap
  clash = mymap.clashTest(sx, sy, sz, radius)
  # bouncing physics
  if clash[0]:
    # returns the components of normal vector if clash
    nx, ny, nz =  clash[1], clash[2], clash[3]
    # move it away a bit to stop it getting trapped inside if it has tunelled
    sx, sy, sz = sx - 0.1*radius*nx, sy - 0.1*radius*ny, sz - 0.1*radius*nz
    # clash[4] is also the ground level below the mid point of the object so this could be used to 'lift' it up

    # use R = I - 2(N.I)N
    rfact = 2.10*(nx*dsx + ny*dsy + nz*dsz) #small extra boost by using value > 2 to top up energy in defiance of 1st LOT
    dsx, dsy, dsz = dsx - rfact*nx, dsy - rfact*ny, dsz - rfact*nz
    # stop the speed increasing too much
    if dsx > 0.8: dsx = 0.7
    if dsz > 0.4: dsz = 0.3    
   
     

  ball.position(sx, sy, sz) #########################################################

  mx=mymouse.x
  my=mymouse.y

  #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
  rot += (mx-omx)*0.2
  tilt -= (my-omy)*0.2
  omx=mx
  omy=my
        
  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119:    #key W
      xm-=math.sin(rot*rads)
      zm+=math.cos(rot*rads)
      ym = -(mymap.calcHeight(xm,zm)+avhgt)
      ################################################################
      # as it stands you can walk anywhere but as the walls are so thin you often see through them
      # you could do a clashTest for yourself (camera) or check the dy if you moved to xm+dx, zm+dz as I do in Amazing.py
      #dx = -math.sin(rot*rads)
      #dz = math.cos(rot*rads)
      #dy = -(mymap.calcHeight(xm + dx*1.5, zm + dz*1.5) + avhgt) - ym
      #if dy > -1.0: # remember camera locations all work in reverse!!
      #  xm, ym, zm = xm + dx, ym + dy, zm + dz

    elif k==115:  #kry S
      xm+=math.sin(rot*rads)
      zm-=math.cos(rot*rads)
      ym = -(mymap.calcHeight(xm,zm)+avhgt)
    elif k==39:   #key '
      tilt -= 2.0
      print tilt
    elif k==47:   #key /
      tilt += 2.0
    elif k==97:   #key A
      rot -= 2
    elif k==100:  #key D
      rot += 2
    elif k==112:  #key P
      display.screenshot("Piom.jpg")
    elif k==27:    #Escape key
      mykeys.close()
      texs.deleteAll()
      display.destroy()
      break
    else:
      print k

  display.swapBuffers()
