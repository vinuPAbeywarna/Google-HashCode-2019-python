import time


class Profiler:
    def __init__(self):
        self.start_time = None
        self.enabled = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def start(self):
        if not self.enabled:
            return
        self.start_time = time.time()

    def stop(self, name):
        if not self.enabled:
            return
        elapsed_time = time.time() - self.start_time
        print(name + " in: " + str(elapsed_time) + " s")


class Photo:
    def __init__(self, id, line):
        param = line.split(" ")
        self.id = id
        self.isHorizontal = True if param[0] == "H" else False
        tags_unstripped = param[2::]
        self.tags = [x.strip() for x in tags_unstripped]


class Slide:
    def __init__(self, photo1, photo2=None):
        self.photo1_n = photo1.id
        self.photo2_n = photo2.id if photo2 else None
        self.tags = set(photo1.tags)
        if photo2:
            self.tags.update(photo2.tags)

    def __str__(self):
        line = str(self.photo1_n)
        if (self.photo2_n is not None):
            line += " " + str(self.photo2_n)
        return line

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


class SlideWithPoints(Slide):
    def __init__(self, slide):
        self.photo1_n = slide.photo1_n
        self.photo2_n = slide.photo2_n
        self.tags = slide.tags
        self.points = 0

    def setPointsTo(self, slide):
        self.points = self.pointsTo(slide)
        return self.points


class SlideLT(SlideWithPoints):
    def __init__(self, LT, slide):
        super().__init__(slide)
        self.tags = [LT.getCode(x) for x in self.tags]
        self.tags.sort()
    
    def pointsTo(self, slide):
        inters = 0
        for tag in self.tags:
            if tag in slide.tags:
                inters += 1
        diff1 = len(self.tags) - inters
        diff2 = len(slide.tags) - inters
        return min(diff1, inters, diff2)


class TagsLookupTable():
    def __init__(self):
        self.tags = []
    
    def getCode(self, tag):
        code = None
        if tag in self.tags:
            code = self.tags.index(tag)
        else:
            self.tags.append(tag)
            code = len(self.tags)
        return code

    def getTag(self, code):
        tag = None
        if code < len(self.tags):
            tag = self.tags[code]
        else:
            print("No tag with code {}".format(code))
        return tag
