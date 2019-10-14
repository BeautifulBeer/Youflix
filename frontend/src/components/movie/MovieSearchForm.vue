<template>
    <div>
        <v-form ref="form">
            <v-combobox v-model="selected" :items="genres" label="Genre" multiple chips />
            <v-text-field v-model="title" label="영화 제목" />
            <v-layout justify-center pa-10>
                <v-btn large color="indigo white--text" @click="onSubmit">Search</v-btn>
            </v-layout>
        </v-form>
        <v-layout justify-center pa-10>
            <v-btn-toggle v-model="selectSort">
                <v-btn text value="titleASC">제목(오름차순)</v-btn>
                <v-btn text value="titleDESC">제목(내림차순)</v-btn>
                <v-btn text value="viewASC">조회순(오름차순)</v-btn>
                <v-btn text value="viewDESC">조회순(내림차순)</v-btn>
                <v-btn text value="rating">평점순</v-btn>
            </v-btn-toggle>
        </v-layout>
    </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    submit: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
      selected: [],
      genres: [
        "TV Movie",
        "Foreign",
        "War",
        "Family",
        "Romance",
        "Music",
        "Mystery",
        "Science Fiction",
        "Documentary",
        "Crime",
        "Thriller",
        "Western",
        "History",
        "Comedy",
        "Action",
        "Horror",
        "Drama",
        "Animation",
        "Fantasy",
        "Adventure"
      ],
      title: "",
      selectSort: ""
    };
  },
  computed: {
    ...mapState({
      movieSearchList: state => state.data.movieSearchList
    })
  },
  watch: {
    selectSort() {
      this.sortMovieListCard();
    }
  },
  methods: {
    onSubmit() {
      const params = {
        title: this.title,
        genres: JSON.stringify(this.selected)
      };
      this.submit(params);
    },

    sortMovieListCard() {
      if (this.selectSort === undefined) return;

      if (this.selectSort == "titleASC") {
        this.movieSearchList.sort((a, b) => (a.title < b.title ? -1 : 1));
      } else if (this.selectSort == "titleDESC") {
        this.movieSearchList.sort((a, b) =>
          a.title < b.title ? 1 : a.title > b.title ? -1 : 1
        );
      } else if (this.selectSort == "viewASC") {
        this.movieSearchList.sort((a, b) => (a.viewCnt < b.viewCnt ? -1 : 1));
      } else if (this.selectSort == "viewDESC") {
        this.movieSearchList.sort((a, b) => (a.viewCnt < b.viewCnt ? 1 : -1));
      } else {
        this.movieSearchList.sort((a, b) => (a.rating < b.rating ? 1 : -1));
      }
    }
  }
};
</script>
