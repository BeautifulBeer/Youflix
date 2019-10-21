<template>
    <v-hover
        v-slot:default="{ hover }"
        open-delay="100"
    >
        <v-card
            :class="{ 'on-hover': hover }"
            :elevation="hover ? 16 : 2"
            width="190"
            height="270"
            max-width="350"
            style="margin: 10px;"
        >
            <v-img
                :src="element.poster_path"
                width="190"
                height="270"
            >
                <v-card-text class="font-weight-medium mt-12 text-center subtitle-1">
                    {{ element.title }}
                </v-card-text>

                <div class="align-self-center">
                    <v-rating
                        id="ratingStar"
                        v-model="rating"
                        dense
                        color="white"
                        background-color="white"
                        half-increments
                        hover
                        :class="{ 'show-btns': hover }"
                    />
                </div>
            </v-img>
        </v-card>
    </v-hover>
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
            // ratingList: [],
            rating: 0
        };
    },
    computed: {
        ...userMapState(['user'])
    },
    mounted() {
        // if (this.user === null) {
        //     this.getSession().then(() => {
        //         this.getRating(this.user.email).then((ret) => {
        //             this.setRatingList(ret);
        //         });
        //     });
        // } else {
        //     this.getRating(this.user.email).then((ret) => {
        //         this.setRatingList(ret);
        //     });
        // }
    },
    methods: {
        ...ratingMapActions(['getRating']),
        ...userMapActions(['getSession'])
        // setRatingList(list) {
        //     list.forEach((element) => {
        //         this.ratingList.push(element);
        //     });
        // }
    }
};
</script>

<style scoped>
.v-card {
  transition: opacity .4s ease-in-out;
}

.v-card:not(.on-hover) {
  opacity: 0.6;
 }

.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
</style>
