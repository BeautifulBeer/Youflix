<template>
    <v-container
        v-if="!isLoaded"
        fluid
        class="loading-container"
    >
        <v-row
            style="height: 100%; position: relative;"
            justify="center"
            align="center"
        >
            <div class="logo">
                <div class="netflix">
                    <span style="height: 35%;" />
                    <span />
                    <span />
                </div>
                <h3 class="heading">
                    LOADING
                </h3>
            </div>
        </v-row>
    </v-container>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapState } = createNamespacedHelpers('movies');

export default {
    computed: {
        ...mapState(['isLoaded'])
    },
    watch: {
        // eslint-disable-next-line
        isLoaded: function(val) {
            this.$log.debug('Loading.vue isLoaded watch', val);
            if (val) {
                setTimeout(() => {
                    this.enableScroll();
                }, 500);
            } else {
                window.scrollTo(0, 0);
            }
            this.disableScroll();
        }
    },
    methods: {
        disableScroll() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
            window.onscroll = () => {
                window.scrollTo(scrollLeft, scrollTop);
            };
        },
        enableScroll() {
            window.onscroll = () => {};
        }
    }
};
</script>

<style lang="scss" scoped>

.loading-container {
    position: absolute;
    background-color: rgba(0, 0, 0);
    width: 100vw;
    height: 100vh;
    z-index: 200;
}

.netflix{
  position: relative;
  width: 360px;
  height: 510px;
  overflow: hidden;
  transform: scale(.7);
}

.netflix:before{
  content: '';
  position: absolute;
  bottom: -100px;
  z-index: 2;
  width: 100%;
  height: 120px;
  background: #000;
  border-top-left-radius: 100%;
  border-top-right-radius: 100%;
  transform: scaleX(1.5);
}
.netflix:after, .heading:before{
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 200%;
  height: 100%;
  background: linear-gradient(to right, transparent, #000, #000);
  z-index:3;
  animation: animate 2s linear alternate;
  animation-iteration-count:infinite;
}
@keyframes animate{
  0%{
    right: 0;
  }
  100%{
    right: -200%;
  }
}

.netflix span{
  position: absolute;
  top: 0;
  width: 120px;
  height: 50%;
  background: #fff;
}

.netflix span:nth-child(1){
  background: #b00612;
  left: 50%;
  top: 50%;
  transform: translateX(-60px);
  z-index: 2;
/*   box-shadow: 0 0 20px rgba(0, 0, 0, 1); */
}

.netflix span:nth-child(2){
  background: #b00612;
  left: 0;
  transform-origin: top left;
  transform: skewX(24.8deg);
  box-shadow: 0 0 20px rgba(0, 0, 0, 1);
}

.netflix span:nth-child(3){
  background: #b00612;
  right: 60px;
  transform: skewX(155.2deg);
  box-shadow: 0 0 20px rgba(0, 0, 0, 1);
}

.heading{
  color: #fff;
  text-transform: uppercase;
  position: relative;
  top: -100px;
  margin: 0;
  padding: 0;
  text-align: center;
  font-family: arial;
  font-size: 45px;
  letter-spacing: 10px;
}

.logo{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
}
</style>
