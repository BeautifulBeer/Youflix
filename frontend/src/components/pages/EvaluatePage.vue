<template>
    <v-container>
        <v-row
            justify="center"
            class="evaluate-header text-center"
        >
            <v-col
                cols="12"
                class="view-count"
            >
                {{ ratingCount }}
            </v-col>

            <v-col
                cols="12"
                class="view-count-content"
            >
                {{ ratingWord }}
            </v-col>
            <v-col
                cols="7"
                style="width: 50%;"
            >
                <v-progress-linear
                    :value="ratingCount"
                    color="white"
                />
            </v-col>
        </v-row>

        <v-row
            class="pa-2"
            fluid
            grid-list-md
        >
            <v-row
                align="center"
                justify="start"
                class="content-wrapper"
            >
                <MyTastes
                    v-for="(element, index) in movieList"
                    :key="index"
                    :element="element"
                />
            </v-row>
        </v-row>

        <v-row
            style="margin-top: 50px;"
            justify="center"
        >
            <v-btn
                class="primary"
                :loading="moreWord === 'MORE' ? false : true"
                large
                @click="loadMovieList()"
            >
                {{ moreWord }}
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>
// import VUEX
import { createNamespacedHelpers } from 'vuex';

// import Component
import MyTastes from '../user/MyTastes.vue';

const userMapState = createNamespacedHelpers('users').mapState;
const movieMapActions = createNamespacedHelpers('movies').mapActions;
const movieMapMutations = createNamespacedHelpers('movies').mapMutations;

export default {
    components: {
        MyTastes
    },
    data() {
        return {
            movieList: [],
            ratingWord: '',
            moreWord: 'MORE',
            page: 1,
            ratingCount: -1
        };
    },
    computed: {
        ...userMapState(['user']),
        getUserEmail() {
            if (this.user) {
                return this.user.email;
            }
            return false;
        }
    },
    watch: {
        // eslint-disable-next-line
        getUserEmail: function(val) {
            if (val) {
                this.getContentBased({ email: val, flag: false }).then((ret) => {
                    this.$log.debug('EvaluatePage.vue getContentBased', ret);
                    this.setIsLoaded(true);
                    this.movieList = this.movieList.concat(ret.result);
                    this.ratingCount = ret.msg;
                });
            }
        },
        ratingCount() {
            if (this.ratingCount === 0) {
                this.ratingWord = '지금까지 본 영화를 평가해주시면 다양하게 추천해드릴 수 있어요! :)';
            } else if (this.ratingCount < 5) {
                this.ratingWord = '평가만 하는 것도 나름 재미있지 않으세요?';
            } else if (this.ratingCount < 10) {
                this.ratingWord = '좋아요. 이제 조금씩 취향의 윤곽이 드러납니다.';
            } else if (this.ratingCount < 13) {
                this.ratingWord = '10개 달성! 시간이 괜찮다면 계속 더 평가해보세요. 추천이 더욱 정확해져요.';
            } else if (this.ratingCount < 20) {
                this.ratingWord = '더 하시기로 마음 먹으셨군요! 좋아요 :)';
            } else if (this.ratingCount < 23) {
                this.ratingWord = '어떤 작품을 좋아하실지 조금씩 감이 와요.';
            } else if (this.ratingCount < 25) {
                this.ratingWord = '아하, 이런 스타일이시군요!';
            } else if (this.ratingCount < 30) {
                this.ratingWord = '30개 평가가 눈 앞이에요!';
            } else if (this.ratingCount < 33) {
                this.ratingWord = '와우! 취향 독특하신데요?';
            } else if (this.ratingCount < 40) {
                this.ratingWord = '한번 마음 먹으면 하는 분이시네요.';
            } else if (this.ratingCount < 43) {
                this.ratingWord = '기왕 이렇게 된 거 50개 가보죠!.';
            } else if (this.ratingCount < 100) {
                this.ratingWord = '훌륭해요! 이 기세로 쭉쭉 밀고 나가봐요!';
            } else {
                this.ratingWord = '오, 정말 많이 보셨네요. 인정합니다! :)';
            }
        }
    },
    mounted() {
        if (this.getUserEmail) {
            this.getContentBased({ email: this.getUserEmail, flag: false }).then((ret) => {
                this.$log.debug('EvaluatePage.vue getContentBased', ret);
                this.setIsLoaded(true);
                this.movieList = this.movieList.concat(ret.result);
                this.ratingCount = ret.msg;
            });
        }
    },
    methods: {
        ...movieMapActions(['getNeverSeenMovieList', 'getContentBased']),
        ...movieMapMutations(['setIsLoaded']),
        urlMapping(value) {
            return `url(${value}) center / cover no-repeat`;
        },
        loadMovieList() {
            this.moreWord = 'LOADING...';
            this.page += 1;
            this.getContentBased({ email: this.getUserEmail, flag: true, page: this.page }).then((ret) => {
                this.$log.debug('EvaluatePage.vue getContentBased', ret);
                this.movieList = this.movieList.concat(ret.result);
                this.moreWord = 'MORE';
                this.ratingCount = ret.msg;
            });
        }
    }
};
</script>

<style lang="scss" scoped>

* {
    color: white;
}

.evaluate-header {

    margin-top: 50px;
    margin-right: 100px;
    margin-left: 100px;
    margin-bottom: 50px;
}

.view-count {
    font-size: 1.7em;
    font-weight: bold;
}

.view-count-content {
    color: rgba(255, 255, 255, 0.7);
}

.content-wrapper{
    padding: 0px 100px 0px 100px;
    min-height: 75vh;
}

.no-result-text{
    font-size: 4em;
    color: white;
}

</style>
