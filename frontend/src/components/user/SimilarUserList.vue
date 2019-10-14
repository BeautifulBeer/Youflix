<template>
    <v-card flat>
        <v-card-text>
            <v-container
                fluid
                class="pa-0"
            >
                <v-row>
                    <v-col
                        cols="12"
                        sm="3"
                    >
                        <v-btn
                            text
                            color="pink"
                            @click="createChart('GENDER')"
                        >
                            <v-icon>mdi-gender-transgender</v-icon>GENDER
                        </v-btn>
                    </v-col>

                    <v-col
                        cols="12"
                        sm="3"
                    >
                        <v-btn
                            text
                            color="indigo"
                            @click="createChart('OCCUPATION')"
                        >
                            <v-icon>mdi-worker</v-icon>OCCUPATION
                        </v-btn>
                    </v-col>

                    <v-col
                        cols="12"
                        sm="3"
                    >
                        <v-btn
                            text
                            color="green"
                            @click="createChart('AGE')"
                        >
                            <v-icon>mdi-cake-variant</v-icon>AGE
                        </v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </v-card-text>

        <div id="chart" />
    </v-card>
</template>

<script>
import ApexCharts from 'apexcharts';

let chart;

export default {
    name: 'SimilarUserList',
    props: {
        similarUserList: { type: Array, default: Array },
    },
    data() {
        return {
            chartColor: [],
            chartSeries: [],
            chartLabels: [],

            ageLabels: [
                'Under 18',
                '18-24',
                '25-34',
                '35-44',
                '45-49',
                '50-55',
                '56+',
            ],

            colors: [
                '#F44336',
                '#E91E63',
                '#9C27B0',
                '#673AB7',
                '#3F51B5',
                '#2196F3',
                '#00BCD4',
                '#009688',
                '#4CAF50',
                '#9CCC65',
                '#C0CA33',
                '#FFEB3B',
                '#FFCA28',
                '#FF7043',
                '#795548',
                '#9E9E9E',
                '#607D8B',
                '#212121',
                '#33FFFF',
                '#ECEFF1',
            ],

            occupationList: [
                'other',
                'academic/educator',
                'artist',
                'clerical/admin',
                'college/grad student',
                'customer service',
                'doctor/health care',
                'executive/managerial',
                'farmer',
                'homemaker',
                'K-12 student',
                'lawyer',
                'programmer',
                'retired',
                'sales/marketing',
                'scientist',
                'self-employed',
                'technician/engineer',
                'tradesman/craftsman',
                'unemployed',
                'writer',
            ],
        };
    },
    watch: {

        similarUserList() {
            this.createChart('GENDER');
        },
    },
    methods: {
        classifyData(classification) {
            this.chartColor = [];
            this.chartSeries = [];
            this.chartLabels = [];

            let index = 0;

            if (classification === 'GENDER') {
                let female = 0;
                let male = 0;

                this.chartColor.push('#F44336');
                this.chartColor.push('#2196F3');

                for (let i = 0; i < this.similarUserList.length; i++) {
                    if (this.similarUserList[i].gender === 'M') male++;
                    else female++;
                }
                this.chartSeries.push(female);
                this.chartSeries.push(male);

                this.chartLabels.push('Female');
                this.chartLabels.push('Male');
            } else if (classification === 'AGE') {
                const ageList = {
                    1: 0,
                    18: 0,
                    25: 0,
                    35: 0,
                    45: 0,
                    50: 0,
                    56: 0,
                };

                for (let i = 0; i < 7; i++) this.chartColor.push(this.colors[i]);

                for (let i = 0; i < this.similarUserList.length; i++) ageList[this.similarUserList[i].age]++;

                for (const key in ageList) {
                    if (ageList[key] != 0) {
                        this.chartColor.push(this.colors[index]);
                        this.chartLabels.push(this.ageLabels[index++]);
                        this.chartSeries.push(ageList[key]);
                    }
                }
            } else {
                const occupationList = {

                    other: 0,
                    'academic/educator': 0,
                    artist: 0,
                    'clerical/admin': 0,
                    'college/grad student': 0,
                    'customer service': 0,
                    'doctor/health care': 0,
                    'executive/managerial': 0,
                    farmer: 0,
                    homemaker: 0,
                    'K-12 student': 0,
                    lawyer: 0,
                    programmer: 0,
                    retired: 0,
                    'sales/marketing': 0,
                    scientist: 0,
                    'self-employed': 0,
                    'technician/engineer': 0,
                    'tradesman/craftsman': 0,
                    unemployed: 0,
                    writer: 0,
                };

                for (let i = 0; i < this.similarUserList.length; i++) occupationList[this.similarUserList[i].occupation]++;

                for (const key in occupationList) {
                    if (occupationList[key] != 0) {
                        this.chartColor.push(this.colors[index++]);
                        this.chartLabels.push(key);
                        this.chartSeries.push(occupationList[key]);
                    }
                }
            }
        },

        createChart(classification) {
            if (chart != null) chart.destroy();
            this.classifyData(classification);

            console.log('CHART COLOR> ', this.chartColor);
            console.log('CHART SERIES> ', this.chartSeries);
            console.log('CHART LABLES> ', this.chartLabels);
            console.log('\n');

            const options = {
                chart: {
                    type: 'donut',
                },

                colors: this.chartColor,
                series: this.chartSeries,
                labels: this.chartLabels,
                responsive: [
                    {
                        breakpoint: 480,
                        options: {
                            chart: {
                                width: 200,
                            },
                            legend: {
                                position: 'bottom',
                            },
                        },
                    },
                ],
            };
            chart = new ApexCharts(document.querySelector('#chart'), options);
            chart.render();
        },
    },
};
</script>
