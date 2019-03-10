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


def improve_run():
    filePath = input("\nSolution file to improve -> ")
    filePath.replace("\\", "/")
    k = filePath.rfind("/")
    folder = filePath[:k]
    inputName = inputFileNames[filePath[k+1:k+2]]
    try:
        with open("input/{}.txt".format(inputName), "r") as inputFile:
            photos = Algorithm.generatePhotoList(inputFile)
        with open(filePath, "r") as solutionFile:
            slideshow = Algorithm.recreateSolution(solutionFile, photos)
    except IOError:
        print("!!! NO INPUT WITH THAT NAME IN INPUT FOLDER !!!")
        exit()
    old_score = Algorithm.calculateScore(slideshow)
    slideshow = Algorithm.improveSolution(slideshow)
    score = Algorithm.calculateScore(slideshow)
    text = "Old: {}, New: {}, improved by {}".format(old_score, score, score - old_score)
    print(text)
    with open("{}/{}_out_{}.txt".format(folder, inputName, score), "w") as out:
        Algorithm.generateOutputFile(out, slideshow)


if __name__ == "__main__":
    improve_run()
