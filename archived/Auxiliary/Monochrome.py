from PIL import Image

original = Image.open("The Rehearsal Star copy.png").convert("RGBA")
#monochromed = Image.new("RGBA", original.size, (0, 0, 0, 255))
monochromed = original.copy()

for i in range(original.size[0]):
    for j in range(original.size[1]):
        pixel = original.getpixel((i,j))
        if pixel[0] > 15 or pixel[1] > 15 or pixel[2] > 15 or pixel[3] != 255:
            monochromed.putpixel((i, j), (0, 0, 0, 0))

monochromed.save("monochromed.png")
