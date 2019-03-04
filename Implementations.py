from Classes import Photo, Slide  # Profiler
import random
import copy


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

'''
This algorithm starts from the first slide in the list and then
searches for the next best matching slide and adds to the slideshow
list, then repeats for the last added slide. It is highly dependent
on starting slide order. First slides added in list get higher priority
in checking the best match over last ones which are sacrificed
The algorithm performs in O(n^2)
'''

def followTheMostRewardingPath(slides, verbose):
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
            if (verbose and slides_processed % 10000 == 0):
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
    if verbose:
        print("\b\b\b\b\b\b\bCOMPLETED")
    return slideshow, score
