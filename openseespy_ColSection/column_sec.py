import openseespy.opensees as ops
import matplotlib.pyplot as plt
import numpy as np

import pygmsh
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def calculation():
    try:
        column_len = float(entry_column_len.get())
        conc_fcu = float(entry_conc_fcu.get())
        conc_eps0 = float(entry_conc_eps0.get())
        steel_fy = float(entry_steel_fy.get())
        b = float(entry_b.get())
        h = float(entry_h.get())
        as1 = float(entry_as1.get())
        nx = int(entry_nx.get())
        ny = int(entry_ny.get())
        dx = float(entry_dx.get())
        dy = float(entry_dy.get())
        nforce = float(entry_nforce.get())
        disp_max = float(entry_disp_max.get())
        nstep = int(entry_nstep.get())

        # Calculate divy, asx, and asy
        divy = (b - as1 * 2) / (ny + 1)
        asx = 3.14 * dx * dx / 4
        asy = 3.14 * dy * dy / 4

        # --- Placeholder for OpenSees model generation and analysis ---
        # Replace this with your actual OpenSees code using the retrieved parameters.
        # For example:
        # import openseespy.opensees as ops
        # ops.model('basic', '-ndm', 2, '-ndf', 3)
        # ... (define nodes, materials, sections, elements, etc.)
        # ops.analyze(nstep, ...)
        # Define the dimensions of the rectangle
        width = b
        height = h

        # Create a geometry object
        with pygmsh.geo.Geometry() as geom:
            # Define the corner points of the rectangle
            points = [
                geom.add_point((-width/2, -height/2), mesh_size=100),  # Lower-left corner
                geom.add_point((width/2, -height/2), mesh_size=100),  # Lower-right corner
                geom.add_point((width/2, height/2), mesh_size=100),  # Upper-right corner
                geom.add_point((-width/2, height/2), mesh_size=100),  # Upper-left corner
            ]

            # Create lines connecting the points
            lines = [
                geom.add_line(points[0], points[1]),
                geom.add_line(points[1], points[2]),
                geom.add_line(points[2], points[3]),
                geom.add_line(points[3], points[0]),
            ]

            # Create a curve loop from the lines
            curve_loop = geom.add_curve_loop(lines)

            # Create a plane surface from the curve loop
            surface = geom.add_plane_surface(curve_loop)

            # Generate the mesh
            geom.synchronize()
            mesh = geom.generate_mesh()

        # Extract points and cells
        points = mesh.points
        cells = mesh.cells

        # Find triangle cells
        triangle_cells = mesh.cells_dict['triangle']

        # Calculate area and centroid for each triangle
        triangle_areas = []
        triangle_centroids = []

        for triangle in triangle_cells:
            # Get the coordinates of the triangle vertices
            v1 = points[triangle[0]]
            v2 = points[triangle[1]]
            v3 = points[triangle[2]]

            # Calculate the area of the triangle using Heron's formula or the determinant method
            # Determinant method: Area = 0.5 * |(x1(y2-y3) + x2(y3-y1) + x3(y1-y2))|
            area = 0.5 * abs(v1[0] * (v2[1] - v3[1]) +
                            v2[0] * (v3[1] - v1[1]) +
                            v3[0] * (v1[1] - v2[1]))
            triangle_areas.append(area)

            # Calculate the centroid of the triangle
            centroid_x = (v1[0] + v2[0] + v3[0]) / 3
            centroid_y = (v1[1] + v2[1] + v3[1]) / 3
            centroid = (centroid_x, centroid_y)
            triangle_centroids.append(centroid)

        # Output the results to a text file
        with open("triangle_data.txt", "w") as f:
            for i, (area, centroid) in enumerate(zip(triangle_areas, triangle_centroids)):
                x, y = centroid
                f.write(f"{x:.2f},{y:.2f},{area:.2f}\n")

        print("Triangle data (centroid x, centroid y, area) written to triangle_data.txt")

        # System
        ops.wipe()
        print("System")
        ops.model('basic', '-ndm', 3, '-ndf', 6)

        # Restraint
        print("restraint")
        ops.node(1, 0.000E+000, 0.000E+000, 0.000E+000)
        ops.node(2, 0.000E+000, 0.000E+000, column_len)

        # Node
        print("node")
        ops.fix(1, 1, 1, 1, 1, 1, 1)
        ops.fix(2, 0, 1, 0, 1, 0, 1)

        # Equal DOF (Not directly implemented, consider constraints)
        print("Equal DOF")

        # Material
        print("material")
        # uniaxialMaterial Elastic 1 1.999E+005
        # uniaxialMaterial Elastic 2 2.482E+004

        ops.uniaxialMaterial('Concrete01', 1, conc_fcu, conc_eps0, -26.80, -0.01)
        ops.uniaxialMaterial('Steel01', 5, steel_fy, 205000, 0.0001)
        ops.uniaxialMaterial('Elastic', 200, 1000E12)
        # NC800X800
        print("section")
        ops.section('Fiber', 1,  '-GJ', 200)
        filename = 'triangle_data.txt'
        with open(filename, 'r') as f:
            for line in f:
            # Split the line into x, y, and area values
                x, y, area = map(float, line.strip().split(','))
                ops.fiber(x, y, area, 1)  # Material tag is assumed to be 1
        print(f"Fiber section created successfully from {filename}")

        #rebar
        ops.layer('straight', 5, nx, asx, -(h/2-as1),(b/2-as1),(h/2-as1),(b/2-as1) )
        ops.layer('straight', 5, nx, asx, -(h/2-as1),-(b/2-as1),(h/2-as1),-(b/2-as1) )
        ops.layer('straight', 5, ny, asy,  (h/2-as1),-(h/2-as1-divy), (h/2-as1), (h/2-as1-divy) )
        ops.layer('straight', 5, ny, asy, -(h/2-as1),-(h/2-as1-divy),-(h/2-as1), (h/2-as1-divy) )

        print("Fiber section created.")

        # Transformation
        print("transformation")
        ops.geomTransf('Linear', 1, 1.000, 0.000, 0.000)
        ops.geomTransf('Linear', 2, 1.000, 0.000, 0.000)
        # Element
        print("element")
        ops.element('nonlinearBeamColumn', 1, 1, 2, 2, 1, 1)
        # Shell Element
        print("shell element")

        # Solid element
        print("SOLID element")

        # Gravity
        print("gravity")
        # Load Case = DEAD
        ops.timeSeries("Linear",1)
        ops.pattern("Plain", 1, 1)
        ops.load(2, 0.000E+000, 0.000E+000, nforce, 0.000E+000, 0.000E+000, 0.000E+000)
        # Analysis
        print("analysis")
        ops.constraints('Plain')
        ops.numberer('Plain')
        ops.system('BandGeneral')
        ops.test('EnergyIncr', 1.0e-6, 200)
        ops.algorithm('Newton')
        ops.integrator('LoadControl', 1)
        ops.analysis('Static')
        ops.analyze(1)

        ops.loadConst(0.0)
        # Pushover analysis
        print("pushover")

        # Load Case = P1
        ops.timeSeries("Linear",2)
        ops.pattern("Plain", 2, 2)
        ops.load(2, 1.000E+003, 0.000E+000, 0.000E+000, 0.000E+000, 0.000E+000, 0.000E+000)

        ops.recorder('Node', '-file', 'node_disp.out', '-time', '-node', 2, '-dof', 1, 'disp')

        print("analysis")
        ops.constraints('Plain')
        ops.numberer('Plain')
        ops.system('BandGeneral')
        ops.test('EnergyIncr', 1.0e-6, 200)
        ops.algorithm('Newton')
        ops.integrator('DisplacementControl', 2, 1, disp_max/nstep)
        ops.analyze(nstep)




        triang = mtri.Triangulation(points[:, 0], points[:, 1], triangle_cells)

        # Create the plot (optional)
        plt.figure(figsize=(8, 6))  # Adjust figure size as needed
        plt.gca().set_aspect('equal')  # Ensure that the aspect ratio is equal

        # Plot the triangles (optional)
        plt.triplot(triang, linewidth=0.5, color='black')  # Plot the triangle edges

        # Plot the centroids (optional)
        triangle_centroids = np.array(triangle_centroids)
        plt.plot(triangle_centroids[:, 0], triangle_centroids[:, 1], 'ro', markersize=3)  # Plot centroids as red circles

        plt.title('Triangulation of Concrete Column Section with Centroids')
        plt.xlabel('X')
        plt.ylabel('Y')

        # Show the plot (optional)
        plt.show()



        try:
            data = np.loadtxt('node_disp.out', delimiter=' ')  # Adjust delimiter if needed
        except FileNotFoundError:
            print("Error: node_disp.out not found.  Make sure the file exists in the current directory.")
            exit()

        # Extract the time and displacement columns
        time = data[:, 0]  # First column (index 0) is time
        displacement = data[:, 1]  # Second column (index 1) is displacement

        # Create the plot
        plt.figure(figsize=(10, 6))  # Adjust figure size as needed
        plt.plot(displacement, time,  marker='o', linestyle='-', color='b')  # Customize the plot

        # Add labels and title
        plt.xlabel('Time')
        plt.ylabel('Displacement')
        plt.title('Node Displacement vs. Time')

        # Add grid lines for better readability
        plt.grid(True)

        # Show the plot
        plt.show()







    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("OpenSees Parameter Input")

