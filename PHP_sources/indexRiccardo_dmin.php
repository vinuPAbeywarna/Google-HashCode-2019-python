<?php
/**
 * Created by PhpStorm.
 * User: Riccardo
 * Date: 28/02/2019
 * Time: 18:41
 */
include 'file_utils.class.php';
include 'Slide.php';

ini_set('memory_limit','512M');

//$file = new FileUtils('a_example.txt');
//$file = new FileUtils('b_lovely_landscapes.txt');
//$file = new FileUtils('c_memorable_moments.txt');
$file = new FileUtils('d_pet_pictures.min.txt');
//$file = new FileUtils('e_shiny_selfies.txt');

$fileOut = new FileUtils('out_d_min.txt');

$slides = array();
$lines_verticali = array();

$lines = $file->ReadLines();

$lines_count = count($lines) - 1;
for ($i = 0; $i < $lines_count; $i++) {
    $params = explode(' ', $lines[$i]);

    $photo_type = $params[0];
    unset($params[1]);
    unset($params[0]);

    //$params[count($params)-1] = trim( $params[count($params)-1]);

    // Alessandro
    $tags = array();
    foreach ($params as $_tag)
        $tags[] = trim($_tag);

    if ($photo_type == 'H') {
        array_push($slides, new Slide($i, $tags));
    } else {
        array_push($lines_verticali, array($i, $tags));
    }
}

accoppiaFotoVerticaliSuccessive($lines_verticali, $slides);

$slideshow = creaSlideshow($slides);
$lines = $fileOut->writeOutput($slideshow);
$fileOut->WriteLines($lines, true);

//echo '<br></br>SLIDESHOW<br/>';
//stampaLista($slideshow);

//stampaLista($slides);
function stampaLista($slides)
{
    foreach ($slides as $slide) {
        print_r($slide);
        echo '<br/>';
    }
}