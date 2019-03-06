from Classes import Photo, Slide, SlideWithPoints #Profiler
import random
import copy


def printPercentage(slides_processed, elements):
    perc = 100 * slides_processed / elements
    print("{:.2f}%".format(perc), end="\r", flush=True)


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


'''
Sequential merging, takes verticals and merges sequentially into one slide.
best solution so far, with sequential and vertical slides on bottom of the
list giving over 1500 points
'''

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


# max 1550 on c
def sequentialMerge_verticalOnBottom(photos):
    h, v = _splitPhotosByOrientation(photos)
    slides_h = _horizontalPhotosToSlides(h)
    slides_v = _verticalPhotosToSlides_sequential(v)
    return slides_h + slides_v


# < 1500 on c
def sequentialMerge_shuffled(photos):
    slides = sequentialMerge_verticalOnBottom(photos)
    random.shuffle(slides)
    return slides


'''
Merging vertical photos that have the least amount of tags in common,
increments the amount of tags per slides but doesn't yield high scores.
The variant merging photos with the highest amount of tags in common
doesn't change the amount of tags per slides so much so it could improve
performances over input files with many tags, but produces even lower scores.
'''

def _verticalPhotosToSlides_leastCommonTags(photos_vertical):
    photos = copy.deepcopy(photos_vertical)
    slides = []
    for p in photos:
        first = photos.pop(photos.index(p))
        second = None
        max_common_tags = 1000
        for q in photos:
            common_tags = len(set(first.tags).intersection(q.tags))
            if (common_tags < max_common_tags):
                max_common_tags = common_tags
                second = photos.pop(photos.index(q))
            if (common_tags == 0):
                break
        if second:
            slides.append(Slide(first, second))
    return slides


# < 1300 on c
def leastCommonTagsMerge_verticalOnBottom(photos):
    h, v = _splitPhotosByOrientation(photos)
    slides_h = _horizontalPhotosToSlides(h)
    slides_v = _verticalPhotosToSlides_leastCommonTags(v)
    return slides_h + slides_v

# < 1250 on c
def leastCommonTagsMerge_shuffled(photos):
    slides = leastCommonTagsMerge_verticalOnBottom(photos)
    random.shuffle(slides)
    return slides


'''
Merging vertical photos with many tags with ones with few tags.
It works by ordering the photos by the tags count, then takes
first and last in list and joins them in one slide, then takes the
second and second to last and so on.
In theory it should balance the number of tags per slide.
'''

def _verticalPhotosToSlides_mostWithLeast(photos_vertical):
    photos = copy.deepcopy(photos_vertical)
    slides = []
    photos.sort(key=lambda x: len(x.tags))
    while(photos):
        slides.append(Slide(photos.pop(0), photos.pop(-1)))
    return slides


def mostWithLeast_verticalOnBottom(photos):
    h, v = _splitPhotosByOrientation(photos)
    slides_h = _horizontalPhotosToSlides(h)
    slides_v = _verticalPhotosToSlides_mostWithLeast(v)
    return slides_h + slides_v


# ALGORITHMS FOR SLIDES MATCHING DURING SLIDESHOW CREATION

def randomSlideshow(slides):
    slideshow = copy.deepcopy(slides)
    random.shuffle(slideshow)
    return slideshow


'''
This algorithm starts from the first slide in the list and then
searches for the next best matching slide and adds to the slideshow
list, then repeats for the last added slide. It is highly dependent
on starting slide order. First slides added in list get higher priority
in checking the best match over last ones which are sacrificed
The algorithm performs in O(n^2)
'''

def greedyPathSearch(slides):
    elements = (len(slides)) * (len(slides) - 1) / 2
    slides_processed = 0
    score = 0
    slideshow = []
    last = slides.pop(0)
    slideshow.append(last)
    while (slides):
        points = -1
        selected = None
        for slide in slides:
            if (slides_processed % 10000 == 0):
                printPercentage(slides_processed, elements)
            slides_processed += 1
            new_points = last.pointsTo(slide)
            if (new_points > points):
                points = new_points
                selected = slide
        if selected:
            score += points
            last = slides.pop(slides.index(selected))
            slideshow.append(last)
    print("", end="\r")
    return slideshow, score


'''
This algorithm generates from a list of slides a series of chains
that link together. First pass matches couples of nodes that have the
best score. Then each of these pairs is tested over each other pair to
find the best ones to link and where to link. Then this process is repeated
for each new chain until there is only one long chain that's the solution
'''

def pairMatchingAndLinking(slides):
    pass


'''
This algorithm starts from a random node and finds the best one to match.
Then, after removing taken nodes, testes the next one to find the best
position for it to be, adds it there and removes from the list. The cycles
repeats until no more node are in the list
'''

