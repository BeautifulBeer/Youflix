<template>
    <div>
        <v-row class="mb-6">
            <v-col>
                <div id="chart2" />
            </v-col>
            <v-col>
                <div id="chart" />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <BasicLine/>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <ContinuousChart/>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import ApexCharts from 'apexcharts';
import BasicLine from './lineChart.vue';
import ContinuousChart from './testChart.vue';

let chart;
let chart2;
let BasicChart;
let BaseChart;

export default {
    components: {
        BasicLine,
        ContinuousChart,
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
