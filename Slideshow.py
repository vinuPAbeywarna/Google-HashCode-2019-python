from Classes import Profiler
import Algorithm
import random
# import pickle

inputFileNames = {
    "a": "a_example",
    "b": "b_lovely_landscapes",
    "c": "c_memorable_moments",
    "d": "d_pet_pictures",
    "e": "e_shiny_selfies"
}


def main_run():

    p = Profiler()
    tp = Profiler()
    tp.start()

    print("\nSTARTED...")

    # acquiring the input
    letter = input("\nType input file letter -> ")
    inputName = inputFileNames[letter]
    p.start()
    try:
        with open("input/{}.txt".format(inputName), "r") as inputFile:
            photos = Algorithm.generatePhotoList(inputFile)
    except IOError:
        print("!!! NO INPUT WITH THAT NAME IN INPUT FOLDER !!!")
        exit()
    p.stop("INPUT ACQUIRED")
    print("NUMBER OF PHOTOS: " + str(len(photos)))

    # shuffling the photos
    # restore_state = input("\nDo you want to load .rsbk file? [y/n] -> ")
    # p.start()
    # if (restore_state in ["y", "Y", "s", "S", "yes", "YES", "Yes"]):
    #     try:
    #         with open("output/.{}.rsbk".format(inputName), "rb") as rsbk:
    #             random_state = pickle.load(rsbk)
    #             random.setstate(random_state)
    #     except IOError:
    #         print("!!! NO .rsbk FILE FOUND !!!")
    # random_state = random.getstate()
    random.shuffle(photos)
    p.stop("PHOTO SHUFFLED")
    p.start()
    slides = Algorithm.generateSlideList(photos)
    del photos
    p.stop("SLIDES CREATED")
    print("\nGENERATING SLIDESHOW...")
    p.start()
    slideshow, score = Algorithm.generateSlideshow(slides, verbose=True)
    del slides
    p.stop("SLIDESHOW GENERATED")
    print("\nFound solution with score {}.".format(score))
    dump_allowed = input("Do you want to write the output? [y/n] -> ")
    if (dump_allowed in ["y", "Y", "s", "S", "yes", "YES", "Yes"]):
        # with open("output/.{}.rsbk".format(inputName), "wb") as rsbk:
        #     pickle.dump(random_state, rsbk)
        with open("output/{}_out_{}.txt".format(inputName, score), "w") as out:
            out.write(str(len(slideshow)) + "\n")
            for slide in slideshow:
                out.write(str(slide) + "\n")
    tp.stop("COMPLETED")
    input("\nPress ENTER to exit...")


if __name__ == "__main__":
    main_run()
