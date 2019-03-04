from Classes import Photo, Slide  # Profiler
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


def generateSlideshow(slides, verbose):
    return Implementations.followTheMostRewardingPath(slides, verbose)


def calculateScore(slideshow):
    points = 0
    for i in range(0, len(slideshow) - 1):
        points += slideshow[i].pointsTo(slideshow[i+1])
    return points


def generateOutputFile(file, slideshow):
    file.write(str(len(slideshow)) + "\n")
    for slide in slideshow:
        file.write(str(slide) + "\n")
