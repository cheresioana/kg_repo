<?php

namespace App\Controllers;

use App\Controllers\Service\EmailService;
use App\Controllers\Service\Views;
use App\Controllers\Service\WaitlistService;
use Config\Email;

class Home extends BaseController
{
    /**
     * @var WaitlistService
     */
    private $waitlistService;

    /**
     * @var EmailService
     */
    private $emailService;

    /**
     * @var Views
     */
    private $viewService;

    public function __construct()
    {
        $this->waitlistService = new WaitlistService();
        $this->viewService = new Views();
        $this->emailService = new EmailService();
    }

    public function index()
    {
        $this->viewService->viewPage('homePage');

        $data = [];
        if($this->session->getFlashdata('error'))
        {
            $data['error'] = $this->session->getFlashdata('error');
        }
        if($this->session->getFlashdata('success'))
        {
            $data['success'] = $this->session->getFlashdata('success');
        }

        echo view('home', $data);
        echo view('footer');
    }

    public function joinWaitlist()
    {
        $p = $_POST;
        helper(['form']);
        $rules = [
            'email' => 'required|min_length[4]|max_length[255]|valid_email|trim',
        ];
        if($this->validate($rules)) {
            $this->waitlistService->registerWaitlist($p['email']);
            $this->emailService->sendEmailNewWaitList($p['email']);
            $this->session->setFlashdata('success', '✅ Successfully added to the waiting list! Stay tuned for updates.');
        }
        else
        {
            $this->session->setFlashdata('error', 'Required fields are not completed! Please try again.');
        }
        return redirect()->back();
    }

}
