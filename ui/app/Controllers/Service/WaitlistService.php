<?php

namespace App\Controllers\Service;

use App\Models\WaitlistModel;

class WaitlistService
{
    /**
     * @var WaitlistModel
     */
    private $waitlistModel;

    public function __construct()
    {
        $this->waitlistModel = new WaitlistModel();
    }

    public function registerWaitlist(string $email)
    {
        $this->waitlistModel->registerNewEmail($email);
    }
}
