<style>
    .selected-statement{
        border: 1px solid var(--bs-primary);
        color: var(--bs-primary);
        background: #E9F3FE;
        cursor: url('<?=base_url()?>/public/layout/font-awesome/minus_sign.png'), pointer;

    }

    .unselected-statement{
        border: 1px solid var(--bs-dark);
        background-color: transparent;
        color: var(--bs-dark);
        cursor: url('<?=base_url()?>/public/layout/font-awesome/plus-sign.png'), pointer;

    }

    .selected-statement > div{
        color: var(--bs-text-primary)!important;
    }

    .unselected-statement > div{
        color: var(--bs-text-gray-600)!important;
    }
</style>
<body id="kt_app_body" style="background: #474747" data-kt-app-header-fixed="true" data-kt-app-header-fixed-mobile="true" data-kt-app-sidebar-enabled="true"
      data-kt-app-sidebar-fixed="true" data-kt-app-sidebar-hoverable="true" data-kt-app-sidebar-push-toolbar="true" data-kt-app-sidebar-push-footer="true" data-kt-app-aside-enabled="true" data-kt-app-aside-fixed="true" data-kt-app-aside-push-toolbar="true"
      data-kt-app-aside-push-footer="true" class="app-default"
      data-kt-app-page-loading-enabled="true" data-kt-app-page-loading="on">

<!--begin::Page loading(append to body)-->
<div class="page-loader">
		<span class="spinner-border text-primary" role="status">
			<span class="visually-hidden">Loading...</span>
		</span>
</div>
<!--end::Page loading-->

<div id="kt_app_header" class="app-header d-flex flex-column flex-stack" style="height: 70px">
    <!--begin::Header main-->
    <div class="d-flex flex-stack flex-grow-1" >
        <!--begin::Navbar-->
        <div class="app-navbar flex-grow-1 justify-content-end" id="kt_app_header_navbar">
            <div class="app-navbar-item d-flex align-items-stretch flex-lg-grow-1">
                <!--begin::Search-->
                <div id="kt_header_search" class="header-search d-flex align-items-center w-100 ms-12 pe-15" data-kt-search-keypress="true" data-kt-search-min-length="2" data-kt-search-enter="enter" data-kt-search-layout="menu" data-kt-search-responsive="true" data-kt-menu-trigger="auto" data-kt-menu-permanent="true" data-kt-menu-placement="bottom-start">
                    <!--begin::Tablet and mobile search toggle-->
                    <div data-kt-search-element="toggle" class="search-toggle-mobile d-flex d-lg-none align-items-center">
                        <div class="d-flex">
                            <i class="ki-outline ki-magnifier fs-1 fs-1"></i>
                        </div>
                    </div>
                    <!--end::Tablet and mobile search toggle-->
                    <!--begin::Form(use d-none d-lg-block classes for responsive search)-->
                    <form data-kt-search-element="form" class="d-none d-lg-block w-100 position-relative mb-5 mb-lg-0" autocomplete="off"
                          action="<?=base_url('graph/graph/new_view')?>" method="get" id="searchForm">
                        <!--begin::Hidden input(Added to disable form autocomplete)-->
                        <input type="hidden" />
                        <!--end::Hidden input-->
                        <!--begin::Icon-->
                        <i class="ki-outline ki-magnifier search-icon fs-2 text-gray-500 position-absolute top-50 translate-middle-y ms-5"></i>
                        <!--end::Icon-->
                        <!--begin::Input-->
                        <input type="text" id="searchInput" class="search-input form-control form-control border h-lg-45px ps-13" name="search" value="<?=$origin[0]["statement"]?>" placeholder="Search..." data-kt-search-element="input" />
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
                    <div data-kt-search-element="content" class="menu menu-sub menu-sub-dropdown py-7 px-7 overflow-hidden w-300px w-md-350px">
                        <!--begin::Wrapper-->
                        <div data-kt-search-element="wrapper">
                            <!--begin::Recently viewed-->
                            <div class="" data-kt-search-element="main">
                                <!--begin::Items-->
                                <div class="scroll-y mh-200px mh-lg-325px">
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
    <!--end::Header main-->
