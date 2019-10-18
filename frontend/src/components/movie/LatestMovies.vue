<template>
    <div class="demo-cont">
        <!-- slider start -->
        <div class="fnc-slider example-slider">
            <div class="fnc-slider__slides">
                <!-- slide start -->
                <div class="fnc-slide m--blend-green m--active-slide">
                    <div class="fnc-slide__inner">
                        <div class="fnc-slide__mask">
                            <div class="fnc-slide__mask-inner" />
                        </div>
                        <div class="fnc-slide__content">
                            <h2 class="fnc-slide__heading">
                                <div class="fnc-slide__heading-line">
                                    <span>LALA</span>
                                </div>
                                <div class="fnc-slide__heading-line">
                                    <span>LAND</span>
                                </div>
                            </h2>
                        </div>
                    </div>
                </div>
                <!-- slide end -->
                <!-- slide start -->
                <div class="fnc-slide m--blend-dark">
                    <div class="fnc-slide__inner">
                        <div class="fnc-slide__mask">
                            <div class="fnc-slide__mask-inner" />
                        </div>
                        <div class="fnc-slide__content">
                            <h2 class="fnc-slide__heading">
                                <div class="fnc-slide__heading-line">
                                    <span>HARRY</span>
                                </div>
                                <div class="fnc-slide__heading-line">
                                    <span>POTTER</span>
                                </div>
                            </h2>
                        </div>
                    </div>
                </div>
                <!-- slide end -->
                <!-- slide start -->
                <div class="fnc-slide m--blend-red">
                    <div class="fnc-slide__inner">
                        <div class="fnc-slide__mask">
                            <div class="fnc-slide__mask-inner" />
                        </div>
                        <div class="fnc-slide__content">
                            <h2 class="fnc-slide__heading">
                                <div class="fnc-slide__heading-line">
                                    <span>LOBSTER</span>
                                </div>
                            </h2>
                        </div>
                    </div>
                </div>
                <!-- slide end -->
                <!-- slide start -->
                <div class="fnc-slide m--blend-blue">
                    <div class="fnc-slide__inner">
                        <div class="fnc-slide__mask">
                            <div class="fnc-slide__mask-inner" />
                        </div>
                        <div class="fnc-slide__content">
                            <h2 class="fnc-slide__heading">
                                <div class="fnc-slide__heading-line">
                                    <span>INCEPTION</span>
                                </div>
                            </h2>
                        </div>
                    </div>
                </div>
                <!-- slide end -->
            </div>
            <nav class="fnc-nav">
                <div class="fnc-nav__bgs">
                    <div class="fnc-nav__bg m--navbg-green m--active-nav-bg" />
                    <div class="fnc-nav__bg m--navbg-dark" />
                    <div class="fnc-nav__bg m--navbg-red" />
                    <div class="fnc-nav__bg m--navbg-blue" />
                </div>
                <div class="fnc-nav__controls">
                    <button class="fnc-nav__control">
                        {{ movies[0].title }}
                        <span class="fnc-nav__control-progress" />
                    </button>
                    <button class="fnc-nav__control">
                        {{ movies[1].title }}
                        <span class="fnc-nav__control-progress" />
                    </button>
                    <button class="fnc-nav__control">
                        {{ movies[2].title }}
                        <span class="fnc-nav__control-progress" />
                    </button>
                    <button class="fnc-nav__control">
                        {{ movies[3].title }}
                        <span class="fnc-nav__control-progress" />
                    </button>
                </div>
            </nav>
        </div>
    </div>
</template>

