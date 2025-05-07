from manim import *
import os
import pandas as pd
global time_values
global y_values

scale_factor = 5.5

def load_csv_data():
    global time_values
    global y_values
    
    # Load the CSV file
    df = pd.read_csv('data.csv')
    
    # Extract the time and y-value columns
    time_values = df['time'].to_numpy()
    y_values = df['value'].to_numpy()

load_csv_data()


class Test(Scene):

    def construct(self):

        def get_y_value(time):
            global time_values
            global y_values
            
            # Find the index of the closest time value
            time_index = np.argmin(np.abs(time_values - time))
            
            # Return the corresponding y-value
            return y_values[time_index]

        # create a value tracker that updates the scene with an x-value
        vt = ValueTracker(0)

        # declare x and y axes
        ax = Axes(x_range=[0, 1000, 50], y_range=[-50, 50, 10], y_length = 4, x_length = 6)

        # declare the two functions but always update their upper end to the ValueTracker
        f1 = always_redraw(lambda: ax.plot(lambda x: scale_factor*get_y_value(x), color=BLUE, x_range=[0,vt.get_value()]))
 
        # declare two dots to trace the two functions, also pointed to the ValueTracker
        f1_dot = always_redraw(lambda: Dot(
                    point=ax.c2p(vt.get_value(), f1.underlying_function(vt.get_value())),
                    color=YELLOW
                )
            )

        text = Text('Top Disp').scale(0.5)
        text.move_to(RIGHT*3.0)
        text.shift([0,-2.5,0])
        self.add(text)

        # Animate the axis being drawn
        ax = ax.move_to(RIGHT*3.0)
        self.play(Write(ax), run_time=0.5)
        self.add(f1, f1_dot)
        # Animate the ValueTracker across 6 seconds, updating the plots and tracing dots
        self.play(vt.animate.set_value(2000), run_time=5)
        # Fade out the dots
        self.wait()

