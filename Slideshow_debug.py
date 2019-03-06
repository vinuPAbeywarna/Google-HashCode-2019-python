# from Classes import Profiler
import Algorithm
import random
import os
from Slideshow import improve_run

inputFileNames = {
    "a": "a_example",
    "b": "b_lovely_landscapes",
    "c": "c_memorable_moments",
    "d": "d_pet_pictures",
    "e": "e_shiny_selfies"
}

def main_run():
    print("\nSTARTED...")
    folder = ("E:/out")
    if not os.path.exists(folder):
        os.makedirs(folder)
    letter = "c"
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
        if (score > best_score):
            best_score = score
            print("Found solution with score {}.".format(score))
            outputFileName = "{}/{}_out_{}.txt".format(folder, inputName, score)
            with open(outputFileName, "w") as out:
                out.write(str(len(slideshow)) + "\n")
                for slide in slideshow:
                    out.write(str(slide) + "\n")


if __name__ == "__main__":
    improve_run()
    main_run()