</div>
<div class="app-wrapper flex-column flex-row-fluid" id="kt_app_wrapper" style="margin-right: 0px; margin-left: 0px; margin-top: 60px">
    <div class="d-flex flex-column flex-root app-root" id="kt_app_root">
    <div id="kt_app_content" class="app-content flex-column-fluid">
        <!--begin::Content container-->
        <div id="kt_app_content_container" class="app-container container-fluid">
    <!--begin::Page-->
            <div class="app-page flex-column flex-column-fluid" id="kt_app_page">
                <div class="row g-5 g-xl-6 mb-5">
                    <div class="col-xl-4 mb-5">
                    <!--begin::Chart Widget 35-->
                        <div class="card card-flush  h-md-50">
                    <!--begin::Header-->
                            <div class="card-header pt-5">
                                <!--begin::Title-->
                                <h3 class="card-title align-items-start flex-column">
                                    <!--begin::Statistics-->
                                    <div class="d-flex align-items-center mb-2">
                                        <span class="card-label fw-bold text-gray-900">Related Statements</span>
                                    </div>
                                    <!--end::Statistics-->
                                    <!--begin::Description-->
                                    <span class="fs-5 fw-semibold text-gray-600">Add or remove from analysis</span>
                                    <!--end::Description-->
                                </h3>
                                <div class="card-toolbar">
                                </div>
                            </div>
                    <!--end::Header-->
                        <!--begin::Body-->
                                <div class="card-body py-4 px-8">
                                    <div class="hover-scroll-overlay-y pe-6 me-n6" style="height: 200px">
                                        <div class="mt-2">
                                            <!--begin::Item-->
                                            <?php
                                            foreach ($all_results as $element):
                                                if ($element['selected'] == 1):
                                                    ?>
                                                    <div class="d-flex flex-stack align-items-start mt-3">
                                                        <!--begin::Section-->
                                                        <div class="d-flex align-items-left me-5">
                                                    <span class="badge badge-outline selected-statement" id="statement-span-<?=$element['intra_id']?>" >
                                                        <!--begin::Symbol-->

                                                        <a href="<?=$element['url']?>" class="symbol-label me-1" style="cursor: context-menu;" target="_blank">
                                                             <i class="bi bi-file-text-fill me-2" style="font-size: 1.5em"></i>
                                                        </a>

                                                        <div class="fw-bold fs-6 text-start" style="max-width: 100%; white-space: normal;"
                                                             onclick="toggleStatementSelection('<?=$element['intra_id']?>')">
                                                            <?= $element['statement'] ?>
                                                            <i class="bi bi-check-lg text-primary"></i>
                                                        </div>
                                                    </span>
                                                </div>
                                            </div>
                                            <?php else:
                                            ?>
                                                <div class="align-items-start mt-3">
                                                    <!--begin::Section-->
                                                    <div class="align-items-left me-5">
                                                    <span class="badge badge-outline unselected-statement" id="statement-span-<?=$element['intra_id']?>" >
                                                        <!--begin::Symbol-->
                                                        <a href="<?=$element['url']?>" class="symbol-label me-1" target="_blank">
                                                            <i class="bi bi-file-text-fill me-2" style="font-size: 1.5em; cursor: context-menu;"></i>
                                                        </a>
                                                        <div class="fw-bold fs-6 text-start" style="max-width: 100%; white-space: normal;"
                                                             onclick="toggleStatementSelection(<?=$element['intra_id']?>)">
                                                            <?= $element['statement'] ?>
                                                            <i class="bi bi-check-lg text-primary d-none"></i>
                                                        </div>
                                                    </span>
                                                    </div>
                                                </div>
                                            <?php endif; endforeach;?>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="card card-flush h-md-40 mt-5  mb-5">
                                <!--begin::Header-->
                                <div class="card-header flex-nowrap pt-3" style="min-height: 30px">
                                    <!--begin::Title-->
                                    <h3 class="card-title align-items-start flex-column">
                                        <span class="card-label fw-bold text-gray-800">Countries</span>
                                        <span class="text-gray-500 mt-1 fw-semibold fs-6">How many times this narrative appeared</span>
                                    </h3>

                                    <!--end::Title-->
                                </div>
                                <!--end::Header-->
                                <!--begin::Body-->
                                <div class="card-body pt-0 ps-1 pe-1">
                                    <div id="kt_countries_chart" style="height: 200px"></div>
                                </div>
                                <!--end::Body-->
                            </div>

                        <!--end::Body-->
                    </div>
                    <div class="col-xl-8 mb-5">
                        <!--begin::Maps widget 1-->
                        <div class="card card-flush h-md-100 pb-50" >
                            <!--begin::Header-->
                            <div class="card-header pt-7">
                                <h3 class="d-flex align-items-center mb-2 w-100">
                                    <span class="card-label fw-bold text-gray-900">Spread</span>
                                </h3>
                                <!--end::Statistics-->
                                <!--begin::Description-->
                                <span class="fs-5 fw-semibold text-gray-600">Countries where the fake news appeared</span>
                                <!--end::Description-->
                            </div>
                            <!--end::Header-->
                            <!--begin::Body-->
                            <div class="card-body d-flex flex-center p-3 pb-0 pt-0">
                                <!--begin::Map container-->
                                <div id="spread_map" class="w-100 h-450px"></div>
                                <!--end::Map container-->
                            </div>
                            <!--end::Body-->
                        </div>
                    </div>
                </div>
                <div class="row g-5 g-xl-6 ">
                    <div class="col-xl-4" style="margin-top: 5px;">
                    <!--begin::Table Widget 4-->
                        <div class="card card-flush h-xl-100" style="min-height: 300px; max-height: 400px">
                        <!--begin::Card header-->
                        <div class="card-header pt-5">
                            <!--begin::Title-->
                            <h3 class="card-title align-items-start flex-column">
                                <span class="card-label fw-bold text-gray-800">Channels</span>
                                <span class="text-gray-500 mt-1 fw-semibold fs-6">On what websites the information was disseminated</span>
                            </h3>
                            <!--end::Title-->
                        </div>
                        <!--end::Card header-->
                        <!--begin::Card body-->
                        <div class="card-body pt-2" style="max-height: 400px; overflow: scroll">
                            <!--begin::Table-->
                            <table class="table align-middle table-row-dashed fs-6 gy-3" id="kt_table_widget_4_table">
                                <!--begin::Table head-->
                                <thead>
                                <!--begin::Table row-->
                                <tr class="text-start text-gray-700 fw-bold fs-7 text-uppercase gs-0">

                                    <th class="min-w-100px fw-bold">Website name</th>
                                    <th class="text-center fw-bold min-w-100px">No. of appearances</th>
                                </tr>
                                <!--end::Table row-->
                                </thead>
                                <!--end::Table head-->
                                <!--begin::Table body-->
                                <tbody class=" text-gray-600" id="channelsTableBody">

                                <?php $index=1; foreach ($channels as $key => $value): ?>
                                <tr>
                                    <td class="text-start"><?php echo $index. '.'. $key ?></td>
                                    <td class="text-center"><?php echo $value; ?></td>
                                </tr>
                                    <?php $index = $index + 1; ?>
                                <?php endforeach; ?>
                                </tbody>
                                <!--end::Table body-->
                            </table>
                            <!--end::Table-->
                        </div>
                        <!--end::Card body-->
                    </div>
                    </div>
                    <!--end::Table Widget 4-->
                    <div class="col-xl-8" style="margin-top: 5px">
                        <!--begin::Timeline Widget 4-->
                        <div class="card h-md-100" style="min-height: 300px; max-height: 400px">
                            <!--begin::Card header-->
                            <div class="card-header pt-5 pb-5">
                                <!--begin::Title-->
                                <h3 class="card-title align-items-start flex-column">
                                    <span class="card-label fw-bold text-gray-800">Timeline</span>
                                    <span class="text-gray-500 mt-1 fw-semibold fs-6">How the information spread over time.</span>
                                </h3>

                            </div>
                            <!--end::Card header-->
                            <!--begin::Card body-->
                            <div class="card-body p-0">
                                <!--begin::Tab content-->
                                <div class="tab-content">
                                    <!--begin::Tab pane-->
                                    <div class="tab-pane active" id="kt_timeline_widget_4_tab_2022" role="tabpanel" aria-labelledby="week-tab" data-kt-timeline-widget-4-blockui="true">
                                        <div class="table-responsive pb-0">
                                            <!--begin::Timeline-->
                                            <div id="kt_timeline_widget_4_4c" class="vis-timeline-c2"></div>
                                            <!--end::Timeline-->
                                        </div>
                                    </div>
                                    <!--end::Tab pane-->
                                </div>
                                <!--end::Tab content-->
                            </div>
                            <!--end::Card body-->
                        </div>
                        <!--end::Timeline Widget 1-->

                    </div>
                </div>
                <div class="row g-5 g-xl-6 mt-1">
                    <div style="justify-content-center">
                        <div id="3d-graph" style="margin: auto"></div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</div>