<script>
export default {
    name: '',
    data() {
        return {
            movies: [
                {
                    title: 'Lala Land',
                    id: 124234,
                    img: 'img/lalaland_wallpaper.png'
                },
                {
                    title: 'Harry Potter',
                    id: 6534,
                    img: 'img/harry_potter_wallpaper.jfif'
                },
                {
                    title: 'Lobster',
                    id: 123414,
                    img: 'img/lobster_wallpaper.jpg'
                },
                {
                    title: 'Inception',
                    id: 456435,
                    img: 'img/inception_wallpaper.jpg'
                }
            ]
        };
    },
    mounted() {
        this.$nextTick(() => {
          (function () {
            const $$ = function (selector, context) {
                var context = context || document;
                const elements = context.querySelectorAll(selector);
                return [].slice.call(elements);
            };

            function _fncSliderInit($slider, options) {
                const prefix = '.fnc-';

                var $slider = $slider;
                const $slidesCont = $slider.querySelector(`${prefix}slider__slides`);
                const $slides = $$(`${prefix}slide`, $slider);
                const $controls = $$(`${prefix}nav__control`, $slider);
                const $controlsBgs = $$(`${prefix}nav__bg`, $slider);
                const $progressAS = $$(`${prefix}nav__control-progress`, $slider);

                const numOfSlides = $slides.length;
                let curSlide = 1;
                let sliding = false;
                const slidingAT = +parseFloat(getComputedStyle($slidesCont)['transition-duration']) * 1000;
                const slidingDelay = +parseFloat(getComputedStyle($slidesCont)['transition-delay']) * 1000;

                let autoSlidingActive = false;
                let autoSlidingTO;
                const autoSlidingDelay = 5000; // default autosliding delay value
                let autoSlidingBlocked = false;

                let $activeSlide;
                let $activeControlsBg;
                let $prevControl;

                function setIDs() {
                    $slides.forEach(($slide, index) => {
                        $slide.classList.add(`fnc-slide-${index + 1}`);
                    });

                    $controls.forEach(($control, index) => {
                        $control.setAttribute('data-slide', index + 1);
                        $control.classList.add(`fnc-nav__control-${index + 1}`);
                    });

                    $controlsBgs.forEach(($bg, index) => {
                        $bg.classList.add(`fnc-nav__bg-${index + 1}`);
                    });
                }

                setIDs();

                function afterSlidingHandler() {
                    $slider.querySelector('.m--previous-slide').classList.remove('m--active-slide', 'm--previous-slide');
                    $slider.querySelector('.m--previous-nav-bg').classList.remove('m--active-nav-bg', 'm--previous-nav-bg');

                    $activeSlide.classList.remove('m--before-sliding');
                    $activeControlsBg.classList.remove('m--nav-bg-before');
                    $prevControl.classList.remove('m--prev-control');
                    $prevControl.classList.add('m--reset-progress');
                    const triggerLayout = $prevControl.offsetTop;
                    $prevControl.classList.remove('m--reset-progress');

                    sliding = false;
                    const layoutTrigger = $slider.offsetTop;

                    if (autoSlidingActive && !autoSlidingBlocked) {
                        setAutoslidingTO();
                    }
                }

                function performSliding(slideID) {
                    if (sliding) return;
                    sliding = true;
                    window.clearTimeout(autoSlidingTO);
                    curSlide = slideID;

                    $prevControl = $slider.querySelector('.m--active-control');
                    $prevControl.classList.remove('m--active-control');
                    $prevControl.classList.add('m--prev-control');
                    $slider.querySelector(`${prefix}nav__control-${slideID}`).classList.add('m--active-control');

                    $activeSlide = $slider.querySelector(`${prefix}slide-${slideID}`);
                    $activeControlsBg = $slider.querySelector(`${prefix}nav__bg-${slideID}`);

                    $slider.querySelector('.m--active-slide').classList.add('m--previous-slide');
                    $slider.querySelector('.m--active-nav-bg').classList.add('m--previous-nav-bg');

                    $activeSlide.classList.add('m--before-sliding');
                    $activeControlsBg.classList.add('m--nav-bg-before');

                    const layoutTrigger = $activeSlide.offsetTop;

                    $activeSlide.classList.add('m--active-slide');
                    $activeControlsBg.classList.add('m--active-nav-bg');

                    setTimeout(afterSlidingHandler, slidingAT + slidingDelay);
                }


                function controlClickHandler() {
                    if (sliding) return;
                    if (this.classList.contains('m--active-control')) return;
                    if (options.blockASafterClick) {
                        autoSlidingBlocked = true;
                        $slider.classList.add('m--autosliding-blocked');
                    }

                    const slideID = +this.getAttribute('data-slide');

                    performSliding(slideID);
                }

                $controls.forEach(($control) => {
                    $control.addEventListener('click', controlClickHandler);
                });

                function setAutoslidingTO() {
                    window.clearTimeout(autoSlidingTO);
                    const delay = +options.autoSlidingDelay || autoSlidingDelay;
                    curSlide++;
                    if (curSlide > numOfSlides) curSlide = 1;

                    autoSlidingTO = setTimeout(() => {
                        performSliding(curSlide);
                    }, delay);
                }

                if (options.autoSliding || +options.autoSlidingDelay > 0) {
                    if (options.autoSliding === false) return;

                    autoSlidingActive = true;
                    setAutoslidingTO();

                    $slider.classList.add('m--with-autosliding');
                    const triggerLayout = $slider.offsetTop;

                    let delay = +options.autoSlidingDelay || autoSlidingDelay;
                    delay += slidingDelay + slidingAT;

                    $progressAS.forEach(($progress) => {
                        $progress.style.transition = `transform ${delay / 1000}s`;
                    });
                }

                $slider.querySelector('.fnc-nav__control:first-child').classList.add('m--active-control');
            }

            const fncSlider = function (sliderSelector, options) {
                const $sliders = $$(sliderSelector);

                $sliders.forEach(($slider) => {
                    _fncSliderInit($slider, options);
                });
            };

            window.fncSlider = fncSlider;
        }());

        /* not part of the slider scripts */

        /* Slider initialization
options:
autoSliding - boolean
autoSlidingDelay - delay in ms. If audoSliding is on and no value provided, default value is 5000
blockASafterClick - boolean. If user clicked any sliding control, autosliding won't start again
*/
        fncSlider('.example-slider', { autoSlidingDelay: 4000 });

        // const $demoCont = document.querySelector('.demo-cont');

        // [].slice.call(document.querySelectorAll('.fnc-slide__action-btn')).forEach(($btn) => {
        //     $btn.addEventListener('click', () => {
        //         $demoCont.classList.toggle('credits-active');
        //     });
        // });

        // document.querySelector('.demo-cont__credits-close').addEventListener('click', () => {
        //     $demoCont.classList.remove('credits-active');
        // });

        // document.querySelector('.js-activate-global-blending').addEventListener('click', () => {
        //     document.querySelector('.example-slider').classList.toggle('m--global-blending-active');
        // });
        });
    }
};
</script>


