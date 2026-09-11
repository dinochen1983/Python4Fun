import ifcopenshell
import numpy
from ifcopenshell.api import run
from ifcopenshell.util.shape_builder import ShapeBuilder
import pandas as pd
from collections import namedtuple
import math


Point = namedtuple('Point', ['name', 'type','np','ax', 'ay','bx', 'by','cx', 'cy','dx', 'dy','bb','hh','ang','az','len'])
data = pd.read_csv('input.txt')
points = []

for index, row in data.iterrows():
    name = row['name']
    type1 = row['type']
    np = row['np']
    ax = row['ax']
    ay = row['ay']
    bx = row['bx']
    by = row['by']  
    cx = row['cx']
    cy = row['cy']        
    dx = row['dx']
    dy = row['dy']       
    bb = row['bb']
    hh = row['hh']   
    ang = row['ang'] 
    az = row['az']       
    len1 = row['len']        
    point = Point(name, type1, np,ax, ay, bx,by,cx,cy,dx,dy, bb,hh,ang,az,len1)
    points.append(point)
    
# Create a blank model
model = ifcopenshell.file()

# All projects must have one IFC Project element
project = run("root.create_entity", model, ifc_class="IfcProject", name="My Project")

# Geometry is optional in IFC, but because we want to use geometry in this example, let's define units
# Assigning without arguments defaults to metric units
run("unit.assign_unit", model)

# Let's create a modeling geometry context, so we can store 3D geometry (note: IFC supports 2D too!)
context = run("context.add_context", model, context_type="Model")

# In particular, in this example we want to store the 3D "body" geometry of objects, i.e. the body shape
body = run("context.add_context", model, context_type="Model",
    context_identifier="Body", target_view="MODEL_VIEW", parent=context)

# Create a site, building, and storey. Many hierarchies are possible.
site = run("root.create_entity", model, ifc_class="IfcSite", name="My Site")
building = run("root.create_entity", model, ifc_class="IfcBuilding", name="Building A")
storey = run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Ground Floor")

# Since the site is our top level location, assign it to the project
# Then place our building on the site, and our storey in the building
run("aggregate.assign_object", model, relating_object=project, products=[site])
run("aggregate.assign_object", model, relating_object=site, products=[building])
run("aggregate.assign_object", model, relating_object=building, products=[storey])

storeys=[]
for x in range(12):
    storey = run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Floor"+str(x))
    run("aggregate.assign_object", model, relating_object=building, products=[storey])
    storeys.append(storey)

def calculate_angle(ax, ay, bx, by):
    # 计算向量的差值
    dx = bx - ax
    dy = by - ay

    # 使用arctan函数计算角度（弧度）
    angle_rad = math.atan2(dy, dx)

    # 将弧度转换为角度
    angle_deg = math.degrees(angle_rad)

    # 角度范围从-180到180，转换为0到360范围
    if angle_deg < 0:
        angle_deg += 360

    return angle_deg


