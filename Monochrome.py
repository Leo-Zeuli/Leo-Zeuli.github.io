from PIL import Image

original = Image.open("Watchmen-smiley.svg.png")
monochromed = Image.new("RGBA", original.size, (0, 0, 0, 255))

#print(original.getpixel((500,100)))

for i in range(original.size[0]):
    for j in range(original.size[1]):
        pixel = original.getpixel((i,j))
        if ((pixel == (0,0,0,0)) or (pixel[1:3] == (31, 37))):
        #if pixel != (0,0,0):
            monochromed.putpixel((i, j), (0, 0, 0, 0))

monochromed.save("monochromed.png")
