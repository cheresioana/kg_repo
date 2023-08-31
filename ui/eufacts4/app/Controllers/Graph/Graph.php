<?php


namespace App\Controllers\Graph;
use App\Controllers\Service\Views;


class Graph extends BaseController
{

    public function index(): void
    {
        echo view('graph/graphView');
    }

    public function getFakeNews($id){
        if (($open = fopen(base_url().'/public/assets/datasets/parsed_dataset.csv', "r")) !== FALSE)
        {
            $header = fgetcsv($open, 1000, ",");
            while (($data = fgetcsv($open, 1000, ",")) !== FALSE)
            {
                if (intval($data[0]) == $id) {

                    //To display array data
                    $complete_data = array_combine($header, $data);
                    $json = json_encode($complete_data);
                    return $json;
                }
            }

            fclose($open);
        }


    }

}