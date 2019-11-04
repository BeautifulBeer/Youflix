<template>
    <div class="progressDiv">
        <div class="statChartHolder">
            <div class="progress-pie-chart" data-percent="67"><!--Pie Chart -->
                <div class="ppc-progress">
                    <div class="ppc-progress-fill"></div>
                </div>
                <div class="ppc-percents">
                    <div class="pcc-percents-wrapper">
                        <span>%</span>
                    </div>
                </div>
            </div><!--End Chart -->
        </div>
        <div class="statRightHolder">
            <ul>
                <li> <h3>39.4k</h3> <span>Interactions</span></li>
                <li> <h3>1.8k</h3> <span>Posts</span></li>
            </ul>   
            <ul class="statsLeft">
                <li><h3>22%</h3> <span>Comments</span></li>
                <li><h3>37%</h3> <span>Cheers</span></li>
            </ul>
            <ul class="statsRight">
                <li><h3>18%</h3> <span>Tasks</span></li>
                <li><h3>23%</h3> <span>Goals</span></li>
            </ul>
        </div>
    </div>
</template>

<script>
import $ from 'jquery';

export default {
    mounted() {
        const $ppc = $('.progress-pie-chart');
        const percent = parseInt($ppc.data('percent'), 10);
        const deg = (360 * percent) / 100;
        if (percent > 50) {
            $ppc.addClass('gt-50');
        }
        $('.ppc-progress-fill').css('transform', `rotate('${deg}'deg)`);
        $('.ppc-percents span').html(`${percent}%`);
    }
};
</script>

<style lang="scss" scoped>

@import url(https://fonts.googleapis.com/css?family=Lato:300,400,700);

.progressDiv {
width: 84%;
background: #fcfcfc;
height: 325px;
border: 1px solid #ccc;
position: relative;
left: 7%;
top: 100px;
display: inline-block;
border-radius: 2px;
box-shadow: 0px 1px 1px 1px #ccc;
}

.statChartHolder {
width: 35%;
height: 90%;
position: relative;
border-right: 1px solid #ccc;
top: 15px;
    display: inline-block;
}

.statRightHolder {
display: inline-block;
height: 90%;
width: 64%;
position: relative;
top: -32px;
margin: 0;
}
.statRightHolder ul {
list-style: none;
    margin: 0;
}
.statRightHolder li {
border-bottom: 1px solid #ccc;
height: 85px;
width: 95%;
position: relative;
top: -25px;
}
.statRightHolder h3 {
display: inline-block;
margin-right: 15px;
color: #B6B5B5;
font-weight: 300;
font-size: 38px;
}
.statRightHolder span {
display: inline-block;
color: #B6B5B5;
font-size: 21px;
font-weight: 300;
}

.statsLeft {
    list-style:none;
    display:inline-block;
    width:45%;
}
.statsLeft li {
width: 100%;
height: 14px;
border: none;
top: 5px;
margin-bottom: 25px;
}
.statsLeft h3{
    font-size:17px;
    display: inline-block;
}
.statsLeft span{
    font-size: 17px;
    display:inline-block;
}
.statsRight {
width: 45%;
display: inline-block;
position: absolute;
}
.statsRight li {
width: 100%;
height: 14px;
border: none;
top: 5px;
margin-bottom: 25px;
}
.statsRight h3{
    font-size:17px;
    display: inline-block;
}
.statsRight span{
    font-size: 17px;
    display:inline-block;
}
/* Pie Chart */
.progress-pie-chart {
  width:200px;
  height: 200px;
  border-radius: 50%;
  background-color: #E5E5E5;
  position: relative;
}
.progress-pie-chart.gt-50 {
  background-color: #81CE97;
}

.ppc-progress {
  content: "";
  position: absolute;
  border-radius: 50%;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 200px;
  height: 200px;
  clip: rect(0, 200px, 200px, 100px);
}
.ppc-progress .ppc-progress-fill {
  content: "";
  position: absolute;
  border-radius: 50%;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 200px;
  height: 200px;
  clip: rect(0, 100px, 200px, 0);
  background: #81CE97;
  transform: rotate(60deg);
}
.gt-50 .ppc-progress {
  clip: rect(0, 100px, 200px, 0);
}
.gt-50 .ppc-progress .ppc-progress-fill {
  clip: rect(0, 200px, 200px, 100px);
  background: #E5E5E5;
}

.ppc-percents {
  content: "";
  position: absolute;
  border-radius: 50%;
  left: calc(50% - 173.91304px/2);
  top: calc(50% - 173.91304px/2);
  width: 173.91304px;
  height: 173.91304px;
  background: #fff;
  text-align: center;
  display: table;
}
.ppc-percents span {
  display: block;
  font-size: 2.6em;
  font-weight: bold;
  color: #81CE97;
}

.pcc-percents-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.progress-pie-chart {
  margin: 50px auto 0;
}

@media(max-width: 720px){
  
  .progressDiv{
    height: auto;
  }
  .statChartHolder{
    width: 100%;
    display: block;
    padding-bottom: 65px;
    border-right: none;
    border-bottom: 1px solid #ccc
    
  }
  .statRightHolder {
    display: block;
    height: auto;
    width: 100%;
    position: relative;
    padding-top: 65px;
    margin-bottom: 100px;
}
}
</style>
