<?php

namespace App\Controllers;

use App\Controllers\Service\Views;

class Blog extends BaseController
{
    /**
     * @var Views
     */
    private $viewService;

    public function __construct()
    {
        $this->viewService = new Views();
    }

    public function index()
    {
        $this->viewService->viewPage('blogs');

        echo view('header');
        echo view('blogs');
        echo view('footer');
    }

    /// $blogName o sa fie numele blogului si numele view-ului pentru fiecare blog
    public function viewBlog($blogName)
    {
        $this->viewService->viewPage($blogName);

        echo view('header');
        echo view('blogs/' . $blogName);
        echo view('footer');
    }

    public function increaseDownloadNumber($downloadName)
    {
        $this->viewService->viewPage($downloadName);
    }
}