<!DOCTYPE html>
<html>

<head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests" />

    <title>Mindbugs | Knowledge graph</title>

    <link href="<?=base_url()?>/public/layout/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="<?=base_url()?>/public/layout/font-awesome/css/font-awesome.css" rel="stylesheet">
    <!--    <link href="--><?php //=base_url()?><!--/public/layout/graph/css/animate.css" rel="stylesheet">-->
    <link href="<?=base_url()?>/public/layout/graph/css/style_b.css" rel="stylesheet">
    <link href="<?=base_url()?>/public/layout/graph/css/style.css" rel="stylesheet">
    <link href="<?=base_url()?>/public/layout/graph/css/graph_style.css" rel="stylesheet">



    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter:300,400,500,600,700" />
    <!--end::Fonts-->
    <!--begin::Vendor Stylesheets(used for this page only)-->
    <link href="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/custom/fullcalendar/fullcalendar.bundle.css" rel="stylesheet" type="text/css" />
    <link href="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/custom/datatables/datatables.bundle.css" rel="stylesheet" type="text/css" />
    <!--end::Vendor Stylesheets-->
    <!--begin::Global Stylesheets Bundle(mandatory for all pages)-->
    <link href="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/global/plugins.bundle.css" rel="stylesheet" type="text/css" />
    <link href="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/css/style.bundle.css" rel="stylesheet" type="text/css" />
    <!--end::Global Stylesheets Bundle-->
    <link href="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/custom/datatables/datatables.bundle.css" rel="stylesheet" type="text/css" />
    <link href="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/custom/vis-timeline/vis-timeline.bundle.css" rel="stylesheet" type="text/css" />

    <style>
        .float{
            position:fixed;
            width:60px;
            height:60px;
            bottom:40px;
            right:40px;
            background-color:#0C9;
            color:#FFF;
            border-radius:50px;
            text-align:center;
            box-shadow: 2px 2px 3px #999;
        }

        .float-filter{
            right:120px
        }

        .my-float{
            margin-top:22px;
            justify-content: center;
            display: flex;
        }

        .centered {
            position: fixed;
            /*display: flex;*/
            top: 15%;
            left: 50%;
            width: 80%;
            opacity: 1;
            /* bring your own prefixes */
            transform: translate(-50%);
            z-index: 9999;
            background-color: rgba(0,0,0,0.75);
            padding: 15px;
            border-radius: 40px;
            padding-bottom: 40px;
            padding-top: 40px;
            width: 60%;
        }

        .w-68{
            width: 68%;
        }
    </style>
</head>

