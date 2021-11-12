from PIL import Image

original = Image.open("_.jpg")
monochromed = Image.new("RGBA", original.size, (0, 0, 0, 0))

for i in range(original.size[0]):
    for j in range(original.size[1]):
        pixel = original.getpixel((i,j))
        if (pixel[0] < (240)) or (pixel[1] < (240)) or (pixel[2] < (240)):
            monochromed.putpixel((i, j), (0, 0, 0, 255))

monochromed.save("monochromed.png")
