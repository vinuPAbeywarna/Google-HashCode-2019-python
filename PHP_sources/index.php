<?php
/**
 * Created by PhpStorm.
 * User: Riccardo
 * Date: 28/02/2019
 * Time: 18:41
 */
include 'file_utils.class.php';
include 'Slide.php';

require_once "SlideshowCreation.php";

$file = new FileUtils('a_example.txt');
$slides = array();

$lines = $file->ReadLines();
$lines_verticali = array();

for ($i = 0; $i < count($lines); $i++){
    $params = explode(' ', $lines[$i]);

    if ($params[0] == 'H'){

        $tags = array();
        unset($params[1]);
        unset($params[0]);

        foreach ($params as $_tag) {
            $tags[] = trim($_tag);
        }

        array_push($slides , new Slide($i, $tags));
    }
    else{
        array_push($lines_verticali);
    }
}


$creation = new SlideshowCreation();

$slide1 = $slides[0];
$slide2 = new Slide(3,array('cat'),5, array('aa'));


$scoreTransizione = $creation->calcolaScoreTransizione($slide1, $slide2);

echo "punteggio transaz $scoreTransizione";


$slideArray = array($slide1, $slide2);

$utils = new FileUtils("output.txt");
$lines = $utils->writeOutput($slideArray);

$utils->WriteLines($lines, true);



//var_dump($slides);