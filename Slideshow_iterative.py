# from Classes import Profiler
import Algorithm
import random

inputFileNames = {
    "a": "a_example",
    "b": "b_lovely_landscapes",
    "c": "c_memorable_moments",
    "d": "d_pet_pictures",
    "e": "e_shiny_selfies"
}


def main_run():
    print("\nSTARTED...")

    letter = input("\nType input file letter -> ")
    inputName = inputFileNames[letter]
    try:
        with open("input/{}.txt".format(inputName), "r") as inputFile:
            photos = Algorithm.generatePhotoList(inputFile)
    except IOError:
        print("!!! {}.txt NOT FOUND IN INPUT FOLDER !!!".format(inputName))
        exit()

    best_score = 0
    while(True):
        random.shuffle(photos)
        slides = Algorithm.generateSlideList(photos)
        slideshow, score = Algorithm.generateSlideshow(slides)
        del slides
        if (score > best_score):
            best_score = score
            print("\nFound solution with score {}.".format(score))
            outputFileName = "output/{}_out_{}.txt".format(inputName, score)
            with open(outputFileName, "w") as out:
                out.write(str(len(slideshow)) + "\n")
                for slide in slideshow:
                    out.write(str(slide) + "\n")

    print("BEST SCORE: {}".format(best_score))
    input("\nPress ENTER to exit...")


if __name__ == "__main__":
    main_run()
