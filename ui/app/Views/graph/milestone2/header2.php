<!DOCTYPE html>
<html data-bs-theme-mode="light">

<head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests" />
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
    <script src="<?=base_url()?>/public/layout/graph/js/3d-force-graph.min.js"></script>

    <script>// Frame-busting to prevent site from being loaded within a frame without permission (click-jacking) if (window.top != window.self) { window.top.location.replace(window.self.location.href); }</script>
<style>
    .vis-timeline-c2 {
        border: 5px solid $vis-border-color !important;


        .vis-labelset {
            .vis-label {
                display: flex;
                align-items: center;
                padding-left: 1rem;
                padding-right: 1rem;
                border-bottom: none;
                font-size: $h4-font-size;
                font-weight: $font-weight-semibold;
                color: var(--#{$prefix}gray-900);
                padding-top: 1rem;
                padding-bottom: 1rem;
            }
        }

        .vis-itemset {
        }

        .vis-foreground {
            .vis-group {
                border-bottom: none;
            }
        }

        .vis-item {
            position: absolute;
            border-color: var(--#{$prefix}primary);
            border-width: 0px;
            background-color: transparent;

            .vis-item-content {
                padding: 0.75rem 1rem;
                width: 100%;
                transform: none !important;
            }
        }

        .vis-time-axis {



            font-size: $font-size-sm;
            text-transform: uppercase;
            font-weight: $font-weight-semibold;

            .vis-text {
                color: var(--#{$prefix}gray-400);
            }

            .vis-grid.vis-minor {
                border-left-color: $vis-border-dashed-color !important;
            }

            .vis-grid.vis-vertical {
                border-left-style: dashed !important;
            }
        }

        .vis-panel {
            .vis-shadow {
                box-shadow: none !important;
            }

        }

        .vis-panel {
            &.vis-bottom,
            &.vis-center,
            &.vis-left,
            &.vis-right,
            &.vis-top {
                border-color: $vis-border-color !important;
            }
        }

    }

    .vis-item-content{
      height: 20px;
    }


</style>

</head>