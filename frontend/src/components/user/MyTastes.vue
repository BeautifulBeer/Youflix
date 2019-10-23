<template>
    <div class="row">
        <div class="movie-container card">
            <div
                class="wrapper"
                :style="{ background: urlMapping(element.poster_path) }"
            >
                <div class="data text-center">
                    <div class="content">
                        <h1 class="title">
                            {{ element.movie_title }}
                        </h1>
                        <div class="date">
                            <span class="year">
                                {{ element.release_date }}
                            </span>
                        </div>
                        <div>
                            <span @click="ratingMovie()">
                                <v-rating
                                    id="ratingStar"
                                    v-model="rating"
                                    dense
                                    color="white"
                                    background-color="white"
                                    half-increments
                                    hover
                                />
                            </span>
                            {{ ratingWord }}
                        </div>
                        <a
                            href="#"
                            class="button"
                        >
                            자세히 보기
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import VUEX
import { createNamespacedHelpers } from 'vuex';

const userMapState = createNamespacedHelpers('users').mapState;
const userMapActions = createNamespacedHelpers('users').mapActions;
const ratingMapActions = createNamespacedHelpers('ratings').mapActions;

export default {
    props: {
        element: { type: Object, default: null }
    },
    data() {
        return {
            rating: 0,
            ratingWord: '최고에요!'
        };
    },
    computed: {
        ...userMapState(['user'])
    },
    mounted() {
        if (this.user === null) {
            this.getSession();
        }
        this.rating = this.element.rating;

        if (this.rating === 0.5) {
            this.ratingWord = '최악이에요!';
        } else if (this.rating === 1.0) {
            this.ratingWord = '싫어요';
        } else if (this.rating === 1.5) {
            this.ratingWord = '재미없어요';
        } else if (this.rating === 2.0) {
            this.ratingWord = '별로에요';
        } else if (this.rating === 2.5) {
            this.ratingWord = '부족해요';
        } else if (this.rating === 3.0) {
            this.ratingWord = '보통이에요';
        } else if (this.rating === 3.5) {
            this.ratingWord = '볼만해요';
        } else if (this.rating === 4.0) {
            this.ratingWord = '재미있어요';
        } else if (this.rating === 4.5) {
            this.ratingWord = '훌륭해요';
        }
    },
    methods: {
        ...ratingMapActions(['rateMovie']),
        ...userMapActions(['getSession']),
        urlMapping(value) {
            return `url(${value}) center / cover no-repeat`;
        },
        ratingMovie() {
            this.rateMovie(
                {
                    email: this.user.email,
                    movie_id: this.element.movie_id,
                    ratingValue: this.rating
                }
            ).then((ret) => {
                this.ratingWord = ret;
            });
        }
    }
};
</script>

<style lang="scss" scoped>
@import url(https://fonts.googleapis.com/css?family=Open+Sans:300,400,700);
// Variables
$regal-blue: #034378;
$san-juan: #2d4e68;
$bermuda: #77d7b9;
$white: #fff;
$black: #000;
$open-sans: 'Open Sans',
sans-serif;
// clear-fix mixin
@mixin cf {
  &::before,
  &::after {
    content: '';
    display: table;
  }
  &::after {
    clear: both;
  }
}

* {
  box-sizing: border-box;
}

body {
  background-image: linear-gradient(to right, $regal-blue, $san-juan);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  font-family: $open-sans;
}

a {
  text-decoration: none;
}

h1 {
  font-family: $open-sans;
  font-weight: 500;
}

.row {
  margin: 20px;
  width: 200px;
  max-width: 200px;
}

.card {
  float: left;
  width: 100%;
  .menu-content {
    @include cf;
    margin: 0;
    padding: 0;
    list-style-type: none;
    li {
      display: inline-block;
    }
    a {
      color: $white;
    }
    span {
      position: absolute;
      left: 50%;
      top: 0;
      font-size: 10px;
      font-weight: 700;
      font-family: 'Open Sans';
      transform: translate(-50%, 0);
    }
  }
  .wrapper {
    background-color: $white;
    min-height: 300px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 19px 38px rgba($black, 0.3), 0 15px 12px rgba($black, 0.2);
    &:hover {
      .data {
        transform: translateY(0);
      }
    }
  }
  .data {
    background-color: rgba($black, 0.7);
    position: absolute;
    bottom: 0;
    width: 100%;
    transform: translateY(calc(70px + 1em));
    transition: transform 0.3s;
    .content {
      padding: 1em;
      position: relative;
      z-index: 1;
    }
  }
  .author {
    font-size: 12px;
  }
  .title {
    margin-top: 10px;
    margin-bottom: 30px;
  }
  .text {
    height: 70px;
    margin: 0;
  }
  input[type='checkbox'] {
    display: none;
  }
  input[type='checkbox']:checked + .menu-content {
    transform: translateY(-60px);
  }
}

.movie-container {
  .wrapper {
    &:hover {
      .menu-content {
        span {
          transform: translate(-50%, -10px);
          opacity: 1;
        }
      }
    }
  }
  .header {
    @include cf;
    color: $white;
    padding: 1em;
    .date {
      float: left;
      font-size: 10px;
    }
  }
  .menu-content {
    float: right;
    li {
      margin: 0 5px;
      position: relative;
    }
    span {
      transition: all 0.3s;
      opacity: 0;
    }
  }
  .data {
    color: $white;
    transform: translateY(calc(70px + 4em));
  }
  .title {
    a {
      color: $white;
    }
  }
  .button {
    display: block;
    width: 100px;
    margin: 2em auto 1em;
    text-align: center;
    font-size: 12px;
    color: $white;
    line-height: 1;
    position: relative;
    font-weight: 700;
    &::after {
      content: '\2192';
      opacity: 0;
      position: absolute;
      right: 0;
      top: 50%;
      transform: translate(0, -50%);
      transition: all 0.3s;
    }
    &:hover {
      &::after {
        transform: translate(5px, -50%);
        opacity: 1;
      }
    }
  }
}
</style>