<style scoped>
.fnc {
  /* you can add color names and their values here
  and then simply add classes like .m--blend-$colorName to .fnc-slide
  to apply specific color for mask blend mode */
}
.fnc-slider {
  overflow: hidden;
  box-sizing: border-box;
  position: relative;
  height: 100vh;
}
.fnc-slider *, .fnc-slider *:before, .fnc-slider *:after {
  box-sizing: border-box;
}
.fnc-slider__slides {
  position: relative;
  height: 100%;
  transition: -webkit-transform 1s 0.6666666667s;
  transition: transform 1s 0.6666666667s;
  transition: transform 1s 0.6666666667s, -webkit-transform 1s 0.6666666667s;
}
.fnc-slider .m--blend-dark .fnc-slide__inner {
  background-color: #8a8a8a;
}
.fnc-slider .m--blend-dark .fnc-slide__mask-inner {
  background-color: #575757;
}
.fnc-slider .m--navbg-dark {
  background-color: #575757;
}
.fnc-slider .m--blend-green .fnc-slide__inner {
  background-color: #6d9b98;
}
.fnc-slider .m--blend-green .fnc-slide__mask-inner {
  background-color: puple;
}
.fnc-slider .m--navbg-green {
  background-color: #42605E;
}
.fnc-slider .m--blend-red .fnc-slide__inner {
  background-color: #ea2329;
}
.fnc-slider .m--blend-red .fnc-slide__mask-inner {
  background-color: white;
}
.fnc-slider .m--navbg-red {
  background-color: #990e13;
}
.fnc-slider .m--blend-blue .fnc-slide__inner {
  background-color: #59aecb;
}
.fnc-slider .m--blend-blue .fnc-slide__mask-inner {
  background-color: #2D7791;
}
.fnc-slider .m--navbg-blue {
  background-color: #2D7791;
}
.fnc-slide {
  overflow: hidden;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}
