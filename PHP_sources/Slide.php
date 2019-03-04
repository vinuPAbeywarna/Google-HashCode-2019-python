<?php
/**
 * Created by PhpStorm.
 * User: Riccardo
 * Date: 28/02/2019
 * Time: 19:05
 */

include 'SlideshowCreation.php';
class Slide
{
    public $id1;
    public $id2;
    public $tags = array();

    public function __construct($id1, $tags1, $id2 = null, $tags2 = null)
    {
        $this->id1 = $id1;

        if ($id2 != null) {
            $this->id2 = $id2;
            $this->tags = array_merge($tags1, $tags2);
        } else {
            $this->tags = $tags1;
        }
    }
}

function creaSlideshow($slides)
{
    $posizione_migliore = 0;
    $result = array();
    array_push($result, $slides[0]);

    //trovaMiglioreSlide($result[count($result) - 1], $slides);
    //return;

    do {
        $c = count($slides);
        unset($slides[$posizione_migliore]);

        // Cerco la migliore corrispondenza con l'ultimo elemento della slideshow di uscita
        $posizione_migliore = trovaMiglioreSlide($result[count($result) - 1], $slides);

        if ($posizione_migliore != null){
            //echo '<br/>POSIZIONE MIGLIORE: ';
            //print_r($posizione_migliore);
            array_push($result, $slides[$posizione_migliore]);
        }
        //else break;

    } while ($c > 1);

    return $result;
}

function trovaMiglioreSlide(Slide $slide_orig, $slides)
{
    //echo '<br/>TROVAMIGLIORE DI:';
    //print_r($slide_orig);


    $best_array_position = -1;  // Posizione dell'elemento migliore nell'array slides passato
    $best_points = -1;
    //$slides_count = count($slides);

    //for ($i = 0; $i < $slides_count; $i++) {
    foreach ($slides as $i => $slide){
        $transition = new SlideshowCreation();
        //print_r($slide);

        $points = $transition->calcolaScoreTransizione($slide_orig, $slide);

        //echo "<br/>POINTS:$points";

        //if ($points > $best_points || $points == 2) {
		if ($points == 1) {
            $best_points = $points;
            $best_array_position = $i;
        }
    }

    if ($best_array_position == -1)
        return null;

    return $best_array_position;
}

// $lines_verticali[id, tags[]]
function accoppiaFotoVerticaliSuccessive($lines_verticali, &$slides)
{
    $c = count($lines_verticali);
    for ($i = 0; $i < $c; $i += 2) {
        array_push($slides,
            new Slide(
                $lines_verticali[$i][0],
                $lines_verticali[$i][1],
                $lines_verticali[$i + 1][0],
                $lines_verticali[$i + 1][1]
            ));
    }
}


function accoppiaFotoVerticaliAlgoritmo1($lines_verticali, &$slides)
{
    $c = count($lines_verticali);
    for ($i = 0; $i < $c; $i += 2) {

    }
}