</div>

</body>

<!-- select/unselect statement -->
<script>
    var newCounter = []; // Pentru a număra aparițiile fiecărei țări
    var newCountryName = [];
    var newColors = [];

    function updateCountriesChart(intraID) {
        newCounter = [];
        newCountryName = [];
        newColors = [];

        all_results.forEach(item => {
            if (item.intra_id == intraID) {
                item.selected = item.selected === 1 ? 0 : 1;

            }

            if (item.selected === 1) {
                if(item.location === "")
                {
                    return
                }
                item.location.forEach(loc =>
                {
                    let index = newCountryName.indexOf(loc);
                    if(index === -1)
                    {
                        newCounter.push(1);
                        newCountryName.push(loc);
                        newColors.push(item.colors[item.location.indexOf(loc)]);
                    }
                    else
                    {
                        newCounter[index]++;
                    }
                })
            }
        });
        window.KTChartsWidget5.update(newCounter, newCountryName, newColors);
    }

    function updateMapChart(newData) {
        // Iterate through the newData and create new polygon series
        let newColorData = {};
        all_results.forEach(item => {
            if (item.selected === 1) {
                if (item.location === "") {
                    return
                }
                item.countries.forEach(loc => {
                    var countryId = loc.name;
                    if (newColorData[countryId]) {
                        newColorData[countryId].counter += 1;
                        newColorData[countryId].narratives.push(item.statement)
                    } else {
                        newColorData[countryId] = {
                            country_id: loc.country_id,
                            name: loc.name,
                            color: loc.color,
                            id: loc.id,
                            counter: 1,
                            narratives: [item.statement]
                        };
                    }
                });
            }
        });
        colorData = newColorData;
        colorData2 = Object.values(newColorData);

        root.dispose();
        loadMap(colorData2);

    }

    function updateChannelsTable() {
        console.log(all_results)
        selectedChannels = {};
        all_results.forEach(item => {
            if (item.selected === 0) {
                return
            }
            if(item.channel !== "")
            {
                item.channel.forEach(ch => {
                    if(selectedChannels[ch]){
                        selectedChannels[ch]++;
                    }
                    else
                    {
                        selectedChannels[ch] = 1;
                    }
                });
            }
        })
        let tbody = $('#channelsTableBody');
        tbody.empty();
        $.each(selectedChannels, function(channel, count) {
            var row = $('<tr>');
            row.append($('<td>').addClass('text-start').text(channel));
            row.append($('<td>').addClass('text-center').text(count));
            tbody.append(row);
        });

    }

    function toggleStatementSelection(intraID) {
        let statementSpan = $('#statement-span-' + intraID);

        if (statementSpan.hasClass('selected-statement')) {
            // Dacă statement-ul este selectat, îl dezactivăm
            statementSpan.removeClass('selected-statement').addClass('unselected-statement');
            statementSpan.find('i.bi-check-lg').addClass('d-none');
            removeStatement(intraID)
        } else {
            // Dacă statement-ul nu este selectat, îl activăm
            statementSpan.removeClass('unselected-statement').addClass('selected-statement');
            statementSpan.find('i.bi-check-lg').removeClass('d-none');
            addStatement(intraID)
        }
        updateCountriesChart(intraID); // aici se face update la selected in all results
        updateMapChart();
        window.updateTimelineData();
        updateChannelsTable();

    }