.fnc-slide.m--before-sliding {
  z-index: 2 !important;
  -webkit-transform: translate3d(100%, 0, 0);
          transform: translate3d(100%, 0, 0);
}
.fnc-slide.m--active-slide {
  z-index: 1;
  transition: -webkit-transform 1s 0.6666666667s ease-in-out;
  transition: transform 1s 0.6666666667s ease-in-out;
  transition: transform 1s 0.6666666667s ease-in-out,
  -webkit-transform 1s 0.6666666667s ease-in-out;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}
.fnc-slide__inner {
  position: relative;
  height: 100%;
  background-size: cover;
  background-position: center top;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}
.m--global-blending-active .fnc-slide__inner, .m--blend-bg-active .fnc-slide__inner {
  background-blend-mode: luminosity;
}
.m--before-sliding .fnc-slide__inner {
  -webkit-transform: translate3d(-100%, 0, 0);
          transform: translate3d(-100%, 0, 0);
}
.m--active-slide .fnc-slide__inner {
  transition: -webkit-transform 1s 0.6666666667s ease-in-out;
  transition: transform 1s 0.6666666667s ease-in-out;
  transition: transform 1s 0.6666666667s ease-in-out,
  -webkit-transform 1s 0.6666666667s ease-in-out;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}
.fnc-slide__mask {
  overflow: hidden;
  z-index: 1;
  position: absolute;
  right: 60%;
  top: 15%;
  width: 50.25vh;
  height: 67vh;
  margin-right: -90px;
  -webkit-clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 0 0, 6vh 0,
                              6vh 61vh, 44vh 61vh, 44vh 6vh, 6vh 6vh);
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 0 0, 6vh 0, 6vh 61vh,
                      44vh 61vh, 44vh 6vh, 6vh 6vh);
  -webkit-transform-origin: 50% 0;
          transform-origin: 50% 0;
  transition-timing-function: ease-in-out;
}
.m--before-sliding .fnc-slide__mask {
  -webkit-transform: rotate(-10deg) translate3d(200px, 0, 0);
          transform: rotate(-10deg) translate3d(200px, 0, 0);
  opacity: 0;
}
.m--active-slide .fnc-slide__mask {
  transition: opacity 0.35s 1.2222222222s, -webkit-transform 0.7s 1.2222222222s;
  transition: transform 0.7s 1.2222222222s, opacity 0.35s 1.2222222222s;
  transition: transform 0.7s 1.2222222222s, opacity 0.35s 1.2222222222s,
  -webkit-transform 0.7s 1.2222222222s;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
  opacity: 1;
}
.m--previous-slide .fnc-slide__mask {
  transition: opacity 0.35s 0.6833333333s, -webkit-transform 0.7s 0.3333333333s;
  transition: transform 0.7s 0.3333333333s, opacity 0.35s 0.6833333333s;
  transition: transform 0.7s 0.3333333333s, opacity 0.35s 0.6833333333s,
  -webkit-transform 0.7s 0.3333333333s;
  -webkit-transform: rotate(10deg) translate3d(-200px, 0, 0);
          transform: rotate(10deg) translate3d(-200px, 0, 0);
  opacity: 0;
}
.fnc-slide__mask-inner {
  z-index: -1;
  position: absolute;
  left: 50%;
  top: 50%;
  width: 100vw;
  height: 100vh;
  margin-left: -50vw;
  margin-top: -50vh;
  background-size: cover;
  background-position: center center;
  background-blend-mode: luminosity;
  -webkit-transform-origin: 50% 16.5vh;
          transform-origin: 50% 16.5vh;
  transition-timing-function: ease-in-out;
}
.m--before-sliding .fnc-slide__mask-inner {
  -webkit-transform: translateY(0) rotate(10deg) translateX(-200px) translateZ(0);
          transform: translateY(0) rotate(10deg) translateX(-200px) translateZ(0);
}
.m--active-slide .fnc-slide__mask-inner {
  transition: -webkit-transform 0.7s 1.2222222222s;
  transition: transform 0.7s 1.2222222222s;
  transition: transform 0.7s 1.2222222222s, -webkit-transform 0.7s 1.2222222222s;
  -webkit-transform: translateX(0);
          transform: translateX(0);
}
.m--previous-slide .fnc-slide__mask-inner {
  transition: -webkit-transform 0.7s 0.3333333333s;
  transition: transform 0.7s 0.3333333333s;
  transition: transform 0.7s 0.3333333333s, -webkit-transform 0.7s 0.3333333333s;
  -webkit-transform: translateY(0) rotate(-10deg) translateX(200px) translateZ(0);
          transform: translateY(0) rotate(-10deg) translateX(200px) translateZ(0);
}
.fnc-slide__content {
  z-index: 2;
  position: absolute;
  left: 40%;
  top: 40%;
}
.fnc-slide__heading {
  margin-bottom: 10px;
  text-transform: uppercase;
}
.fnc-slide__heading-line {
  overflow: hidden;
  position: relative;
  padding-right: 20px;
  font-size: 100px;
  color: #fff;
  word-spacing: 10px;
}
.fnc-slide__heading-line:nth-child(2) {
  padding-left: 30px;
}
.m--before-sliding .fnc-slide__heading-line {
  -webkit-transform: translateY(100%);
          transform: translateY(100%);
}
.m--active-slide .fnc-slide__heading-line {
  transition: -webkit-transform 1.5s 1s;
  transition: transform 1.5s 1s;
  transition: transform 1.5s 1s, -webkit-transform 1.5s 1s;
  -webkit-transform: translateY(0);
          transform: translateY(0);
}
.m--previous-slide .fnc-slide__heading-line {
  transition: -webkit-transform 1.5s;
  transition: transform 1.5s;
  transition: transform 1.5s, -webkit-transform 1.5s;
  -webkit-transform: translateY(-100%);
          transform: translateY(-100%);
}
.fnc-slide__heading-line span {
  display: block;
}
.m--before-sliding .fnc-slide__heading-line span {
  -webkit-transform: translateY(-100%);
          transform: translateY(-100%);
}
.m--active-slide .fnc-slide__heading-line span {
  transition: -webkit-transform 1.5s 1s;
  transition: transform 1.5s 1s;
  transition: transform 1.5s 1s, -webkit-transform 1.5s 1s;
  -webkit-transform: translateY(0);
          transform: translateY(0);
}
.m--previous-slide .fnc-slide__heading-line span {
  transition: -webkit-transform 1.5s;
  transition: transform 1.5s;
  transition: transform 1.5s, -webkit-transform 1.5s;
  -webkit-transform: translateY(100%);
          transform: translateY(100%);
}
.fnc-nav {
  z-index: 5;
  position: absolute;
  right: 0;
  bottom: 0;
}
.fnc-nav__bgs {
  z-index: -1;
  overflow: hidden;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}
