<template>
    <div id="chart" />
</template>

<script>
// import libraries
import ApexCharts from 'apexcharts';

// import VUEX
import { createNamespacedHelpers } from 'vuex';

// Movie API
import MovieAPI from '../../../api/movie/movieApi';

import axios from 'axios';

const userMapState = createNamespacedHelpers('users').mapState;
const infoMapState = createNamespacedHelpers('infos').mapState;

// Variables
var chart;

export default {
    data() {
        return {
            ratings: []
        };
    },
    computed: {
        ...userMapState(['user']),
        ...infoMapState(['genres'])
    },
    mounted() {
        // normal : '#FFDD63'
        // max : '#FFA136'
        // let colors = [];
        if (this.user === null) {
            this.getUserBySession(this.token);
        }
        this.test();
        let options = {
            chart: {
                height: 350,
                type: 'bar',
                events: {
                    click: (ch, w, e) => {
                        this.$log.debug('RatingNumberGraph.vue', ch, w, e);
                    }
                }
            },
            colors: [],
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
                data: [21, 22, 10, 28, 16, 21, 13, 30]
            }],
            xaxis: {
                categories: ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
                labels: {
                    style: {
                        colors: [],
                        fontSize: '14px'
                    }
                }
            }
        };
        chart = new ApexCharts(
            document.querySelector('#chart'),
            options
        );

        chart.render();
    },
    methods: {
        test() {
            // console.log('USER ;, this.user);
            // console.log(typeof(this.user));
            axios.get(`/api/movies/pref/`, {
                params: {
                    email: this.user.email
                }
            }).then((ret) => {
                console.log(ret);
            });
            console.log(this.user.email)
        }
    }
};
</script>
