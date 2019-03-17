from Classes import Photo, Slide
import random
import copy


def printPercentage(slides_processed, elements):
    perc = 100 * slides_processed / elements
    print("{:.2f}%".format(perc), end="\r", flush=True)


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
        slide = Slide(p1)
        if p2:
            slide.addVertical(p2)
        slideshow.append(slide)
    return slideshow


def generatePhotoList(file):
    photos = []
    lineNumber = 0
    for line in file:
        if (lineNumber != 0):
            photos.append(Photo(lineNumber-1, line))
        lineNumber += 1
    return photos


def generateSlideshow(photos_toCopy):
    '''
    it's a greedy algorithm that searches for best slide looking from
    the last one. If the last one is vertical, searches for another vertical
    to match that increases the score the most (or if not, at least the one
    that decreases the less)
    '''
    photos = copy.deepcopy(photos_toCopy)
    photos.sort(key=lambda x: len(x.tags))
    elements = len(photos)
    slideshow = []
    last = None
    for photo in photos:
        if photo.isHorizontal:
            last = Slide(photos.pop(photos.index(photo)))
            photos_processed = 1
            break
    if last is None:
        last = Slide(photos.pop(0))
        last.addVertical(photos.pop(0))
        photos_processed = 2
    slideshow.append(last)
    while (photos):
        printPercentage(photos_processed, elements)
        points = -1
        selected = None
        for p in photos:
            new_points = last.pointsTo(p)
            if (new_points > points):
                points = new_points
                selected = p
        if selected:
            last = Slide(photos.pop(photos.index(selected)))
            if selected.isHorizontal:
                photos_processed += 1
            else:
                match = None
                best_delta = -1000
                for p in [x for x in photos if not x.isHorizontal]:
                    new_points = last.previewPointsTo(p, slideshow[-1])
                    delta = new_points - points
                    if (delta > best_delta):
                        best_delta = delta
                        match = p
                if match:
                    points += best_delta
                    last.addVertical(photos.pop(photos.index(match)))
                    photos_processed += 2
            slideshow[-1].points = points
            slideshow.append(last)
    print("       ", end="\r")
    return slideshow


def generateSlideshow_prevident(photos_toCopy):
    '''
    greedy algorithm that works on a sorted by len(tags) photo list
    it searches for the next best photo to add into the slideshow.
    It searches the best horizontal and the best vertical. It also searches
    for the next vertical to match the first one with the highest score. If
    it then surpasses the horizontal one choses the verticals else the horizontal
    '''
    photos = copy.deepcopy(photos_toCopy)
    photos.sort(key=lambda x: len(x.tags))
    elements = len(photos)
    slideshow = []
    last = None
    for photo in photos:
        if photo.isHorizontal:
            last = Slide(photos.pop(photos.index(photo)))
            photos_processed = 1
            break
    if last is None:
        last = Slide(photos.pop(0))
        last.addVertical(photos.pop(0))
        photos_processed = 2
    slideshow.append(last)
    while (photos):
        printPercentage(photos_processed, elements)
        points_v = -1
        points_h = -1
        selected_h = None
        selected_v1 = None
        selected_v2 = None
        for p in photos:
            new_points = last.pointsTo(p)
            if (p.isHorizontal and new_points > points_h):
                points_h = new_points
                selected_h = p
            if (not p.isHorizontal and new_points > points_v):
                points_v = new_points
                selected_v1 = p
        if selected_v1:
            proposed = Slide(selected_v1)
            best_delta = -1000
            for p in [x for x in photos if not x.isHorizontal]:
                if (p is not selected_v1):
                    new_points = proposed.previewPointsTo(p, slideshow[-1])
                    delta = new_points - points_v
                    if (delta > best_delta):
                        best_delta = delta
                        selected_v2 = p
            if selected_v2:
                points_v += best_delta
        if (points_h > points_v):
            last = Slide(photos.pop(photos.index(selected_h)))
            slideshow[-1].points = points_h
            photos_processed += 1
        else:
            last = Slide(photos.pop(photos.index(selected_v1)))
            last.addVertical(photos.pop(photos.index(selected_v2)))
            slideshow[-1].points = points_v
            photos_processed += 2
        slideshow.append(last)
    print("       ", end="\r")
    return slideshow


def improveSolution(slideshow):
    '''
    after building a solution with the greedy algorithm it is possible to
    improve it searching for a better place to put the last added slides
    which have low priority in the greedy algorithm and usually give low scores.
    by placing in better places it's possible to improve the score up to 3%
    '''
    elements = (len(slideshow)) * (len(slideshow) - 1) / 2
    size = len(slideshow)
    slides_processed = 0
    slideshow.reverse()
    for i in range(1, size):
         slideshow[i-1].points = slideshow[i-1].pointsTo(slideshow[i])
    for i in range(0, size-1):
        current = slideshow[i]
        current_score = current.points
        if (i > 0 and slideshow[i-1] is not None):
            current_score += slideshow[i-1].points
        higher_delta = 0
        candidate_insert = i
        best_points1 = 0
        best_points2 = 0
        for j in range(i+1, size-1):
            if (slides_processed % 10000 == 0):
                printPercentage(slides_processed, elements)
            slides_processed += 1
            pts1 = current.pointsTo(slideshow[j])
            pts2 = current.pointsTo(slideshow[j+1])
            previous_score = slideshow[j].points
            new_score = pts1 + pts2
            delta = (new_score - previous_score) - current_score
            if (delta > higher_delta):
                higher_delta = delta
                candidate_insert = j+1
                best_points1 = pts1
                best_points2 = pts2
        if (candidate_insert != i):
            slideshow[i] = None
            slideshow.insert(candidate_insert, current)
            slideshow[candidate_insert-1].points = best_points1
            slideshow[candidate_insert].points = best_points2
        print("", end="\r")
    return [x for x in slideshow if x is not None]


    