.fnc-nav__bg {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}
.fnc-nav__bg.m--nav-bg-before {
  z-index: 2 !important;
  -webkit-transform: translateX(100%);
          transform: translateX(100%);
}
.fnc-nav__bg.m--active-nav-bg {
  z-index: 1;
  transition: -webkit-transform 1s 0.6666666667s;
  transition: transform 1s 0.6666666667s;
  transition: transform 1s 0.6666666667s, -webkit-transform 1s 0.6666666667s;
  -webkit-transform: translateX(0);
          transform: translateX(0);
}
.fnc-nav__controls {
  font-size: 0;
}
.fnc-nav__control {
  overflow: hidden;
  position: relative;
  display: inline-block;
  vertical-align: top;
  width: 100px;
  height: 50px;
  font-size: 14px;
  color: #fff;
  text-transform: uppercase;
  background: transparent;
  border: none;
  outline: none;
  cursor: pointer;
  transition: background-color 0.5s;
}
.fnc-nav__control.m--active-control {
  background: #1F2833;
}
.fnc-nav__control-progress {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background: #fff;
  -webkit-transform-origin: 0 50%;
          transform-origin: 0 50%;
  -webkit-transform: scaleX(0);
          transform: scaleX(0);
  transition-timing-function: linear !important;
}
.m--with-autosliding .m--active-control .fnc-nav__control-progress {
  -webkit-transform: scaleX(1);
          transform: scaleX(1);
}
.m--prev-control .fnc-nav__control-progress {
  -webkit-transform: translateX(100%);
          transform: translateX(100%);
  transition: -webkit-transform 0.5s !important;
  transition: transform 0.5s !important;
  transition: transform 0.5s, -webkit-transform 0.5s !important;
}
.m--reset-progress .fnc-nav__control-progress {
  -webkit-transform: scaleX(0);
          transform: scaleX(0);
  transition: -webkit-transform 0s 0s !important;
  transition: transform 0s 0s !important;
  transition: transform 0s 0s, -webkit-transform 0s 0s !important;
}
.m--autosliding-blocked .fnc-nav__control-progress {
  transition: all 0s 0s !important;
  -webkit-transform: scaleX(0) !important;
          transform: scaleX(0) !important;
}