def putInTheBestPlace(slides):
    elements = (len(slides)) * (len(slides) - 1) / 2
    slides_processed = 0
    slideshow = []
    slideshow.append(SlideWithPoints(slides.pop(0)))
    # greedy select the second slide as best matching with first
    best_score = -1
    selected = None
    for slide in slides:
        if (slides_processed % 10000 == 0):
            printPercentage(slides_processed, elements)
        score = slide.pointsTo(slideshow[0])
        if (score > best_score):
            best_score = score
            selected = slide
        slides_processed += 1
    slideshow[0].points = best_score
    slideshow.append(SlideWithPoints(slides.pop(slides.index(selected))))
    # find best place to put every slide in the slideshow
    while (slides):
        popped = SlideWithPoints(slides.pop(0))
        best_delta = popped.pointsTo(slideshow[0])
        best_points1, best_points2 = 0, 0
        best_index = 0
        slides_processed += 1
        for i in range(1, len(slideshow)):
            if (slides_processed % 10000 == 0):
                printPercentage(slides_processed, elements)
            current_score = slideshow[i-1].points
            pts1 = popped.pointsTo(slideshow[i-1])
            pts2 = popped.pointsTo(slideshow[i])
            delta = pts1 + pts2 - current_score
            if (delta >= best_delta):
                best_delta = delta
                best_points1 = pts1
                best_points2 = pts2
                best_index = i
            slides_processed += 1
        delta = popped.pointsTo(slideshow[-1])
        slides_processed += 1
        if (delta >= best_delta):
            slideshow[-1].points = delta
            slideshow.append(popped)
        elif (best_index == 0):
            popped.points = best_delta
            slideshow.insert(0, popped)
        else:
            popped.points = best_points2
            slideshow[best_index-1].points = best_points1
            slideshow.insert(best_index, popped)
    print("", end="\r")
    score = sum([x.points for x in slideshow])
    return slideshow, score


# ALGORITHMS TO IMPROVE THE SCORE OF A SOLUTION

'''
This algorithm optimizes an already found solution with the greedy algorithm.
It takes the last and lower scoring slides and searches for places to put
them in order to increase the overall score. The score increase is not worth
the time it spends to calculate it, which is 4 times the first algorithm
'''

def improveSolution_aBetterPlace(slideshow):
    elements = (len(slideshow)) * (len(slideshow) - 1) / 2
    slides_processed = 0
    slideshow.reverse()
    pss = []
    for i in range(0, len(slideshow)):
        pss.append(SlideWithPoints(slideshow[i]))
        if i > 0:
            pss[i-1].setPointsTo(pss[i])
    for i in range(0, len(slideshow)-1):
        current = pss[i]
        current_score = current.points
        if (i > 0 and pss[i-1] is not None):
            current_score += pss[i-1].points
        higher_delta = 0
        candidate_insert = i
        best_points1 = 0
        best_points2 = 0
        for j in range(i+1, len(slideshow)-1):
            if (slides_processed % 10000 == 0):
                printPercentage(slides_processed, elements)
            slides_processed += 1
            pts1 = current.pointsTo(pss[j])
            pts2 = current.pointsTo(pss[j+1])
            previous_score = pss[j].points
            new_score = pts1 + pts2
            delta = (new_score - previous_score) - current_score
            if (delta > higher_delta):
                higher_delta = delta
                candidate_insert = j+1
                best_points1 = pts1
                best_points2 = pts2
        if (candidate_insert != i):
            pss[i] = None
            pss.insert(candidate_insert, current)
            pss[candidate_insert-1].points = best_points1
            pss[candidate_insert].points = best_points2
        print("", end="\r")
    return [x for x in pss if x is not None]


# !!! NOT WORKING PROPERLY
# repeat on whole array until no more swap increases the solution
def improveSolution_aBetterPlace2(slideshow):
    elements = len(slideshow)
    slides_processed = 0
    pss = [SlideWithPoints(x) for x in slideshow[::-1]]
    for i in range(0, len(pss)-1):
        pss[i].setPointsTo(pss[i+1])
    slideshow = []
    while (len(pss) > 1):
        swapped = False
        selected = pss[0]
        position = 0
        higher_delta = selected.pointsTo(pss[1])
        bp1, bp2 = 0, 0
        for i in range(1, len(pss)-1):
            if (slides_processed % 10000 == 0):
                printPercentage(len(slideshow), elements)
            slides_processed += 1
            pts1 = selected.pointsTo(pss[i])
            pts2 = selected.pointsTo(pss[i+1])
            previous_score = pss[i].points
            new_score = pts1 + pts2
            delta = new_score - previous_score
            if (delta > higher_delta):
                higher_delta = delta
                position = i+1
                bp1 = pts1
                bp2 = pts2
                swapped = True
        if swapped:
            pss.insert(position, selected)
            pss[position-1].points = bp1
            pss[position].points = bp2
        else:
            slideshow.append(selected)
        pss.pop(0)
    pss.pop(0)
    print("", end="\r")
    return slideshow
