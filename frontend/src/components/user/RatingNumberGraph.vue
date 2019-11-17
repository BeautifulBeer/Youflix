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
const movieMapMutation = createNamespacedHelpers('movies').mapMutations;

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
            this.getUserBySession(localStorage.getItem('token')).then(() => {
                if (this.user == null) {
                    swal({
                        title: 'Session Timeout',
                        text: 'Session이 만료되었습니다. Login Page로 돌아갑니다.',
                        icon: 'error',
                        button: false
                    }).then(() => {
                        this.$router.push('/login');
                        this.setIsLoaded(true);
                    });
                } else {
                    this.drawChart();
                }
            });
        } else {
                this.drawChart();
        }
    },
    methods: {
        ...movieMapActions(['getRatingPref']),
        ...userMapActions(['getUserBySession']),
        ...movieMapMutation(['setIsLoaded']),
        drawChart() {
            
            this.getRatingPref(this.user.email).then((ret) => {
                const data = [];
                Object.keys(ret.data).sort().forEach((key) => {
                    data.push(ret.data[key]);
                });

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
