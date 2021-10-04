from PIL import Image

original = Image.open("_.png")
monochromed = Image.new("RGBA", original.size, (0, 0, 0, 0))

for i in range(original.size[0]):
    for j in range(original.size[1]):
        pixel = original.getpixel((i,j))
        if (pixel[0] < 220) and (pixel[1] < 220) and (pixel[2] < 220):
            monochromed.putpixel((i, j), (0, 0, 0, 255))

monochromed.save("monochromed.png")
