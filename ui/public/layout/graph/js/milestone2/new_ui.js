

"use strict";
// Class definition
var KTTimelineWidget4 = function () {
    // Private methods

    // 2022 timeline
    const initTimeline2022 = () => {
        // Detect element
        const element = document.querySelector('#kt_timeline_widget_4_4c');
        if (!element) {
            return;
        }

        if(element.innerHTML){
            return;
        }

        // Set variables
        var now = Date.now();

        // Build vis-timeline datasets
        var groups = new vis.DataSet([
            {
                id: "Russia",
                content: "Russia",
                order: 1,
                color: '#333DA8',
            },
            {
                id: "Lithuania",
                content: "Lithuania",
                order: 2,
                color: '#DC67CE',
            },
            {
                id: "Germany",
                content: "Germany",
                order: 3,
                color: '#A467DC',
            },

        ]);
        console.log(moment("07.07.2021", "DD.MM.YYYY").year())
        console.log(moment("07.07.2021", "DD.MM.YYYY").month())
        console.log(moment("07.07.2021", "DD.MM.YYYY").day())

        const date = '07.07.2021';
        const formattedDate = moment(date, 'DD.MM.YYYY').format('YYYY-MM-DD');

        console.log(formattedDate); // This will print "2021-07-07"

        var items = new vis.DataSet([
            {
                id: 1,
                group: 'Russia',
                start: moment("27.05.2023", "DD.MM.YYYY"),
                content: "Ukraine is a Soviet invention",
                //color: 'primary',
                color: '#333DA8',
            },
            {
                id: 11,
                group: 'Russia',
                start: moment("07.07.2021", "DD.MM.YYYY"),
                content: "Ukraine does not exist, it is part of Russia",
                //color: 'primary',
                color: '#333DA8',
            },
            {
                id: 12,
                group: 'Russia',
                start: moment("01.03.2021", "DD.MM.YYYY"),
                content: "Ukraine does not exist, it is a Polish fake",

                color: '#333DA8',
            },
            {
                id: 13,
                group: 'Russia',
                start: moment("26.06.2020", "DD.MM.YYYY"),
                content: "Ukraine does not exist as a state, it is a colony of the US Democratic Party",
                color: '#333DA8',
            },
            {
                id: 14,
                group: 'Lithuania',
                start: moment("10.04.2023", "DD.MM.YYYY"),
                content: "Ukraine was created from parts of Russia",
                color: '#DC67CE',
            },
            {
                id: 15,
                group: 'Germany',
                start: moment("30.07.2021", "DD.MM.YYYY"),
                content: "Ukraine is not a sovereign country and it should stay that way",
                color: '#A467DC',
            }
        ]);

        // Set vis-timeline options
        var options = {
            zoomable: false,
            moveable: true,
            selectable: false,
            // More options https://visjs.github.io/vis-timeline/docs/timeline/#Configuration_Options
            margin: {
                item: {
                    horizontal: 10,
                    vertical: 2
                }
            },

            // Remove current time line --- more info: https://visjs.github.io/vis-timeline/docs/timeline/#Configuration_Options
            showCurrentTime: false,
            showTooltips: true,
            verticalScroll: true,
            maxHeight:"400px",

            // Whitelist specified tags and attributes from template --- more info: https://visjs.github.io/vis-timeline/docs/timeline/#Configuration_Options
            xss: {
                disabled: false,
                filterOptions: {
                    whiteList: {
                        div: ['class', 'style'],
                        span: ['class']
                    },
                },
            },
            // specify a template for the items
            template: function (item) {
                let userTemplate = '';

                return `<div class="rounded-pill d-flex align-items-center position-relative h-20px w-100 p-2 px-5 overflow-hidden" style="background-color: ${item.color}">

                    <div class="d-flex align-items-center position-relative z-index-2">
                        <span class="fw-bold text-white text-hover-light fs-10px">${item.content}</span>
                    </div>
                </div>
                `;
            },

            groupTemplate: function (item) {
                let userTemplate = '';

                return `<div class="rounded-pill d-flex align-items-center position-relative h-20px w-100 p-2 px-5 overflow-hidden" style="color: ${item.color}">

                    <div class="d-flex align-items-center position-relative z-index-2">
                        <span class="fw-bold fs-10px" >${item.content}</span>
                    </div>
                </div>
                `;
            },

            // Remove block ui on initial draw
            onInitialDrawComplete: function () {

                const target = element.closest('[data-kt-timeline-widget-4-blockui="true"]');
                const blockUI = KTBlockUI.getInstance(target);

                if (blockUI.isBlocked()) {
                    setTimeout(() => {
                        blockUI.release();
                    }, 1000);
                }
            }
        };

        // Init vis-timeline
        const timeline = new vis.Timeline(element, items, groups, options);

        // Prevent infinite loop draws
        timeline.on("currentTimeTick", () => {
            // After fired the first time we un-subscribed
            timeline.off("currentTimeTick");
        });
    }
    // Handle BlockUI
    const handleBlockUI = () => {
        // Select block ui elements
        const elements = document.querySelectorAll('[data-kt-timeline-widget-4-blockui="true"]');

        // Init block ui
        elements.forEach(element => {
            const blockUI = new KTBlockUI(element, {
                overlayClass: "bg-body",
            });

            blockUI.block();
        });
    }
    //initTimeline2022();


    // Public methods
    return {
        init: function () {
            initTimeline2022();
            handleBlockUI();
        }
    }
}();

// Webpack support
if (typeof module !== 'undefined') {
    module.exports = KTTimelineWidget4;
}

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTTimelineWidget4.init();
});
