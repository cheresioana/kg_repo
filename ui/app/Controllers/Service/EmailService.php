<?php

namespace App\Controllers\Service;

class EmailService
{
    public function sendEmailNewWaitList($userOnWaitlist)
    {
        $email = \Config\Services::email();
        $email->setFrom('contact@techwave.ro', 'Mindbugs Discovery');
        $email->setTo('mike.topor@yahoo.com');
        $email->setSubject('New user on waitlist MBDiscovery');
        $email->setMessage("New user on waitlist email: $userOnWaitlist");

        $email->send();
    }

    public function sendEmail(string $destEmail, string $message, $subject)
    {
        $email = \Config\Services::email();
        $email->setFrom('contact@techwave.ro', 'Contact Techwave @ MindBugs');
        $email->setTo($destEmail);
        $email->setSubject($subject);
        $email->setMessage($message);

        $email->send();
    }

}