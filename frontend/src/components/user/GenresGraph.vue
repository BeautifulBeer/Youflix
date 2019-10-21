<template>
    <div id="chart3" />
</template>

<script>
import ApexCharts from 'apexcharts';

let chart3;

export default {
    name: 'GenresGraph',
    mounted() {
        const options = {
            chart: {
                height: 350,
                type: 'bar',
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        position: 'top' // top, center, bottom
                    }
                }
            },
            dataLabels: {
                enabled: true,
                formatter(val) {
                    return `${val}%`;
                },
                offsetY: -20,
                style: {
                    fontSize: '12px',
                    colors: ['#304758']
                }
            },
            series: [
                {
                    name: 'Inflation',
                    data: [2.3, 3.1, 4.0, 10.1, 4.0, 3.6, 3.2, 2.3, 1.4, 0.8, 0.5, 0.2]
                }
            ],
            xaxis: {
                categories: [
                    'Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'
                ],
                position: 'top',
                labels: {
                    offsetY: -18
                },
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false
                },
                crosshairs: {
                    fill: {
                        type: 'gradient',
                        gradient: {
                            colorFrom: '#D8E3F0',
                            colorTo: '#BED1E6',
                            stops: [0, 100],
                            opacityFrom: 0.4,
                            opacityTo: 0.5
                        }
                    }
                },
                tooltip: {
                    enabled: true,
                    offsetY: -35
                }
            },
            fill: {
                gradient: {
                    shade: 'light',
                    type: 'horizontal',
                    shadeIntensity: 0.25,
                    gradientToColors: undefined,
                    inverseColors: true,
                    opacityFrom: 1,
                    opacityTo: 1,
                    stops: [50, 0, 100, 100]
                }
            },
            yaxis: {
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false
                },
                labels: {
                    show: false,
                    formatter(val) {
                        return `${val}%`;
                    }
                }
            },
            title: {
                text: 'Monthly Inflation in Argentina, 2002',
                floating: true,
                offsetY: 320,
                align: 'center',
                style: {
                    color: '#444'
                }
            }
        };
        chart3 = new ApexCharts(document.querySelector('#chart3'), options);
        chart3.render();
    }
};
</script>

<style scoped>

#chart3{
    height: 600px;
}

</style>
