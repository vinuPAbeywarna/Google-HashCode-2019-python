<?php

//ini_set('memory_limit', '256M');

class FileUtils{
	
	public $fileName;
	
	public function __construct($fileName)
	{
		$this->fileName = $fileName;
	}

	public function ReadContent()
	{
		$file = fopen($this->fileName, "r") or exit("Cannot open file");
		
		$line = file_get_contents($this->fileName);
		return $line;
	}

	public function ReadLines()
	{
		$file = fopen($this->fileName, "r") or exit("Cannot open file");
		$lines = array();
		
		while(!feof($file)){
			$lines[] = fgets($file);
		}
		
		fclose($file);
		return $lines;
	}

	public function ReadMatrix($separator)
	{
		$file = fopen($this->fileName, "r") or exit("Cannot open file");
		$matrix = array();

		while(!feof($file)){
			$row = fgets($file);
			$matrix[] = explode($separator, $row);
		}
		
		return $matrix;
	}
	
	public function ReadMatrixArray($separator)
	{
		return $this->ReadMatrix($separator);
	}

	public function ReadBytes()
	{
		$file = fopen($this->fileName, "r") or exit("Cannot open file");
		
		$bytes = unpack("N*",file_get_contents($this->fileName));
		
		return $bytes;
	}

	//public function ReadBytesStream($offset = 0, $count = 2048)	{ }

	public function WriteLines($lines, $append = false)
	{
		$flag = $append ? FILE_APPEND : null;
		
		foreach($lines as $line){
			file_put_contents($this->fileName, $line . "\n", $flag);
		}

		return true;
	}


	public function writeOutput($slideArray) {

        $lines = array();

        $lines[] = count($slideArray);

	    foreach ($slideArray as $item) {

            $id1 = $item->id1;
            $slideLine = (string) $id1;

            if ($item->id2 !== null) {
                $slideLine .= " ".$item->id2;
            }

            $lines[] = $slideLine;
        }

	    return $lines;

    }

/*
	public function WriteBytes(byte[] bytes)
	{
		try
		{
			File.WriteAllBytes($this->fileName, bytes);
		}
		catch (Exception)
		{
			return false;
		}

		return true;
	}
*/
}