<body class="gray-bg" style="background-color: #000011!important;">



    <div id="whatever" style="background-color: #0a0c0d">
        <div id="3d-graph" style="float: right!important;z-index: 1;">
        </div>

    </div>

    <div class="justify-content-center centered">
        <div class="w-100">
            <img src="<?=base_url()?>/public/layout/logo/LOGOALB_mare_MBDisc_inline.png" style="height: 60px; display: block; margin: auto; opacity: 1;">
        </div>
        <div class="w-100">
            <h1 class="text-center pt-5" style="color: white ">Explore fake news statistics</h1>
        </div>

        <!--begin::Header main-->
        <div class="d-flex flex-row">
            <div class="d-flex flex-stack flex-grow-1 " >

            <!--begin::Navbar-->
            <div class="app-navbar flex-grow-1 justify-content-end" id="kt_app_header_navbar">
                <div class="app-navbar-item d-flex align-items-stretch flex-lg-grow-1">
                    <!--begin::Search-->
                    <div id="kt_header_search" style="margin: auto; margin-top: 10px; width: 70%" class="header-search d-flex align-items-center pt-5"  data-kt-search-keypress="true" data-kt-search-min-length="2" data-kt-search-enter="enter" data-kt-search-layout="menu" data-kt-search-responsive="true" data-kt-menu-trigger="auto" data-kt-menu-permanent="true" data-kt-menu-placement="bottom-start">
                        <!--begin::Tablet and mobile search toggle-->
                        <div data-kt-search-element="toggle" class="search-toggle-mobile d-flex d-lg-none align-items-center">
                            <div class="d-flex">
                                <i class="ki-outline ki-magnifier fs-1 fs-1"></i>
                            </div>
                        </div>
                        <!--end::Tablet and mobile search toggle-->
                        <!--begin::Form(use d-none d-lg-block classes for responsive search)-->
                        <form data-kt-search-element="form" class="d-none d-lg-block w-100 position-relative mb-5 mb-lg-0" autocomplete="off"
                              action="<?=base_url('graph/graph/milestone2Search')?>" method="get" id="searchForm">
                            <!--begin::Hidden input(Added to disable form autocomplete)-->
                            <input type="hidden" />
                            <!--end::Hidden input-->
                            <!--begin::Icon-->
                            <i class="ki-outline ki-magnifier search-icon fs-2 text-gray-500 position-absolute top-50 translate-middle-y ms-5"></i>
                            <!--end::Icon-->
                            <!--begin::Input-->
                            <input type="text" class="search-input form-control form-control border h-lg-45px ps-13" name="search" value="" placeholder="Search..." data-kt-search-element="input" id="searchInput"/>
                            <!--end::Input-->
                            <!--begin::Spinner-->
                            <span class="search-spinner position-absolute top-50 end-0 translate-middle-y lh-0 d-none me-5" data-kt-search-element="spinner">
                                                <span class="spinner-border h-15px w-15px align-middle text-gray-500"></span>
                                            </span>
                            <!--end::Spinner-->
                            <!--begin::Reset-->
                            <span class="search-reset btn btn-flush btn-active-color-primary position-absolute top-50 end-0 translate-middle-y lh-0 d-none me-4" data-kt-search-element="clear">
                                                <i class="ki-outline ki-cross fs-2 fs-lg-1 me-0"></i>
                                            </span>
                            <!--end::Reset-->
                        </form>
                        <!--end::Form-->
                        <!--begin::Search Options-->
                        <div data-kt-search-element="content" class="menu menu-sub menu-sub-dropdown py-7 px-7 w-68 overflow-hidden" >
                            <!--begin::Wrapper-->
                            <div data-kt-search-element="wrapper">
                                <!--begin::Recently viewed-->
                                <div class="" data-kt-search-element="main">
                                    <!--begin::Items-->
                                    <div class="scroll-y mh-200px mh-lg-325px">
                                        <!--begin::Item-->
                                        <div class="d-flex align-items-center mb-5">
                                                <a onclick="completeSearch('Ukraine does not exist')" class="w-100 fs-6 text-gray-800 text-hover-primary fw-semibold">Ukraine does not exist</a>
                                        </div>
                                        <!--end::Item-->
                                        <!--begin::Item-->
                                        <div class="d-flex align-items-center mb-5">
                                            <!--begin::Title-->
                                            <a onclick="completeSearch('EU is anti Russia')" class="w-100 fs-6 text-gray-800 text-hover-primary fw-semibold">EU is anti Russia</a>
                                            <!--end::Title-->
                                        </div>
                                        <!--end::Item-->
                                        <!--begin::Item-->
                                        <div class="d-flex align-items-center mb-5">
                                            <a onclick="completeSearch('Klaus Iohannis')" class="w-100 fs-6 text-gray-800 text-hover-primary fw-semibold">Klaus Iohannis</a>
                                        </div>
                                        <!--end::Item-->
                                        <!--begin::Item-->
                                        <div class="d-flex align-items-center mb-5">
                                            <!--begin::Title-->
                                            <a onclick="completeSearch('USA is evil')" class="w-100 fs-6 text-gray-800 text-hover-primary fw-semibold">USA is evil</a>
                                            <!--end::Title-->
                                        </div>
                                        <!--end::Item-->
                                    </div>
                                    <!--end::Items-->
                                </div>
                                <!--end::Recently viewed-->
                            </div>
                            <!--end::Wrapper-->
                        </div>
                        <!--end::Search Options-->
                    </div>
                    <!--end::Search-->
                </div>

            </div>
            <!--end::Navbar-->
        </div>
        </div>
    </div>


    <div class="page-loader flex-column bg-dark bg-opacity-25">
        <span class="spinner-border text-primary" role="status"></span>
        <span class="text-gray-800 fs-6 fw-semibold mt-5">Loading...</span>
    </div>

