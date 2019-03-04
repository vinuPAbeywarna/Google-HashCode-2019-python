<?php
/**
 * Created by PhpStorm.
 * User: alessandro
 * Date: 2019-02-28
 * Time: 19:25
 */




class SlideshowCreation
{


    private $tagSlide1;
    private $tagSlide2;

    public function calcolaScoreTransizione(Slide $slide1, Slide $slide2)
    {

        $this->tagSlide1 = $slide1->tags;
        $this->tagSlide2 = $slide2->tags;

        //var_dump($this->tagSlide1);
        //var_dump($this->tagSlide2);


        $commonTag = $this->getCommonTags();
        if ($commonTag == 0) return 0;
        $notUsedIn1 = $this->getNotUsedIn1();
        if ($notUsedIn1 == 0) return 0;
        $notUsedIn2 = $this->getNotUsedIn2();
        if ($notUsedIn2 == 0) return 0;

        $scoreTransizione = min($commonTag, $notUsedIn1, $notUsedIn2);
/*
        echo "<br>tag in comune = $commonTag<br>";
        echo "non usati in slide 1 = $notUsedIn1<br>";

        echo "non usati in slide 2 = $notUsedIn2<br>";

        echo "punteggio transizione = $scoreTransizione";
*/

        return $scoreTransizione;
    }

    private function getCommonTags()
    {

        return count(array_intersect($this->tagSlide1, $this->tagSlide2));

    }

    private function getNotUsedIn1()
    {
        //echo __METHOD__."<br>";
        $diff2_1 = array_diff($this->tagSlide2, $this->tagSlide1);
        $score = count($diff2_1);

        return $score;
        //var_dump($diff2_1);
    }

    private function getNotUsedIn2()
    {
        //echo __METHOD__."<br>";
        $diff1_2 = array_diff($this->tagSlide1, $this->tagSlide2);
        $score = count($diff1_2);
        return $score;

        //var_dump($diff1_2);
    }
}