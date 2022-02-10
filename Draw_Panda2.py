from csv import reader
from PIL import Image, ImageDraw
from PIL import ImageFont

from PIL import Image,ImageColor

image = Image.new('RGBA', (800, 800),(20, 20, 20))

draw = ImageDraw.Draw(image)

colortext2 = (232,43,123)


with open('panda.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        ##color
        if row[1] == '7':
            colortext2 = (255,255,255)
        elif row[1] == '250':
            colortext2 = (0,0,0)
        elif row[1] == '255':
            colortext2 = (0,0,0)            
        elif row[1] == '251':
            colortext2 = (120,120,120)            
        elif row[1] == '1':
            colortext2 = (255,0,0)
        elif row[1] == '4':
            colortext2 = (0,255,255)         
        elif row[1] == '5':
            colortext2 = (0,0,255)    
        elif row[1] == '2':
            colortext2 = (255,255,0)    
        elif row[1] == '6':
            colortext2 = (255,0,255)                  
        else:
            colortext2 = (255,0,0)


        if (row[0]=='Circle'):
            px = float(row[3])/20
            py = 800-float(row[4])/20
            rr = float(row[5])/20
            if (row[2]=='1'):
                draw.ellipse((px-rr, py-rr, px+rr, py+rr), fill = colortext2, outline =colortext2)
            if (row[2]=='0'):
                draw.ellipse((px-rr, py-rr, px+rr, py+rr), outline =colortext2, width=2)



        if (row[0]=='Poly'):
            np = int(row[2])
            xy = []
            for j in range(np):
                px = float(row[3+(j)*2])/20
                py = 800-float(row[4+(j)*2])/20
                rr = 1 
                xy.append((px,py))
     
            draw.polygon(xy,fill=colortext2,outline=colortext2)
     
          
        font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 12)  

    draw.text((365, 570), 'BEIJING', font = font, align ="left", fill = "red")  



image.save('Panda.png')
im = Image.open('Panda.png')
im.show()