</body>
<script>var hostUrl = "assets/";</script>
<!--begin::Global Javascript Bundle(mandatory for all pages)-->
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/global/plugins.bundle.js"></script>
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/js/scripts.bundle.js"></script>
<!--end::Global Javascript Bundle-->
<!--begin::Vendors Javascript(used for this page only)-->
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/custom/fullcalendar/fullcalendar.bundle.js"></script>
<script src="https://cdn.amcharts.com/lib/5/index.js"></script>
<script src="https://cdn.amcharts.com/lib/5/xy.js"></script>
<script src="https://cdn.amcharts.com/lib/5/percent.js"></script>
<script src="https://cdn.amcharts.com/lib/5/radar.js"></script>
<script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>
<script src="https://cdn.amcharts.com/lib/5/map.js"></script>
<script src="https://cdn.amcharts.com/lib/5/geodata/worldLow.js"></script>
<script src="https://cdn.amcharts.com/lib/5/geodata/continentsLow.js"></script>
<script src="https://cdn.amcharts.com/lib/5/geodata/usaLow.js"></script>
<script src="https://cdn.amcharts.com/lib/5/geodata/worldTimeZonesLow.js"></script>
<script src="https://cdn.amcharts.com/lib/5/geodata/worldTimeZoneAreasLow.js"></script>
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/custom/datatables/datatables.bundle.js"></script>
<!--end::Vendors Javascript-->
<!--begin::Custom Javascript(used for this page only)-->
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/js/widgets.bundle.js"></script>
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/js/custom/widgets.js"></script>
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/js/custom/apps/chat/chat.js"></script>
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/js/custom/utilities/modals/upgrade-plan.js"></script>
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/js/custom/utilities/modals/users-search.js"></script>

<!--begin::Vendors Javascript(used for this page only)-->
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/custom/datatables/datatables.bundle.js"></script>

<script src="//unpkg.com/three"></script>
<script src="//unpkg.com/d3"></script>
<script src="<?=base_url()?>/public/layout/graph/js/3d-force-graph.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
<script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
<script type="importmap">{ "imports": { "three": "https://unpkg.com/three/build/three.module.js" }}</script>
<script type="module"></script>

<script src="//unpkg.com/three-spritetext"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js"></script>

<script type="module" src="<?=base_url()?>/public/layout/graph/js/init_big_graph.js"></script>
<!--<script src="--><?php //=base_url()?><!--/public/layout/graph/js/global_variables.js"></script>-->
<!--<script src="--><?php //=base_url()?><!--/public/layout/graph/js/filter_graph.js"></script>-->
<!--<script src="--><?php //=base_url()?><!--/public/layout/graph/js/details_pannel_utils.js"></script>-->
<!--<script type="module" src="--><?php //=base_url()?><!--/public/layout/graph/js/init_graph.js"></script>-->
<!--<script src="--><?php //=base_url()?><!--/public/layout/graph/js/graph.js"></script>-->

<script>
    function completeSearch(searchKey)
    {
        searchInput = $('#searchInput');
        searchForm = $('#searchForm');

        const loadingEl = document.createElement("div");
        document.body.prepend(loadingEl);
        loadingEl.classList.add("page-loader");
        loadingEl.classList.add("flex-column");
        loadingEl.classList.add("bg-dark");
        loadingEl.classList.add("bg-opacity-25");
        loadingEl.innerHTML = `
        <span class="spinner-border text-primary" role="status"></span>
        <span class="text-gray-800 fs-6 fw-semibold mt-5">Loading...</span>
    `;

        // Show page loading
        KTApp.showPageLoading();
        searchInput.val(searchKey);
        searchForm.submit();


    }

</script>


</html>