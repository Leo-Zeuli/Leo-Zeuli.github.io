from PIL import Image

original = Image.open("163692123258061987.png")
monochromed = Image.new("RGBA", original.size, (0, 0, 0, 0))

for i in range(original.size[0]):
    for j in range(original.size[1]):
        pixel = original.getpixel((i,j))
        if (pixel[0] > 100) or (pixel[1] > 100) or (pixel[2] > 100):
        #if pixel != (0,0,0):
            monochromed.putpixel((i, j), (0, 0, 0, 255))

monochromed.save("monochromed.png")
