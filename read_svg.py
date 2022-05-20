from svgpathtools import svg2paths2, wsvg
import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
from bresenham import bresenham
import math

def getSVG(fileName):
    paths, attributes, svg_attributes = svg2paths2(fileName)
    return [paths, attributes, svg_attributes]


def getOper(value, t):
    s, c1, c2, e = value
    firstOper = (1 - t)**3 * s
    secondOper = 3 * (1 - t)**2 * t * c1
    thirdOper = 3 * (1 - t) * t**2 * c2
    lastOper = t ** 3 * e

    return  firstOper + secondOper + thirdOper + lastOper

def getLength(a, b):
    x1, y1 = a
    x2, y2 = b

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def bezier(points):
    points = np.array(points)
    print(points)
    lines = []

    for i in range(0, 100):
        i /= 100
        x = getOper(points[:,0], i)
        y = getOper(points[:,1], i)
        lines.append((x, y))

    return lines

def getPoint(paths):
    xy = []

    for p in paths:
        for pp in p:
            
            if(len(pp) == 4):
                points = []
                
                try:

                    for controlPoint in pp:
                        cP = str(controlPoint)

                        if(cP != "None"):
                            cP = cP.rstrip(")").lstrip("(")
                            x_, y_ = cP.split("+")
                            y_ = y_.rstrip("j")

                        points.append([float(x_), float(y_)])

                    points = bezier(points)
                    xy += points
                        
                except:
                    pass

            else:
                
                b = []
                for controlPoint in pp:

                    cP = str(controlPoint)
                    try:
                        if(cP != "None"):
                            cP = cP.rstrip(")").lstrip("(")
                            x_, y_ = cP.split("+")
                            y_ = y_.rstrip("j")
                            x_, y_ = float(x_), float(y_)

                            xy.append([x_, y_])
                            b.append([int(x_), int(y_)])
                        

                    except:
                        # print(pp, cP, x_, y_)
                        pass
                
                if(len(b) == 2):
                    b = np.array(list(bresenham(b[0][0], b[0][1], b[1][0], b[1][1])))
                    xy += list(b)

    return xy


def v1_show(points, imgPath, fileName):
    points = np.array(points)

    # img = plt.imread(imgPath)
    # plt.imshow(img)
    plt.scatter(points[:,0], points[:,1], s = 0.5, color = "b")
    plt.axis("off")
    # plt.show()
    plt.savefig(f"./result/{fileName}.png")
    plt.cla()

def showPoints(points, imgPath, fileName):
    points = np.array(points)

    img = plt.imread(imgPath)
    h, w, c = img.shape
    fig, ax = plt.subplots()

    # ax.imshow(img)

    ax.margins(0)
    ax.set_axis_off()
    
    ax.scatter(points[:,0], points[:,1], s = 0.5, color = "b")
    fig.set_figwidth((h / fig.dpi) + (2.16 * 1.3))
    fig.set_figheight((w / fig.dpi) + (2.16 * 1.3))

    ax.invert_yaxis()
    fig.savefig(f"./result/{fileName}.png", bbox_inches='tight')
    plt.cla()

def writeSVG(svg, fileName):
    paths, attributes, svg_attributes = svg
    wsvg(paths, attributes=attributes, svg_attributes=svg_attributes, filename=fileName)


def readImage(fileName):
    return cv2.imread(fileName)


def main():
    svgPath = "./svg"
    pngPath = "./png"
    
    
    files = glob.glob((f"{svgPath}/*"))

    for file in files:
        fileName = file.split("\\")[-1].split(".")[0]
        
        svg = getSVG(f"{svgPath}/{fileName}.svg")

        points = getPoint(svg[0])

        showPoints(points, f"{pngPath}/{fileName}.png", fileName)

if(__name__ == "__main__"):
    main()