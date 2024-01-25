<?php

namespace App\Controllers\Service;

use App\Models\CountryModel;

class CountryService
{
    private $countryModel;

    public function __construct()
    {
        $this->countryModel = new CountryModel();
    }

    public function getAllCountries(): array
    {
        return $this->countryModel->getAllCountries();
    }

    public function getCountryByName($countryID)
    {
        return $this->countryModel->getCountryByName($countryID);
    }
}