/* NOT PART OF COMMON SLIDER STYLES */
body {
  margin: 0;
}

.example-slider {
  z-index: 2;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
  transition: -webkit-transform 0.7s;
  transition: transform 0.7s;
  transition: transform 0.7s, -webkit-transform 0.7s;
}
.credits-active .example-slider {
  -webkit-transform: translate3d(-400px, 0, 0) rotateY(10deg) scale(0.9);
          transform: translate3d(-400px, 0, 0) rotateY(10deg) scale(0.9);
}
.example-slider .fnc-slide-1 .fnc-slide__inner,
.example-slider .fnc-slide-1 .fnc-slide__mask-inner {
  background-image: url("/static/img/lalaland_wallpaper.jpg");
}
.example-slider .fnc-slide-2 .fnc-slide__inner,
.example-slider .fnc-slide-2 .fnc-slide__mask-inner {
  background-image: url("/static/img/harry-potter-wallpaper.jpg");
}
.example-slider .fnc-slide-3 .fnc-slide__inner,
.example-slider .fnc-slide-3 .fnc-slide__mask-inner {
  background-image: url("/static/img/lobster_wallpaper.jpg");
}
.example-slider .fnc-slide-3 .fnc-slide__inner:before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
}
.example-slider .fnc-slide-4 .fnc-slide__inner,
.example-slider .fnc-slide-4 .fnc-slide__mask-inner {
  background-image: url("/static/img/inception_wallpaper.jpg");
}
.example-slider .fnc-slide-4 .fnc-slide__inner:before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2);
}
.example-slider .fnc-slide__heading,
.example-slider .fnc-slide__action-btn,
.example-slider .fnc-nav__control {
  font-family: "Open Sans", Helvetica, Arial, sans-serif;
}

/* COLORFUL SWITCH STYLES
   ORIGINAL DEMO - https://codepen.io/suez/pen/WQjwOb */
