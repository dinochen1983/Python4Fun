from manim import *
import numpy as np

class MovingBallsWithLinks(Scene):
    def construct(self):
        # Load data from files with error handling
        try:
            story1 = np.loadtxt("STORY1.txt")
            story2 = np.loadtxt("STORY2.txt")
            story3 = np.loadtxt("STORY3.txt")
            story4 = np.loadtxt("STORY4.txt")
        except FileNotFoundError:
            self.play(Write(Text("Error: STORY files not found!")))
            self.wait(3)
            return  # Exit if files are missing
        except ValueError:
            self.play(Write(Text("Error: Invalid data in STORY files!")))
            self.wait(3)
            return  # Exit if data is invalid

        # Number of frames based on the shortest data length
        num_frames = min(len(story1), len(story2), len(story3), len(story4))
        x_scale = 0.45
        start_x = -4

        # Create the balls
        ball1 = Dot(point=[start_x, 3, 0], color=RED, radius=0.2)
        ball2 = Dot(point=[start_x, 1.5, 0], color=GREEN, radius=0.2)
        ball3 = Dot(point=[start_x, 0, 0], color=BLUE, radius=0.2)
        ball4 = Dot(point=[start_x, -1.5, 0], color=YELLOW, radius=0.2)
        ball5 = Dot(point=[start_x, -3, 0], color=PURPLE, radius=0.2) # Fifth ball, no movement

        self.add(ball1, ball2, ball3, ball4, ball5)

        # Create the lines (links)
        line1 = Line(ball1.get_center(), ball2.get_center(), color=WHITE)
        line2 = Line(ball2.get_center(), ball3.get_center(), color=WHITE)
        line3 = Line(ball3.get_center(), ball4.get_center(), color=WHITE)
        line4 = Line(ball4.get_center(), ball5.get_center(), color=WHITE)

        self.add(line1, line2, line3, line4)

        # Create animation for each ball
        def update_ball1(ball,alpha):
            x_pos = story4[int(alpha * (num_frames - 1))]*x_scale + start_x  # Interpolate x position
            ball.move_to([x_pos, 3, 0])
            line1.become(Line(ball.get_center(), ball2.get_center(), color=WHITE)) # Update line

        def update_ball2(ball, alpha):
            x_pos = story3[int(alpha * (num_frames - 1))]*x_scale  + start_x 
            ball.move_to([x_pos, 1.5, 0])
            line1.become(Line(ball1.get_center(), ball.get_center(), color=WHITE)) # Update line

        def update_ball3(ball, alpha):
            x_pos = story2[int(alpha * (num_frames - 1))]*x_scale  + start_x 
            ball.move_to([x_pos, 0, 0])
            line2.become(Line(ball2.get_center(), ball.get_center(), color=WHITE)) # Update line

        def update_ball4(ball, alpha):
            x_pos = story1[int(alpha * (num_frames - 1))]*x_scale  + start_x 
            ball.move_to([x_pos, -1.5, 0])
            line3.become(Line(ball3.get_center(), ball.get_center(), color=WHITE)) # Update line

        def update_ball5(ball, alpha):
            # Ball 5 doesn't move, but we still need to update its line
            line4.become(Line(ball4.get_center(), ball.get_center(), color=WHITE)) # Update line


        def update_line1(line1,alpha):
            x_pos1 = story4[int(alpha * (num_frames - 1))]*x_scale  + start_x  # Interpolate x position
            ball1.move_to([x_pos1, 3, 0])
            x_pos2 = story3[int(alpha * (num_frames - 1))]*x_scale  + start_x   # Interpolate x position
            ball2.move_to([x_pos2, 1.5, 0])
            line1.become(Line(ball1.get_center(), ball2.get_center(), color=WHITE)) # Update line

        def update_line2(line,alpha):
            x_pos1 = story3[int(alpha * (num_frames - 1))]*x_scale  + start_x   # Interpolate x position
            ball2.move_to([x_pos1, 1.5, 0])
            x_pos2 = story2[int(alpha * (num_frames - 1))]*x_scale  + start_x   # Interpolate x position
            ball3.move_to([x_pos2, 0, 0])
            line.become(Line(ball2.get_center(), ball3.get_center(), color=WHITE)) # Update line

        def update_line3(line,alpha):
            x_pos1 = story2[int(alpha * (num_frames - 1))]*x_scale + start_x  # Interpolate x position
            ball3.move_to([x_pos1, 0, 0])
            x_pos2 = story1[int(alpha * (num_frames - 1))]*x_scale + start_x   # Interpolate x position
            ball4.move_to([x_pos2, -1.5, 0])
            line.become(Line(ball3.get_center(), ball4.get_center(), color=WHITE)) # Update line

        def update_line4(line,alpha):
            x_pos1 = story1[int(alpha * (num_frames - 1))]*x_scale + start_x   # Interpolate x position
            ball4.move_to([x_pos1, -1.5, 0])
            x_pos2 = 0.0  + start_x 
            ball5.move_to([x_pos2, -3, 0])
            line.become(Line(ball4.get_center(), ball5.get_center(), color=WHITE)) # Update line

        # Create the animations
        anim1 = UpdateFromAlphaFunc(ball1, update_ball1)
        anim2 = UpdateFromAlphaFunc(ball2, update_ball2)
        anim3 = UpdateFromAlphaFunc(ball3, update_ball3)
        anim4 = UpdateFromAlphaFunc(ball4, update_ball4)
        anim5 = UpdateFromAlphaFunc(ball5, update_ball5) # Even though it doesn't move
        ##line
        anim6 = UpdateFromAlphaFunc(line1, update_line1)
        anim7 = UpdateFromAlphaFunc(line2, update_line2)
        anim8 = UpdateFromAlphaFunc(line3, update_line3)
        anim9 = UpdateFromAlphaFunc(line4, update_line4)

        # Create the curve from the data
        # Play the animations
        self.play(AnimationGroup(anim1,anim2, anim3, anim4, anim5, anim6,anim7,anim8,anim9), run_time=num_frames * 0.005)  # Total animation time


        self.wait(1) # Wait for 1 second at the end