<template>
    <div class="content">
        <div id="chart" />
    </div>
</template>

<script>
// import libraries
import ApexCharts from 'apexcharts';

// import VUEX
import { createNamespacedHelpers } from 'vuex';

const userMapState = createNamespacedHelpers('users').mapState;
const userMapActions = createNamespacedHelpers('users').mapActions;
const movieMapActions = createNamespacedHelpers('movies').mapActions;

// Variables
var chart;

export default {
    data() {
        return {
            ratingDict: {}
        };
    },
    computed: {
        ...userMapState(['user'])
    },
    mounted() {
        if (this.user === null) {
            this.getSession().then(() => {
                this.drawChart();
            });
        } else {
            this.drawChart();
        }
    },
    methods: {
        ...movieMapActions(['getRatingPref']),
        ...userMapActions(['getSession']),
        drawChart() {
            // normal : '#FFDD63'
            // max : '#FFA136'
            // let colors = [];
            this.getRatingPref(this.user.email).then((ret) => {
                const data = [];
                Object.keys(ret.data).sort().forEach((key) => {
                    data.push(ret.data[key]);
                });
                // const options = {
                //     chart: {
                //         height: 350,
                //         type: 'bar'
                //     },
                //     plotOptions: {
                //         bar: {
                //             dataLabels: {
                //                 position: 'center' // top, center, bottom
                //             }
                //         }
                //     },
                //     dataLabels: {
                //         enabled: true,
                //         formatter: (val) => val,
                //         offsetY: -20,
                //         style: {
                //             fontSize: '15px',
                //             colors: ['#E50914']
                //         }
                //     },
                //     series: [{
                //         name: '횟수',
                //         data
                //     }],
                //     xaxis: {
                //         categories: ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
                //         position: 'top',
                //         labels: {
                //             offsetY: -18

                //         },
                //         axisBorder: {
                //             show: false
                //         },
                //         axisTicks: {
                //             show: false
                //         },
                //         crosshairs: {
                //             fill: {
                //                 type: 'gradient',
                //                 gradient: {
                //                     colorFrom: '#D8E3F0',
                //                     colorTo: '#BED1E6',
                //                     stops: [0, 100],
                //                     opacityFrom: 0.4,
                //                     opacityTo: 0.5
                //                 }
                //             }
                //         },
                //         tooltip: {
                //             enabled: true,
                //             offsetY: -35

                //         }
                //     },
                //     fill: {
                //         gradient: {
                //             shade: 'light',
                //             type: 'horizontal',
                //             shadeIntensity: 0.25,
                //             gradientToColors: undefined,
                //             inverseColors: true,
                //             opacityFrom: 1,
                //             opacityTo: 1,
                //             stops: [50, 0, 100, 100]
                //         }
                //     },
                //     yaxis: {
                //         axisBorder: {
                //             show: false
                //         },
                //         axisTicks: {
                //             show: false
                //         },
                //         labels: {
                //             show: false,
                //             formatter: (val) => val
                //         }
                //     }
                // };
                const colors = ['#7dd426', '#26d483', '#09e5cb', '#09a3e5', '#2609e5', '#8609e5', '#e509e1', '#e5099f', '#e5096c', '#E50914'];
                const options = {
                    chart: {
                        height: 350,
                        type: 'bar'
                    },
                    colors,
                    plotOptions: {
                        bar: {
                            columnWidth: '45%',
                            distributed: true
                        }
                    },
                    dataLabels: {
                        enabled: false
                    },
                    series: [{
                        name: '횟수',
                        data
                    }],
                    xaxis: {
                        categories: ['0.5점', '1점', '1.5점', '2점', '2.5점', '3점', '3.5점', '4점', '4.5점', '5점'],
                        labels: {
                            style: {
                                colors,
                                fontSize: '15px'
                            }
                        }
                    }
                }
                chart = new ApexCharts(
                    document.querySelector('#chart'),
                    options
                );
                chart.render();
            });
        }
    }
};
</script>

<style scoped>

.content {
    position: absolute;
    top: 50%;
    transform: translateY(-50%); width: 100%;
}
</style>