.colorful-switch {
  position: relative;
  width: 180px;
  height: 77.1428571429px;
  margin: 0 auto;
  border-radius: 32.1428571429px;
  background: #cfcfcf;
}
.colorful-switch:before {
  content: "";
  z-index: -1;
  position: absolute;
  left: -5px;
  top: -5px;
  width: 190px;
  height: 87.1428571429px;
  border-radius: 37.1428571429px;
  background: #314239;
  transition: background-color 0.3s;
}
.colorful-switch:hover:before {
  background: #4C735F;
}
.colorful-switch__checkbox {
  z-index: -10;
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
}
.colorful-switch__label {
  z-index: 1;
  overflow: hidden;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  border-radius: 32.1428571429px;
  cursor: pointer;
}
.colorful-switch__bg {
  position: absolute;
  left: 0;
  top: 0;
  width: 540px;
  height: 100%;
  background: linear-gradient(90deg, #14DCD6 0, #10E7BD 180px, #EF9C29 360px, #E76339 100%);
  transition: -webkit-transform 0.5s;
  transition: transform 0.5s;
  transition: transform 0.5s, -webkit-transform 0.5s;
  -webkit-transform: translate3d(-360px, 0, 0);
          transform: translate3d(-360px, 0, 0);
}
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__bg {
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}
.colorful-switch__dot {
  position: absolute;
  left: 131.1428571429px;
  top: 50%;
  width: 5.1428571429px;
  height: 5.1428571429px;
  margin-left: -2.5714285714px;
  margin-top: -2.5714285714px;
  border-radius: 50%;
  background: #fff;
  transition: -webkit-transform 0.5s;
  transition: transform 0.5s;
  transition: transform 0.5s, -webkit-transform 0.5s;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__dot {
  -webkit-transform: translate3d(-80.3571428571px, 0, 0);
          transform: translate3d(-80.3571428571px, 0, 0);
}
.colorful-switch__on {
  position: absolute;
  left: 104.1428571429px;
  top: 22.5px;
  width: 19.2857142857px;
  height: 36px;
  transition: -webkit-transform 0.5s;
  transition: transform 0.5s;
  transition: transform 0.5s, -webkit-transform 0.5s;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__on {
  -webkit-transform: translate3d(-80.3571428571px, 0, 0);
          transform: translate3d(-80.3571428571px, 0, 0);
}
.colorful-switch__on__inner {
  position: absolute;
  width: 100%;
  height: 100%;
  transition: -webkit-transform 0.25s 0s cubic-bezier(0.52, -0.96, 0.51, 1.28);
  transition: transform 0.25s 0s cubic-bezier(0.52, -0.96, 0.51, 1.28);
  transition: transform 0.25s 0s cubic-bezier(0.52, -0.96, 0.51, 1.28),
  -webkit-transform 0.25s 0s cubic-bezier(0.52, -0.96, 0.51, 1.28);
  -webkit-transform-origin: 100% 50%;
          transform-origin: 100% 50%;
  -webkit-transform: rotate(45deg) scale(0) translateZ(0);
          transform: rotate(45deg) scale(0) translateZ(0);
}
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__on__inner {
  transition: -webkit-transform 0.25s 0.25s cubic-bezier(0.67, -0.16, 0.47, 1.61);
  transition: transform 0.25s 0.25s cubic-bezier(0.67, -0.16, 0.47, 1.61);
  transition: transform 0.25s 0.25s cubic-bezier(0.67, -0.16, 0.47, 1.61),
  -webkit-transform 0.25s 0.25s cubic-bezier(0.67, -0.16, 0.47, 1.61);
  -webkit-transform: rotate(45deg) scale(1) translateZ(0);
          transform: rotate(45deg) scale(1) translateZ(0);
}
.colorful-switch__on__inner:before, .colorful-switch__on__inner:after {
  content: "";
  position: absolute;
  border-radius: 2.5714285714px;
  background: #fff;
}
.colorful-switch__on__inner:before {
  left: 0;
  bottom: 0;
  width: 100%;
  height: 6.1428571429px;
}
.colorful-switch__on__inner:after {
  right: 0;
  top: 0;
  width: 6.1428571429px;
  height: 100%;
}
.colorful-switch__off {
  position: absolute;
  left: 131.1428571429px;
  top: 50%;
  width: 41.1428571429px;
  height: 41.1428571429px;
  margin-left: -20.5714285714px;
  margin-top: -20.5714285714px;
  transition: -webkit-transform 0.5s;
  transition: transform 0.5s;
  transition: transform 0.5s, -webkit-transform 0.5s;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__off {
  -webkit-transform: translate3d(-80.3571428571px, 0, 0);
          transform: translate3d(-80.3571428571px, 0, 0);
}
.colorful-switch__off:before, .colorful-switch__off:after {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  width: 100%;
  height: 5.1428571429px;
  margin-top: -2.5714285714px;
  border-radius: 2.5714285714px;
  background: #fff;
  transition: -webkit-transform 0.25s 0.25s;
  transition: transform 0.25s 0.25s;
  transition: transform 0.25s 0.25s, -webkit-transform 0.25s 0.25s;
}
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__off:before,
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__off:after {
  transition-delay: 0s;
}
.colorful-switch__off:before {
  -webkit-transform: rotate(45deg) scaleX(1) translateZ(0);
          transform: rotate(45deg) scaleX(1) translateZ(0);
}
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__off:before {
  -webkit-transform: rotate(45deg) scaleX(0) translateZ(0);
          transform: rotate(45deg) scaleX(0) translateZ(0);
}
.colorful-switch__off:after {
  transition-timing-function: cubic-bezier(0.67, -0.16, 0.47, 1.61);
  -webkit-transform: rotate(-45deg) scaleX(1) translateZ(0);
          transform: rotate(-45deg) scaleX(1) translateZ(0);
}
.colorful-switch__checkbox:checked ~ .colorful-switch__label .colorful-switch__off:after {
  transition-timing-function: ease;
  -webkit-transform: rotate(-45deg) scaleX(0) translateZ(0);
          transform: rotate(-45deg) scaleX(0) translateZ(0);
}

</style>
