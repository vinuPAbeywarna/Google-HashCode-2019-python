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
        self.tags = param[2::]


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