# --- Parameter Labels and Entry Fields with Default Values ---
# Use a loop to create labels and entry fields for each parameter
parameters = {
    "column_len": ("Column Length:", 1000),
    "conc_fcu": ("Concrete fcu:", -26.8),
    "conc_eps0": ("Concrete eps0:", -0.00214),
    "steel_fy": ("Steel fy:", 435.0),
    "b": ("Width (b):", 1200.0),
    "h": ("Height (h):", 800.0),
    "as1": ("Cover (as1):", 50.0),
    "nx": ("Number of X Divisions:", 8),
    "ny": ("Number of Y Divisions:", 6),
    "dx": ("Diameter X Reinforcement:", 40.0),
    "dy": ("Diameter Y Reinforcement:", 40.0),
    "nforce": ("Axial Force:", -15000e3),
    "disp_max": ("Max Displacement:", 8.0),
    "nstep": ("Number of Steps:", 100)
}

entries = {}  # Store entry fields for later access

row_num = 0
for param_name, (label_text, default_value) in parameters.items():
    label = ttk.Label(root, text=label_text)
    label.grid(row=row_num, column=0, padx=5, pady=5, sticky="e")

    entry = ttk.Entry(root)
    entry.insert(0, str(default_value))  # Insert the default value
    entry.grid(row=row_num, column=1, padx=5, pady=5, sticky="w")
    entries[param_name] = entry  # Store the entry field

    row_num += 1

# Access the entry fields using the 'entries' dictionary
entry_column_len = entries["column_len"]
entry_conc_fcu = entries["conc_fcu"]
entry_conc_eps0 = entries["conc_eps0"]
entry_steel_fy = entries["steel_fy"]
entry_b = entries["b"]
entry_h = entries["h"]
entry_as1 = entries["as1"]
entry_nx = entries["nx"]
entry_ny = entries["ny"]
entry_dx = entries["dx"]
entry_dy = entries["dy"]
entry_nforce = entries["nforce"]
entry_disp_max = entries["disp_max"]
entry_nstep = entries["nstep"]

# --- Calculation Button ---
calculate_button = ttk.Button(root, text="Calculation", command=calculation)
calculate_button.grid(row=row_num, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()