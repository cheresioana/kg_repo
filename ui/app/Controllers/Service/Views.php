<?php

namespace App\Controllers\Service;

use App\Models\ViewModel;

class Views
{
    private $viewModel;

    /**
     * @param $viewModel
     */
    public function __construct()
    {
        $this->viewModel = new ViewModel();
    }

    public function viewPage($pageCode)
    {
        $date = date('m-Y');
        $pageCode = $pageCode . '-' . $date;

        if ($this->viewModel->existViewCode($pageCode))
        {
            $this->viewModel->incrementView($pageCode);
        }
        else
        {
            $this->viewModel->createView($pageCode);
        }
    }
}