</script>
<!-- END select/unselect statement -->

<script src="//unpkg.com/three"></script>
<script src="//unpkg.com/d3"></script>
<script src="<?=base_url()?>/public/layout/graph/js/3d-force-graph.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
<script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
<script type="importmap">{ "imports": { "three": "https://unpkg.com/three/build/three.module.js" }}</script>
<script type="module"></script>
<script src="//unpkg.com/three-spritetext"></script>


<!--Timeline-->
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"></script>
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/custom/vis-timeline/vis-timeline.bundle.js"></script>
<script>
    var colorData = <?php echo json_encode($all_countries_colors)?>;
    var colorData2 = Object.values(colorData)
    var all_results = <?php echo json_encode($all_results)?>;
    var all_data = <?php echo json_encode($data)?>;
    console.log("ALL DATA")
    console.log(all_data)
    console.log("COLOR DATA")
    console.log(colorData)
</script>
<script type="module" src="<?=base_url()?>/public/layout/graph/js/new_ui.js"></script>

<!-- Countries map chart dependencies-->
<script src="<?=base_url()?>/public/layout/graph/metronic_demo39/assets/plugins/global/plugins.bundle.js"></script>
<!-- End Countries map chart dependencies -->
<!-- Countries bar chart -->
<script>
    var counters = <?php $arr = [];
    foreach($all_countries_colors as $element)
        $arr[]= $element['counter'];
    echo json_encode($arr);
    ?>;

    var categories = <?php $arr = [];
    foreach($all_countries_colors as $element)
        $arr[]= $element['name'];
    echo json_encode($arr);
    ?>;

    var colors = <?php $arr = [];
    foreach($all_countries_colors as $element)
        $arr[]= $element['color'];
    echo json_encode($arr);
    ?>;

