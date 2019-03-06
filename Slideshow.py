from Classes import Profiler
import Algorithm
import random
import sys
import os

inputFileNames = {
    "a": "a_example",
    "b": "b_lovely_landscapes",
    "c": "c_memorable_moments",
    "d": "d_pet_pictures",
    "e": "e_shiny_selfies"
}


def main_run():

    arguments = [x.lower() for x in sys.argv[1::]]

    if ("help" in arguments):
        print_help()
        exit()

    if ("improve" in arguments):
        improve_run()
        exit()

    if ("analyze" in arguments):
        analyze_run()
        exit()

    p = Profiler()
    tp = Profiler()

    verbose = True if "verbose" in arguments else False
    test = True if "test" in arguments else False
    iterative = True if "iterative" in arguments else test
    auto = True if "auto" in arguments else test

    if not verbose:
        p.disable()
        tp.disable()

    tp.start()
    if verbose:
        print("\nSTARTED...")

    folder = input("\nOutput folder -> ") if not test else "E:/out"
    if not os.path.exists(folder):
        os.makedirs(folder)

    letter = input("\nType input file letter -> ").lower() if not test else "c"
    inputName = inputFileNames[letter]
    p.start()
    try:
        with open("input/{}.txt".format(inputName), "r") as inputFile:
            photos = Algorithm.generatePhotoList(inputFile)
    except IOError:
        print("!!! NO INPUT WITH THAT NAME IN INPUT FOLDER !!!")
        exit()
    if verbose:
        print("NUMBER OF PHOTOS: " + str(len(photos)))
    p.stop("INPUT ACQUIRED")
    print("\n")

    best_score = 0
    while(True):
        random.shuffle(photos)
        p.stop("PHOTO SHUFFLED")
        p.start()
        slides = Algorithm.generateSlideList(photos)
        slides.sort(key=lambda x: len(x.tags))
        if verbose:
            print("NUMBER OF SLIDES: " + str(len(slides)))
        p.stop("SLIDES CREATED")
        if verbose:
            print("GENERATING SLIDESHOW...")
        p.start()
        slideshow, score = Algorithm.generateSlideshow(slides)
        del slides
        p.stop("SLIDESHOW GENERATED")
        print("Found solution with score {}.".format(score))
        dump_allowed = "n"
        if not iterative:
            text = "Do you want to dump the solution? [y/n] -> "
            dump_allowed = input(text).lower() if not auto else "y"
        elif (score > best_score):
            if verbose:
                print("NEW BEST SCORE!!!")
            best_score = score
            if auto:
                dump_allowed = "y"
            else:
                text = "Do you want to dump the new high score? [y/n] -> "
                dump_allowed = input(text).lower()
        if (dump_allowed in ["y", "s", "yes"]):
            with open("{}/{}_out_{}.txt".format(folder, inputName, score), "w") as out:
                Algorithm.generateOutputFile(out, slideshow)
        if verbose:
            print("\n")
        if not iterative:
            break

    tp.stop("COMPLETED")
    if verbose:
        input("\nPress ENTER to exit...")


def print_help():
    print("improve\trun a script to improve a solution")
    print("help\tshow this message")
    print("test\ttest the process on file C")
    print("iter\trun as iterative process")
    print("verb\tverbose output")
    print("auto\tdump files automatically")


def improve_run():
    filePath = input("\nSolution file to improve -> ")
    filePath.replace("\\", "/")
    k = filePath.rfind("/")
    folder = filePath[:k]
    inputName = inputFileNames[filePath[k+1:k+2]]
    h = filePath.rfind("_")
    # declared_score = int(filePath[h+1:-4])
    try:
        with open("input/{}.txt".format(inputName), "r") as inputFile:
            photos = Algorithm.generatePhotoList(inputFile)
        with open(filePath, "r") as solutionFile:
            slideshow = Algorithm.recreateSolution(solutionFile, photos)
    except IOError:
        print("!!! NO INPUT WITH THAT NAME IN INPUT FOLDER !!!")
        exit()
    old_score = Algorithm.calculateScore(slideshow)
    # if (old_score != declared_score):
    #     print("ERROR WHILE RECREATING SOLUTION")
    #     return
    slideshow = Algorithm.improveSolution(slideshow)
    score = Algorithm.calculateScore(slideshow)
    text = "Old: {}, New: {}, improved by {}".format(old_score, score, score - old_score)
    print(text)
    with open("{}/{}_out_{}.txt".format(folder, inputName, score), "w") as out:
        Algorithm.generateOutputFile(out, slideshow)


def analyze_run():
    pass

if __name__ == "__main__":
    main_run()
