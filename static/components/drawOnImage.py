from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def DrawOnImg(parsed, abstand, fileName):
    detection = parsed or " "
    print(abstand)
    img = Image.open('/home/pi/Desktop/tfjs-customvision/static/pictures/picture.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/pi/Downloads/Poppins-Bold.ttf")
    draw.text((50,50), detection,(242,186,34), font=font)
    draw.text((470, 430), "SmartFlap | Elias Englen", (242,186,34), font=font)
    img.save('/home/pi/Desktop/tfjs-customvision/static/pictures/' + fileName)