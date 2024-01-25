<?php

namespace App\Models;

use CodeIgniter\Model;

class WaitlistModel extends Model
{
    protected $table = 'waiting_list';
    protected $allowedFields = [];


    public function registerNewEmail(string $email)
    {
        $this->set('email', $email);
        $this->insert();
    }
}