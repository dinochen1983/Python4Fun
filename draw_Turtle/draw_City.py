import turtle
import math
import random


def draw_polygon(points, fill_color=None):
    # 创建画笔
    pen.speed("fastest")
    # 移动到第一个顶点
    pen.penup()

    pen.goto(points[0])
    pen.pendown()
    pen.color('white')
    pen.width(2)
    # 如果设置了填充颜色，则开始填充多边形内部颜色
    if fill_color is not None:
        pen.fillcolor(fill_color)
        pen.begin_fill()

    # 循环绘制多边形的边
    for point in points[1:]:
        pen.goto(point)

    # 回到第一个顶点，完成多边形闭合
    pen.goto(points[0])

    # 如果设置了填充颜色，则结束填充多边形内部颜色
    if fill_color is not None:
        pen.end_fill()

    # 隐藏画笔
    pen.hideturtle()


def draw_rectangle(x, y, width, height, color):
    # 创建画笔
    pen.speed("fastest")
    turtle.tracer(0)
    # 移动到起始点
    pen.penup()
    pen.goto(x, y)
    pen.pendown()

    # 设置填充颜色
    pen.fillcolor(color)

    # 开始填充
    pen.begin_fill()

    # 绘制矩形
    for i in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)

    # 结束填充
    pen.end_fill()

    # 隐藏画笔
    pen.hideturtle()

    # 更新画布
    turtle.update()

    # 显示绘制结果


def draw_circle(x, y, diameter, color):
    # 创建画笔
    pen.speed("fastest")
    turtle.tracer(0)
    # 移动到圆心
    pen.penup()
    pen.goto(x, y - diameter / 2)
    pen.pendown()

    # 设置画笔颜色和填充颜色
    pen.color(color)
    pen.fillcolor(color)

    # 开始填充
    pen.begin_fill()

    # 绘制圆形
    pen.circle(diameter / 2)

    # 结束填充
    pen.end_fill()

    # 隐藏画笔
    pen.hideturtle()

    # 更新画布


def draw_line(start_x, start_y, end_x, end_y, color="white", width=0):
    # 创建画笔
    pen = turtle.Turtle()
    turtle.tracer(0)
    # 设置画笔属性
    pen.color(color)
    pen.pensize(width)
    
    # 绘制直线
    pen.penup()
    pen.goto(start_x, start_y)
    pen.pendown()
    pen.goto(end_x, end_y)
    pen.penup()
    pen.hideturtle()
    # 更新画布
    ##turtle.update()



# 设置画布大小为800x800
turtle.setup(800, 800)

# 定义多边形的顶点坐标
points = [
(-400,400),
(400,400),
(400,-141),
(327,-141),
(327,-43),
(284,-43),
(284,-111),
(279,-111),
(279,13),
(273,13),
(273,52),
(267,52),
(267,82),
(261,82),
(261,107),
(230,107),
(230,82),
(223,82),
(223,52),
(216,52),
(216,15),
(210,15),
(210,-107),
(205,-110),
(205,1),
(194,1),
(194,-112),
(190,-112),
(190,-31),
(154,-31),
(154,-47),
(132,-47),
(132,-9),
(70,-9),
(70,-45),
(52,-45),
(52,-6),
(45,1),
(45,15),
(41,15),
(41,3),
(36,9),
(32,6),
(32,30),
(27,30),
(27,3),
(15,-6),
(15,-119),
(3,-119),
(3,-9),
(-45,-9),
(-45,12),
(-84,12),
(-84,-62),
(-89,-62),
(-89,6),
(-103,6),
(-103,-69),
(-109,-69),
(-109,-7),
(-133,-7),
(-133,24),
(-155,46),
(-155,70),
(-160,70),
(-160,46),
(-183,25),
(-183,-115),
(-190,-115),
(-190,-41),
(-241,-41),
(-241,-106),
(-256,-106),
(-256,-41),
(-311,-41),
(-311,-141),
(-400,-141)
]

pen = turtle.Turtle()
draw_rectangle(-400, -400, 800, 800, "black")


##draw helix
pen = turtle.Turtle()
turtle.tracer(0)
# 定义螺线的参数
a = 0.2
b = 0.01

# 设置画笔颜色
color1 = (250/255, 137/255, 123/255)
color2 = (255/255, 221/255, 149/255)
color3 = (208/255, 230/255, 165/255)
color4 = (137/255, 227/255, 206/255)
color5 = (204/255, 171/255, 217/255)

colors = [color1, color2, color3, color4, color5]
color_index = 0
# 绘制螺线
for t in range(0, 1500):
    x = (a + b * t) * math.cos(t*0.5)
    y = (a + b * t) * math.sin(t*0.5)
    pw = random.randint(1, 10)
    pen.width(pw)
    pen.goto(x * 50, y * 50-200)
    pen.pencolor(colors[color_index])
    color_index = (color_index + 1) % len(colors)

# 隐藏画笔
pen.hideturtle()

# 绘制多边形并填充颜色
draw_polygon(points, (0/255, 0/255, 0/255))

draw_rectangle(-400, -400, 800, 200, (0/255, 3/255, 56/255))
draw_circle(200,250,75,'yellow')
draw_circle(200-20,250,75,'black')

points2 = []
for i in range(100):
    x = random.randint(-400, 400)
    y = random.randint(0, 400)
    points2.append((x, y))

for point in points2:
    x,y =point
    draw_circle(x,y,1,'white')


points3 = []
lens = []
for i in range(500):
    x = random.randint(-400, 400)
    y = random.randint(-400, -200)
    len1 = random.randint(20, 50)
    points3.append((x, y))
    lens.append(len1)

##def draw_line(start_x, start_y, end_x, end_y, color="white", width=2):
color_index = 0
num = 0
for point in points3:
    x,y =point
    color_index = (color_index + 1) % len(colors)
    len1 = lens[num]
    draw_line(x,y,x+len1,y,colors[color_index],2)
    num = num +1



draw_polygon(points)

# 等待用户关闭窗口
turtle.done()