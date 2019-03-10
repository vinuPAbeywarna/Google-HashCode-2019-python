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
    it's a greedy algorithm that searches for best slide given the actual one
    it does not get an optimal solution, but it's fast and gives a good
    aproximation of it. Applied on randomly ordered slides and coupled with
    the improving algorithm gives a good score for the competition
    given the slideshow found with the greedy algorithm all the remaining verticals
    are matched with other verticals in places where they increase the overall score
    '''
    photos = copy.deepcopy(photos_toCopy)
    horizontals = sum(1 for x in photos if x.isHorizontal)
    verticals = len(photos) - horizontals
    verticals /= 2
    elements = len(photos)
    score = 0
    slideshow = []
    last = photos.pop(0)
    photos_processed = 1
    if last.isHorizontal:
        horizontals -= 1
    else:
        verticals -= 1
    slideshow.append(Slide(last))
    while (horizontals or verticals):
        printPercentage(photos_processed, elements)
        points = -1
        selected = None
        for p in photos:
            if (verticals <= 0 and not p.isHorizontal):
                continue
            new_points = last.pointsTo(p)
            if (new_points > points):
                points = new_points
                selected = p
        if selected:
            if selected.isHorizontal:
                horizontals -= 1
            else:
                verticals -= 1
            score += points
            last = photos.pop(photos.index(selected))
            slideshow.append(Slide(last))
            slideshow[-2].points = points
            photos_processed += 1
    # slideshow[-1].points = slideshow[-1].pointsTo(slideshow[0])
    for i in range(0, len(slideshow)-1):
        printPercentage(photos_processed, elements)
        if slideshow[i].isHorizontal:
            continue
        selected = None
        delta = 0
        bs1 = 0
        bs2 = 0
        for p in photos:
            ps1, ns1 = 0, 0
            if i > 0:
                ps1 = slideshow[i-1].points
                ns1 = slideshow[i].previewPointsTo(p, slideshow[i-1])
            ps2 = slideshow[i].points
            ns2 = slideshow[i].previewPointsTo(p, slideshow[i+1])
            new_delta = (ns1 + ns2) - (ps1 + ps2)
            if (new_delta >= delta):
                delta = new_delta
                selected = p
                bs1, bs2 = ns1, ns2
        if selected:
            slideshow[i].addVertical(photos.pop(photos.index(selected)))
            if i > 0:
                slideshow[i-1].points = bs1
            slideshow[i].points = bs2
        photos_processed += 1
    # min_points = 1000
    # index = 0
    # for i in range(0, len(slideshow)):
    #     if (slideshow[i].points < min_points):
    #         min_points = slideshow[i].points
    #         index = i
    # first_half = slideshow[:index+1]
    # second_half = slideshow[index:]
    print("       ", end="\r")
    return slideshow # second_half + first_half


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


    