</script>

<script type="module">

    "use strict";

    // Class definition

    var KTChartsWidget5 = function () {
        var chart = {
            self: null,
            rendered: false
        };

        var updateChart = function(newCounters, newCategories, newColors) {
            if (chart.self) {
                chart.self.updateOptions({
                    series: [{
                        data: newCounters
                    }],
                    xaxis: {
                        categories: newCategories
                    },
                    colors: newColors
                });
            }
        };

        // Private methods
        var initChart = function(chart) {
            var element = document.getElementById("kt_countries_chart");

            if (!element) {
                return;
            }

            var borderColor = KTUtil.getCssVariableValue('--bs-border-dashed-color');
            console.log(counters)
            console.log(categories)
            console.log(colors)
            var options = {
                series: [{
                    data: counters,
                    show: false
                }],
                chart: {
                    type: 'bar',
                    height: 200,
                    toolbar: {
                        show: false
                    }
                },
                plotOptions: {
                    bar: {
                        borderRadius: 4,
                        horizontal: true,
                        distributed: true,
                        barHeight: 15
                    }
                },
                dataLabels: {
                    enabled: false
                },
                legend: {
                    show: false
                },
                colors: colors,
                xaxis: {
                    categories: categories,
                    labels: {
                        style: {
                            colors: KTUtil.getCssVariableValue('--bs-gray-400'),
                            fontSize: '12px',
                            fontWeight: '600',
                            align: 'left'
                        }
                    },

                    axisBorder: {
                        show: false
                    }
                },
                yaxis: {
                    labels: {
                        style: {
                            colors: KTUtil.getCssVariableValue('--bs-gray-800'),
                            fontSize: '14px',
                            fontWeight: '600'
                        },
                        offsetY: 2,
                        align: 'left'
                    }
                },
                grid: {
                    borderColor: borderColor,
                    xaxis: {
                        lines: {
                            show: true
                        }
                    },
                    yaxis: {
                        lines: {
                            show: false
                        }
                    },
                    strokeDashArray: 4,
                    padding: { left: 10, right: 15, top: -15, bottom: -15 },
                }
            };

            chart.self = new ApexCharts(element, options);

            // Set timeout to properly get the parent elements width
            setTimeout(function() {
                chart.self.render();
                chart.rendered = true;
            }, 200);
        }

        // Public methods
        return {
            init: function () {
                initChart(chart);

                // Update chart on theme mode change
                KTThemeMode.on("kt.thememode.change", function() {
                    if (chart.rendered) {
                        chart.self.destroy();
                    }

                    initChart(chart);
                });
            },
            update: updateChart // Expose the update function
        }
    }();

    // Webpack support
    if (typeof module !== 'undefined') {
        module.exports = KTChartsWidget5;
    }

    //On document ready
    // KTUtil.onDOMContentLoaded(function() {
    //     KTChartsWidget5.init();
    // });
    window.KTChartsWidget5 = KTChartsWidget5;
    export { KTChartsWidget5 };
