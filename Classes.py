import time


class Photo:
    def __init__(self, id, line):
        param = line.split(" ")
        self.id = id
        self.isHorizontal = True if param[0] == "H" else False
        tags_unstripped = param[2::]
        self.tags = set([x.strip() for x in tags_unstripped])

    def pointsTo(self, slide):
        intersection = len(self.tags & slide.tags)
        if intersection == 0:
            return 0
        diff_self = len(self.tags) - intersection
        if diff_self == 0:
            return 0
        diff_slide = len(slide.tags) - intersection
        if diff_slide == 0:
            return 0
        return min(diff_self, intersection, diff_slide)


class Slide:
    def __init__(self, photo):
        self.photo1_n = photo.id
        self.photo2_n = None
        self.tags = photo.tags
        self.points = 0
        self.isHorizontal = photo.isHorizontal

    def addVertical(self, photo):
        if photo.isHorizontal:
           print("Cannot put an horizontal photo in a slide with a vertical one") 
        else:
            self.photo2_n = photo.id
            self.tags.update(photo.tags)

    def previewPointsTo(self, photo, slide):
        prev_tags = self.tags.union(photo.tags)
        inters = len(prev_tags & slide.tags)
        if inters == 0:
            return 0
        diff1 = len(prev_tags) - inters
        if diff1 == 0:
            return 0
        diff2 = len(slide.tags) - inters
        if diff2 == 0:
            return 0
        return min(diff1, inters, diff2)

    def pointsTo(self, slide):
        intersection = len(self.tags & slide.tags)
        if intersection == 0:
            return 0
        diff_self = len(self.tags) - intersection
        if diff_self == 0:
            return 0
        diff_slide = len(slide.tags) - intersection
        if diff_slide == 0:
            return 0
        return min(diff_self, intersection, diff_slide)

    def __str__(self):
        line = str(self.photo1_n)
        if (self.photo2_n is not None):
            line += " " + str(self.photo2_n)
        return line
