import Algorithm
import random
import os
import sys

inputFileNames = {
    "a": "a_example",
    "b": "b_lovely_landscapes",
    "c": "c_memorable_moments",
    "d": "d_pet_pictures",
    "e": "e_shiny_selfies"
}

def main_run():
    arguments = [x.lower() for x in sys.argv[1::]]
    if len(arguments) == 0:
        letter = "c"
    else:
        letter = arguments[0]

    print("\nSTARTED...")
    folder = ("E:/out")
    if not os.path.exists(folder):
        os.makedirs(folder)
    inputName = inputFileNames[letter]
    try:
        with open("input/{}.txt".format(inputName), "r") as inputFile:
            photos = Algorithm.generatePhotoList(inputFile)
    except IOError:
        print("!!! {}.txt NOT FOUND IN INPUT FOLDER !!!".format(inputName))
        exit()

    slideshow = Algorithm.generateSlideshow(photos)
    score = sum(x.points for x in slideshow[:-2])
    print("Found solution with score {}.".format(score))
    outputFileName = "{}/{}_out_{}.txt".format(folder, inputName, score)
    with open(outputFileName, "w") as out:
        out.write(str(len(slideshow)) + "\n")
        for slide in slideshow:
            out.write(str(slide) + "\n")


if __name__ == "__main__":
    main_run()