</script>
<!-- End Countries bar chart -->


<!--Map Chart dependencies-->
<script src="https://cdn.amcharts.com/lib/5/index.js"></script>
<script src="https://cdn.amcharts.com/lib/5/map.js"></script>
<script src="https://cdn.amcharts.com/lib/5/geodata/worldLow.js"></script>
<script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>
<!--End Map Chart dependencies-->

<!--Map Chart-->
<script>
    var root;
    var colorData = <?php echo json_encode($all_countries_colors)?>;
    var colorData2 = Object.values(colorData)

    am5.ready(loadMap())
    function loadMap() {

// Create root and chart
        root = am5.Root.new("spread_map");
        //root.interpolationDuration = 0;
// Set themes
        root.setThemes([
           am5themes_Animated.new(root)
        ]);



// Create chart
        var chart = root.container.children.push(am5map.MapChart.new(root, {
            homeZoomLevel: 3.5,
            homeGeoPoint: { longitude: 10, latitude: 52 }
        }));


// Create world polygon series
        var worldSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
            geoJSON: am5geodata_worldLow,
            exclude: ["AQ"]
        }));

        worldSeries.mapPolygons.template.setAll({
            fill: am5.color(0xaaaaaa)
        });

        worldSeries.events.on("datavalidated", () => {
            chart.goHome();
        });


        var colors = am5.ColorSet.new(root, {
            step: 2
        });
        colors.next();

        // var countriesToColor = [
        //     { "id": "RU", "joined": ["Ukraine does not exist, it is a Polish fake", "Ukraine is a failed state which will soon cease to exist",
        //             "Ukraine does not exist, it is part of Russia", "Ukraine does not exist as a state, it is a colony of the US Democratic Party"]},
        //     { "id": "DE", "joined": ["Ukraine is not a sovereign country and it should stay that way"]},
        //     { "id": "LT", "joined": ["Ukraine was created from parts of Russia"]},
        // ]
        //
        console.log("INTRA IN REFRESH")
        am5.array.each(colorData2, function(countryGroup) {
            color = am5.color(countryGroup.color)
            var countries = []
            countries.push(countryGroup.country_id)
            var polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
                geoJSON: am5geodata_worldLow,
                include: countries,
                narrative: countryGroup.narratives.join('\n'),
                fill: color
            }));


            polygonSeries.mapPolygons.template.setAll({
                tooltipText: "[bold]{name}[/]\n{narrative}",
                interactive: true,
                fill: color,
                strokeWidth: 2
            });

            polygonSeries.mapPolygons.template.states.create("hover", {
                fill: am5.Color.brighten(color, -0.3)
            });

            polygonSeries.mapPolygons.template.events.on("pointerover", function(ev) {
                ev.target.series.mapPolygons.each(function(polygon) {
                    polygon.states.applyAnimate("hover");
                });
            });

            polygonSeries.mapPolygons.template.events.on("pointerout", function(ev) {
                ev.target.series.mapPolygons.each(function(polygon) {
                    polygon.states.applyAnimate("default");
                });
            });
        });
    } // end am5.ready()
</script>
<!--End Map Chart-->

<!-- START WITH #D FORCE GRAPH-->



