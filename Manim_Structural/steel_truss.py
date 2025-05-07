from manim import *
import pandas as pd

class AnimateNodesRelativeDisplacement(Scene):
    def construct(self):
        df = pd.read_csv("node_displacements_relative.csv")
        # Define initial node positions (arbitrary, but consistent)
        initial_positions = {
                1:[0,0.6,0],
                2:[1.2,0.6,0],
                3:[1.2,0,0],
                4:[0,0,0],
                5:[2.4,0.6,0],
                6:[2.4,0,0],
                7:[3.6,0.6,0],
                8:[3.6,0,0],
                9:[0.6,0.6,0],
                10:[0.6,0,0],
                11:[1.8,0.6,0],
                12:[1.8,0,0],
                13:[3,0.6,0],
                14:[3,0,0]
        }

        # Define the amount to reduce the x-coordinate by
        x_reduction = 2.0

        # Define the scaling factor for x and y coordinates
        scale_factor = 2.8

        # Create a new dictionary to store the modified positions
        modified_positions = {}

        # Iterate through the initial positions and apply the transformations
        for node, position in initial_positions.items():
            # Reduce the x-coordinate
            reduced_x = position[0] - x_reduction

            # Scale the x and y coordinates
            scaled_x = reduced_x * scale_factor
            scaled_y = position[1] * scale_factor

            # Store the modified position in the new dictionary
            modified_positions[node] = [scaled_x, scaled_y, position[2]]  # Keep z the same

        initial_positions = modified_positions


        # Get the number of nodes
        num_nodes = df['node'].nunique()
        print(f"Number of nodes: {num_nodes}")

        # Get the number of frames
        num_frames = df['frame'].nunique()
        num_frames = 2
        print(f"Number of frames: {num_frames}")



        # Define line start and end points using node indices
        lines_data = [
        (1,2),
        (3,0),
        (4,5),
        (6,7),
        (0,8),
        (8,1),
        (2,9),
        (9,3),
        (1,10),
        (10,4),
        (5,11),
        (11,2),
        (4,12),
        (12,6),
        (7,13),
        (13,5),
        (8,9),
        (10,11),
        (12,13),
        (3,8),
        (9,1),
        (2,10),
        (11,4),
        (5,12),
        (13,6)
        ]

        # Create the title text
        title = Text("Steel Truss Deformation", font_size=48)
        # Position the title at the top of the screen
        title.to_edge(UP)
        # Add the title to the scene
        self.play(Write(title))
        # Wait for a moment
        # Optional: Fade out the title
        self.play(FadeOut(title))
 

        # Create node Mobjects (Circles) at initial positions
        node_mobjects = []
        for i in range(1, num_nodes + 1):
            initial_pos = initial_positions[i]
            node = Circle(radius=0.03, color=BLUE, fill_opacity=1)
            node.move_to(initial_pos)
            node_mobjects.append(node)
            self.add(node)


        # Create initial lines based on initial node positions
        lines = []
        for start_index, end_index in lines_data:
            start_point = node_mobjects[start_index].get_center()
            end_point = node_mobjects[end_index].get_center()
            line = Line(start_point, end_point, color=GREEN)
            lines.append(line)
            self.add(line)

        deform_scale = 0.15
        # Animation: Move nodes according to relative displacements
        current_positions = initial_positions.copy()  # Track current positions
        for frame in range(1, num_frames):
            animations = []
            new_node_positions = {}


            for i in range(1, num_nodes + 1):
                dx = df[(df['frame'] == frame) & (df['node'] == i)]['dx'].iloc[0]
                dy = df[(df['frame'] == frame) & (df['node'] == i)]['dy'].iloc[0]
                current_x = current_positions[i][0]
                current_y = current_positions[i][1]
                new_x = current_x + dx*deform_scale
                new_y = current_y + dy*deform_scale
                new_pos = [new_x, new_y, 0]
                new_node_positions[i] = new_pos
                animations.append(node_mobjects[i-1].animate.move_to(new_pos))

                # Update current position for the next frame
                current_positions[i] = new_pos


            # Update line endpoints
            new_lines = []
            for start_index, end_index in lines_data:
                start_node = start_index + 1
                end_node = end_index + 1
                start_point = new_node_positions[start_node]
                end_point = new_node_positions[end_node]
                new_line = Line(start_point, end_point, color=GREEN)
                new_lines.append(new_line)

            # Transform the old lines into the new lines
            for i, line in enumerate(lines):
                animations.append(Transform(line, new_lines[i]))

            # Play animations for this frame
            self.play(*animations, run_time=1.5)

        self.wait(1)