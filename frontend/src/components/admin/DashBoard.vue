<template>
    <div>
        <v-row class="mb-6">
            <v-col>
                <Line />
            </v-col>
            <v-col>
                <div id="chart2" />
            </v-col>
            <v-col>
                <div id="chart" />
            </v-col>
        </v-row>
    </div>
</template>

<script>
import ApexCharts from 'apexcharts';
import Line from './lineChart.vue';

let chart;
let chart2;
let basicChart;

export default {
    components: {
        Line
    },
    mounted() {
        const options = {
            chart: {
                type: 'donut',
            },
            series: [44, 55, 41, 17, 15],
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 200,
                    },
                    legend: {
                        position: 'bottom',
                    },
                },
            }],
        };

        chart = new ApexCharts(
            document.querySelector('#chart'),
            options,
        );

        chart.render();

        const options2 = {
            chart: {
                type: 'pie',
            },
            series: [44, 55, 41, 17, 15],
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 200,
                    },
                    legend: {
                        position: 'bottom',
                    },
                },
            }],
        };

        chart2 = new ApexCharts(
            document.querySelector('#chart2'),
            options2,
        );

        chart2.render();
    },
};
</script>
