<?php


namespace App\Controllers\Graph;
use App\Controllers\Service\CountryService;
use App\Controllers\Service\Views;


class Graph extends BaseController
{
    /**
     * @var Views
     */
    private $countryService;

    public function __construct()
    {
        $this->countryService = new CountryService();
    }

    public function milestone2Search()
    {

        $searchKey = "Ukraine does not exist";

        $apiURL = 'https://call_backend_analyse';
        $client = \Config\Services::curlrequest();
        $postData = array(
            'statement' => $searchKey
        );
        $response = $client->post($apiURL, ['json' => $postData]);
        $body = $response->getBody();

        $data = json_decode($body, true);

        $all_countries_colors = [];
        $channels = [];

        $all_results = $data["all_results"];

        $existingResults = [];
        $allResultsFiltered = [];
        foreach ($all_results as $result) {
            if (!in_array($result['intra_id'], $existingResults))
            {
                $allResultsFiltered[] = $result;
                $existingResults[] = $result['intra_id'];
            }
        }

        foreach ($allResultsFiltered as &$result){
            $result['colors'] = [];
            $result['countries'] = [];
            if ($result['location']!= '') {
                foreach ($result['location'] as $loc) {
                    $country = $this->countryService->getCountryByName($loc);
                    $result['colors'][] = $country['color'];
                    $result['countries'][] = $country;
                }
            }
            if($result['selected'] == 0)
            {
                continue;
            }
            if ($result['channel']!= '') {
                foreach ($result['channel'] as $ch) {

                    if (isset($channels[$ch])) {
                        $channels[$ch] = $channels[$ch] + 1;
                    } else {
                        $channels[$ch] = 1;
                    }
                }
            }

            if ($result['location']!= '') {
                foreach ($result['location'] as $loc) {
                    $country = $this->countryService->getCountryByName($loc);
                    if (isset($all_countries_colors[$loc])) {
                        $all_countries_colors[$loc]['counter']++;
                        $all_countries_colors[$loc]['narratives'][] = $result["statement"];
                    } else {
                        $all_countries_colors[$loc] = $country;
                        $all_countries_colors[$loc]['counter'] = 1;
                        $all_countries_colors[$loc]['narratives'] = [$result["statement"]];
                    }
                }
            }
        }
        $data['all_results'] = $allResultsFiltered;
        $data['all_results_original'] = $all_results;

        $data['data'] = $data;
        $data['all_countries_colors'] = $all_countries_colors;
        arsort($channels);
        //array_reverse($channels);
        $data['channels'] = $channels;
        // Handle the response as needed
        if ($response) {
            echo view('graph/milestone2/header2');
            echo view('graph/milestone2/graphView3', $data);
            echo view('graph/milestone2/footer');

        } else {
            // Error
            echo $this->curl->error_string;
        }
    }

    public function milestone2()
    {
        echo view('graph/milestone2/searchPage2');
    }

}