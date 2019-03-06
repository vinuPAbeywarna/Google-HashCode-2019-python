from Classes import Photo, Slide, Profiler
import Implementations
import random
import copy


def generatePhotoList(file):
    photos = []
    lineNumber = 0
    for line in file:
        if (lineNumber != 0):
            photos.append(Photo(lineNumber-1, line))
        lineNumber += 1
    return photos


def generateSlideList(photos):
    return Implementations.mostWithLeast_verticalOnBottom(photos)


def generateSlideshow(slides):
    return Implementations.greedyPathSearch(slides)


def improveSolution(slideshow):
    return Implementations.improveSolution_aBetterPlace(slideshow)


def calculateScore(slideshow):
    points = 0
    for i in range(0, len(slideshow) - 1):
        points += slideshow[i].pointsTo(slideshow[i+1])
    return points


def generateOutputFile(file, slideshow):
    file.write(str(len(slideshow)) + "\n")
    for slide in slideshow:
        file.write(str(slide) + "\n")


def recreateSolution(solutionFile, photos):
    slideshow = []
    next(solutionFile)
    for line in solutionFile:
        ids = line.split(" ")
        ids = [int(x.strip()) for x in ids]
        p1 = photos[ids[0]]
        p2 = photos[ids[1]] if len(ids) == 2 else None
        slideshow.append(Slide(p1, p2))
    return slideshow
