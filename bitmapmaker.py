from PIL import Image

# Open a PNG image
img = Image.open(r' ')# insert img location here ex: img = Image.open(r'C:\Users\chala\OneDrive\Documents\bitmaps\images\topright.png')

pixels = img.load()
width, height = img.size

output = ""
lineHex = ""
bitstring = ""
i = 0
if width%8 == 0:
    for y in range(0, height):
        for x in range(0, width):
            i += 1
            
                
            if pixels[x, y][0] == 0: # dark = bit
                bitstring += "1"

            else:
                bitstring += "0"
                
            if i == 8:
                val = 0
                for num in range (1, 9):
                    val += int(bitstring[-num])*(2**(num-1))
                bitstring = ""
                a = str(hex(val))
                lineHex += a if len(a) == 4 else "0x0"+a[-1]
                lineHex += ", "
                i = 0
            
        output+=lineHex+"\n"
        
        lineHex = ""
        
else:
    print("Error: width not multiple of 8")
    print("Height is fine :)")
        
print(output)
        
print("thanks for using my img to bitmap converter :)")
print("until next time :D")
