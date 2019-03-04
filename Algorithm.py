from Classes import Photo, Slide  # Profiler
import random


def generatePhotoList(file):
    photos = []
    lineNumber = 0
    for line in file:
        if (lineNumber != 0):
            photos.append(Photo(lineNumber-1, line))
        lineNumber += 1
    return photos


def generateSlideList(photos):
    return _createSlides_sequentialMerge_verticalOnBottom(photos)


def generateSlideshow(slides):
    return _followTheMostRewardingPath(slides)


def calculateScore(slideshow):
    points = 0
    for i in range(0, len(slideshow) - 1):
        points += slideshow[i].pointsTo(slideshow[i+1])
    return points


def generateOutputFile(file, slideshow):
    file.write(str(len(slideshow)) + "\n")
    for slide in slideshow:
        file.write(str(slide) + "\n")


# ALGORITHMS FOR VERTICAL MERGE DURING SLIDES CREATION

def _splitPhotosByOrientation(photos):
    horizontal = []
    vertical = []
    for photo in photos:
        if photo.isHorizontal:
            horizontal.append(photo)
        else:
            vertical.append(photo)
    return horizontal, vertical


def _horizontalPhotosToSlides(photos_horizontal):
    slides = []
    for photo in photos_horizontal:
        slides.append(Slide(photo))
    return slides


def _verticalPhotosToSlides_sequential(photos_vertical):
    slides = []
    first_vertical = None
    for photo in photos_vertical:
        if not first_vertical:
            first_vertical = photo
        else:
            slides.append(Slide(first_vertical, photo))
            first_vertical = None
    return slides


def _createSlides_sequentialMerge_verticalOnBottom(photos):
    h, v = _splitPhotosByOrientation(photos)
    slides_h = _horizontalPhotosToSlides(h)
    random.shuffle(v)
    slides_v = _verticalPhotosToSlides_sequential(v)
    return slides_h + slides_v


# ALGORITHMS FOR SLIDES MATCHING DURING SLIDESHOW CREATION

def _followTheMostRewardingPath(slides):
    # maybe not working properly, getting lower scores than expected
    # profiler = Profiler()
    # profiler.disable()
    elements = (len(slides)) * (len(slides) - 1) / 2
    slides_processed = 0
    score = 0
    slideshow = []
    last = slides.pop(0)
    slideshow.append(last)
    # profiler.start()
    while (slides):
        points = -1
        selected = None
        for slide in slides:
            if (slides_processed % 10000 == 0):
                perc = 100 * slides_processed / elements
                print("\b\b\b\b\b\b\b{:.2f}%".format(perc), end="", flush=True)
            slides_processed += 1
            new_points = last.pointsTo(slide)
            if (new_points > points):
                points = new_points
                selected = slide
        if selected:
            score += points
            last = slides.pop(slides.index(selected))
            slideshow.append(last)
    #         profiler.stop("PROCESSING 100 SLIDES")
    #         profiler.start()
    # profiler.stop("PROCESSING LAST SLIDES")
    print("\b\b\b\b\b\b\bCOMPLETED")
    return slideshow, score
