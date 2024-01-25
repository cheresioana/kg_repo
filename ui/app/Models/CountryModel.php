<?php

namespace App\Models;

use CodeIgniter\Model;

class CountryModel extends Model
{
    protected $table = 'country';
    protected $allowedFields = [];

    public function getAllCountries(): array
    {
        $this->select();
        return $this->get()->getResultArray();
    }

    public function getCountryByName($countryID)
    {
        $this->select();
        $this->like('name', "%$countryID%");
        return $this->get()->getRowArray();
    }
}