<script type="module">
    import { CSS2DRenderer, CSS2DObject } from '//unpkg.com/three/examples/jsm/renderers/CSS2DRenderer.js';
    // Random tree
    // const N = 300;
    // const gData = {
    //     nodes: [...Array(N).keys()].map(i => ({ id: i })),
    //     links: [...Array(N).keys()]
    //         .filter(id => id)
    //         .map(id => ({
    //             source: id,
    //             target: Math.round(Math.random() * (id-1))
    //         }))
    // };
    //
    // var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    // console.log("Screen width: " + screenWidth + " pixels");
    //
    //
    // const Graph = ForceGraph3D()
    // (document.getElementById('3d-graph'))
    //     .graphData(gData)
    //     .height(800)
    //     .width(parseInt(0.96 * screenWidth))
    //     .style('margin:auto');


    function updateGraphAnalyze(data){
        var origin_node = data['origin'][0]
        var my_data2 = {}
        my_data2["nodes"]= data["nodes"]
        my_data2["links"] = data['links']

        var zoom_node = null
        var Graph = ForceGraph3D({
            extraRenderers: [new CSS2DRenderer()]
        })

        (document.getElementById('3d-graph'))
            .graphData(my_data2)
            .dagMode('td')
            .dagLevelDistance(40)
            //.nodeAutoColorBy('tag')
            .nodeLabel('statement')
            .nodeThreeObject(node => {

                const nodeEl = document.createElement('div');
                nodeEl.style.color = '#b3eae7';
                nodeEl.color = '#67f5ef';
                nodeEl.style.opacity = 1;
                nodeEl.style.fontsize= "48px"

                nodeEl.renderOrder = 1;
                nodeEl.textContent = node.statement
                nodeEl.className = 'statement_node';
                nodeEl.style.color = node.color;

                if (node.intra_id === origin_node.intra_id){

                    nodeEl.style.color = 'rgb(121,64,60)'

                }
                else if (node.tag=== 'key_element'){
                    nodeEl.style.color = 'rgb(238,199,109)'

                }
                else {
                    nodeEl.style.color = 'rgb(90,151,162)'

                }

                return new CSS2DObject(nodeEl);

                // const sprite = new SpriteText(node.statement);
                // sprite.material.depthWrite = false;
                // sprite.color = 'lightsteelblue';
                //
                // if (node.id === origin_node){
                //   sprite.color = '#D09541'
                //     addInfoCard(node)
                // }
                // else if (node.tag=== 'key_element'){
                //    sprite.color = "#F3F3F3"
                //
                // }
                // else {
                //     sprite.color = "#4C70AC"
                //     //nodeEl.style.opacity = 0.45;
                //     addInfoCard(node)
                //
                // }
                // sprite.textHeight = 6;
                // return sprite;
                //
                // return new CSS2DObject(nodeEl);
            })
            .nodeColor(node=>{
                if (node.id === origin_node){

                    return 'rgb(206,86,66)'

                }
                else if (node.tag=== 'key_element'){
                    return 'rgb(238,199,109)'

                }
                else {
                    return 'rgb(90,151,162)'

                }
            })
            .onNodeDragEnd(node => {
                node.fx = node.x;
                node.fy = node.y;
                node.fz = node.z;
            })
            .linkWidth(1)
            .height(700)
            // .onNodeClick(node => click_node(node))
            .cooldownTicks(10)
            // .linkDirectionalParticles("value")
            // .linkDirectionalParticleSpeed(d =>  d.value * 0.001)
            .nodeThreeObjectExtend(true)
        var k = 0
        Graph.d3Force('charge').strength(-250);
        Graph.onEngineStop(() => {
            if (k === 0) {
                k = 1
                Graph.zoomToFit(250)
                Graph.cameraPosition(
                    { x:0, y:100, z: 200 },  // new position
                    { x: 0, y: 0, z: 0 },  // look-at position
                    1000  // transition duration
                );
            }

        });


    }
    updateGraphAnalyze(all_data)
    window.updateGraphAnalyze = updateGraphAnalyze;
</script>
<script src="<?=base_url()?>/public/layout/graph/js/requests2.js"></script>

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