# Let's create a new wall
for one_point in points:
    if (one_point.type =="column"):
        wall = run("root.create_entity", model, ifc_class="IfcColumn")
        # Give our wall a local origin at (0, 0, 0)
        ##run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_x) 
        builder = ifcopenshell.util.shape_builder.ShapeBuilder(model)
        b1 = one_point.bb/2*1000
        h1 = one_point.hh/2*1000
        len1 = one_point.len
        ##outer_curve = builder.polyline([(-b1,-h1), (b1,-h1), (b1,h1), (-b1,h1)],
        ##    arc_points=[], closed=True)
        ##outer_curve = builder.polyline([(-b1,-h1), (-b1,h1), (b1,h1),(b1,-h1), (-b1,-h1) ],
        ##    arc_points=[], closed=True)    

        ##outer_curve = builder.circle((0.,0.), radius=-b1)
        outer_curve = builder.polyline([(-b1,-h1), (b1,-h1), (b1,h1), (-b1,h1)],arc_points=[], closed=True)    
        profile = builder.profile(outer_curve, inner_curves=[], name="Arbitrary")

        # Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
        #representation = run("geometry.add_wall_representation", model, context=body, length=5, height=0.2, thickness=1.5)
        
        representation = run("geometry.add_profile_representation", model, context=body, profile=profile, depth=len1)
        # Assign our new body geometry back to our wall
        run("geometry.assign_representation", model, product=wall, representation=representation)
        matrix = numpy.eye(4)
        matrix = ifcopenshell.util.placement.rotation(one_point.ang, "Z") @ matrix
        # Set the X, Y, Z coordinates. Notice how we rotate first then translate.
        # This is because the rotation origin is always at 0, 0, 0.
        matrix[:,3][0:3] = (one_point.ax, one_point.ay, one_point.az-len1)
        run("geometry.edit_object_placement", model, product=wall, matrix=matrix, is_si=True)
        # Place our wall in the ground floor
        run("spatial.assign_container", model, relating_structure=storeys[2], products=[wall])
        pset = ifcopenshell.api.run("pset.add_pset", model, product=wall, name="Other")
        run("pset.edit_pset", model, pset=pset, properties={"Ax": "0.001", "Ay": "0.001"})
        pset = ifcopenshell.api.run("pset.add_pset", model, product=wall, name="Other")
        run("pset.edit_pset", model, pset=pset, properties={"Section": "Rect"})


    elif (one_point.type =="beam"):
        wall = run("root.create_entity", model, ifc_class="IfcBeam")
        # Give our wall a local origin at (0, 0, 0)
        ##run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_x) 
        ang =  calculate_angle(one_point.ax,one_point.ay,one_point.bx,one_point.by)
        b1 =  one_point.bb/2
        az = one_point.az
        ax1 = one_point.ax + b1*math.sin(math.pi/180*ang)
        ay1 = one_point.ay - b1*math.cos(math.pi/180*ang)
        len = math.sqrt((one_point.by-one_point.ay)*(one_point.by-one_point.ay)+(one_point.bx-one_point.ax)*(one_point.bx-one_point.ax))
        # Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
        representation = run("geometry.add_wall_representation", model, context=body, length=len, height=-one_point.hh, thickness=one_point.bb)
        # Assign our new body geometry back to our wall
        run("geometry.assign_representation", model, product=wall, representation=representation)
        matrix = numpy.eye(4)
        matrix = ifcopenshell.util.placement.rotation(ang, "Z") @ matrix
        # Set the X, Y, Z coordinates. Notice how we rotate first then translate.
        # This is because the rotation origin is always at 0, 0, 0.
        matrix[:,3][0:3] = (ax1, ay1, az)
        run("geometry.edit_object_placement", model, product=wall, matrix=matrix, is_si=True)
        # Place our wall in the ground floor
        run("spatial.assign_container", model, relating_structure=storeys[2], products=[wall])
        pset = ifcopenshell.api.run("pset.add_pset", model, product=wall, name="Other")
        run("pset.edit_pset", model, pset=pset, properties={"Ax": "0.001", "Ay": "0.001"})

    elif (one_point.type =="wall"):
        wall = run("root.create_entity", model, ifc_class="IfcWall")
        # Give our wall a local origin at (0, 0, 0)
        ##run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_x) 
        
        ang =  calculate_angle(one_point.ax,one_point.ay,one_point.bx,one_point.by)
        b1 =  one_point.bb/2
        ax1 = one_point.ax + b1*math.sin(math.pi/180*ang)
        ay1 = one_point.ay - b1*math.cos(math.pi/180*ang)
        len1 = one_point.len
        az = one_point.az
        len = math.sqrt((one_point.by-one_point.ay)*(one_point.by-one_point.ay)+(one_point.bx-one_point.ax)*(one_point.bx-one_point.ax))
        # Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
        representation = run("geometry.add_wall_representation", model, context=body, length=len, height=len1, thickness=one_point.bb)
        # Assign our new body geometry back to our wall
        run("geometry.assign_representation", model, product=wall, representation=representation)
        matrix = numpy.eye(4)

        matrix = ifcopenshell.util.placement.rotation(ang, "Z") @ matrix
        # Set the X, Y, Z coordinates. Notice how we rotate first then translate.
        # This is because the rotation origin is always at 0, 0, 0.
        matrix[:,3][0:3] = (ax1, ay1, az-len1)
        run("geometry.edit_object_placement", model, product=wall, matrix=matrix, is_si=True)
        # Place our wall in the ground floor
        run("spatial.assign_container", model, relating_structure=storeys[2], products=[wall])
        pset = ifcopenshell.api.run("pset.add_pset", model, product=wall, name="Other")
        run("pset.edit_pset", model, pset=pset, properties={"Ax": "0.001", "Ay": "0.001"})     


    elif (one_point.type =="slab"):
        wall = run("root.create_entity", model, ifc_class="IfcSlab")
        # Give our wall a local origin at (0, 0, 0)
        ##run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_x) 
        ax = one_point.ax*1000
        ay = one_point.ay*1000
        bx = one_point.bx*1000
        by = one_point.by*1000
        cx = one_point.cx*1000
        cy = one_point.cy*1000
        dx = one_point.dx*1000
        dy = one_point.dy*1000
        az = one_point.az   
        builder = ifcopenshell.util.shape_builder.ShapeBuilder(model)
        if (one_point.np==3):
            outer_curve = builder.polyline([(ax,ay), (bx,by), (cx,cy)],
                arc_points=[], closed=True)    
            profile = builder.profile(outer_curve, inner_curves=[], name="Arbitrary")
        elif (one_point.np==4):
            outer_curve = builder.polyline([(ax,ay), (bx,by), (cx,cy), (dx,dy)],
                arc_points=[], closed=True)    
            profile = builder.profile(outer_curve, inner_curves=[], name="Arbitrary")
        # Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
        #representation = run("geometry.add_wall_representation", model, context=body, length=5, height=0.2, thickness=1.5)
        representation = run("geometry.add_profile_representation", model, context=body, profile=profile, depth=-one_point.bb)
        # Assign our new body geometry back to our wall
        run("geometry.assign_representation", model, product=wall, representation=representation)
        matrix = numpy.eye(4)
        matrix[:,3][0:3] = (0, 0, az)
        # Set the X, Y, Z coordinates. Notice how we rotate first then translate.
        # This is because the rotation origin is always at 0, 0, 0.
        run("geometry.edit_object_placement", model, product=wall, matrix=matrix, is_si=True)
        # Place our wall in the ground floor
        run("spatial.assign_container", model, relating_structure=storeys[2], products=[wall])
        pset = ifcopenshell.api.run("pset.add_pset", model, product=wall, name="Other")
        run("pset.edit_pset", model, pset=pset, properties={"Ax": "0.001", "Ay": "0.001"})

# Write out to a file

model.write("output.ifc")
print('export ifc done')