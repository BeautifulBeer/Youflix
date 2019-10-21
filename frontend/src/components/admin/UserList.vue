<template>
    <div class="vld-parent">
        <Loading
            loader="dots"
            color="#E50914"
            :active.sync="isLoading"
            :is-full-page="fullPage"
        />
        <v-expansion-panels>
            <v-expansion-panel
                v-for="(user, index) in userList"
                :key="index"
            >
                <v-expansion-panel-header v-slot="{ open }">
                    <v-row no-gutters>
                        <v-col cols="4">
                            {{ user.username }}
                        </v-col>
                        <v-col
                            cols="8"
                            class="text--secondary"
                        >
                            <v-fade-transition leave-absolute>
                                <span v-if="user.is_staff">
                                    <v-icon color="red">mdi-account-card-details</v-icon>
                                </span>
                                <span v-else>
                                    <v-icon color="blue">mdi-account-box</v-icon>
                                </span>
                            </v-fade-transition>
                        </v-col>
                    </v-row>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-row no-gutters>
                        <v-divider
                            vertical
                            class="mx-4"
                        />
                        <v-col cols="2">
                            ID : {{ user.id }}
                        </v-col>
                        <v-col cols="2">
                            Occupation : {{ user.occupation }}
                        </v-col>
                        <v-col cols="2">
                            AGE : {{ user.age }}
                        </v-col>
                        <v-col cols="2">
                            Gender :
                            <v-icon
                                v-if="user.gender === 'M'"
                                color="blue"
                            >
                                mdi-human-male
                            </v-icon>
                            <v-icon
                                v-else
                                color="red"
                            >
                                mdi-human-female
                            </v-icon>
                        </v-col>
                    </v-row>
                    <v-card-actions v-if="!user.is_staff">
                        <div class="flex-grow-1" />
                        <v-btn
                            text
                            color="primary"
                        >
                            Modify
                        </v-btn>
                        <v-btn
                            text
                            color="secondary"
                        >
                            Cancel
                        </v-btn>
                    </v-card-actions>
                </v-expansion-panel-content>
            </v-expansion-panel>
            <v-row>
                <v-col>
                    <v-btn @click="loadMore()">
                        더보기
                    </v-btn>
                </v-col>
            </v-row>
        </v-expansion-panels>
    </div>
</template>

<script>
import Loading from 'vue-loading-overlay';
import API from '../../../api/user/userApi';

// import loading animations
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
    components: {
        Loading
    },
    data: () => ({
        userList: [],
        page: 1,

        isLoading: true,
        fullPage: true
    }),
    mounted() {
        this.getUsers();
    },
    methods: {
        async getUsers() {
            this.isLoading = true;

            await API.getUsers({ page: this.page }).then((ret) => {
                if (ret.data === undefined || ret.data.length === 0) return;

                if (ret.status === 200) {
                    if (this.userList.length === 0) {
                        this.userList = ret.data;
                    } else {
                        this.userList.push.spread(this.userList, ret.data);
                    }
                    this.isLoading = false;
                }
            });
        },
        loadMore() {
            this.page += 1;
            this.getUsers();
        }
    }
};
</script>
