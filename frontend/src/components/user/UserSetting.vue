<template>
    <div class="appMountPoint">
        <div class="setting-page">
            <div
                class="display-1"
                style="margin-bottom: 19px;"
            >
                계정
            </div>
            <v-alert type="info">
                회원님의 멤버십은 현재 결제 주기의 마지막 날에 해지됩니다.
            </v-alert>

            <v-divider />

            <v-container class="mg-top-none">
                <v-row>
                    <v-col cols="4">
                        프로필
                    </v-col>

                    <v-col class="pd-right-none">
                        <v-container class="mg-top-none">
                            <v-row class="mg-top-none">
                                <v-col
                                    cols="2"
                                    class="pd-none"
                                >
                                    <v-img
                                        width="32"
                                        height="32"
                                        src="../../assets/icon/avatar.png"
                                    />
                                </v-col>

                                <v-col class="mg-top-none text-light">
                                    테스트
                                    <br>test@naver.com
                                </v-col>

                                <v-col class="mg-top-none pd-right-none text-right">
                                    프로필 관리
                                    <br>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-col>
                </v-row>
            </v-container>

            <v-divider />

            <v-container class="mg-top-none">
                <v-row>
                    <v-col cols="4">
                        회원정보
                    </v-col>

                    <v-col class="pd-right-none">
                        <v-container class="mg-top-none">
                            <v-row class="mg-top-none">
                                <v-col class="mg-top-none">
                                    ABC123@naver.com
                                </v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>
                                    <v-text-field label="비밀번호" />
                                </v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>
                                    <v-text-field label="닉네임" />
                                </v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>Age: 1</v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>Gender: Other</v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>
                                    <v-combobox
                                        v-model="selectedOccupation"
                                        :items="occupations"
                                        label="Select your occupation"
                                    />
                                </v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>
                                    <v-combobox
                                        v-model="selectedGenre"
                                        :items="genres"
                                        label="Choose your favorite genre."
                                        multiple
                                        chips
                                    >
                                        <template v-slot:selection="data">
                                            <v-chip
                                                :key="JSON.stringify(data.item)"
                                                v-bind="data.attrs"
                                                :input-value="data.selected"
                                                :disabled="data.disabled"
                                                @click:close="data.parent.selectItem(data.item)"
                                            >
                                                <v-avatar
                                                    class="accent white--text"
                                                    left
                                                    v-text="data.item.slice(0, 1).toUpperCase()"
                                                />
                                                {{ data.item }}
                                            </v-chip>
                                        </template>
                                    </v-combobox>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-col>
                </v-row>
            </v-container>

            <v-divider />

            <v-container class="mg-top-none">
                <v-row class="text-center">
                    <v-col>
                        <v-btn style="margin: 10px;">
                            수정하기
                        </v-btn>
                    </v-col>

                    <v-col>
                        <v-btn style="margin: 10px;">
                            취 소
                        </v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </div>
</template>

<script>
// import VUEX
import { mapState } from 'vuex';

export default {
    data() {
        return {
            selectedOccupation: 'artist',
            occupations: ['other',
                'academic/educator',
                'artist',
                'clerical/admin',
                'college/grad student',
                'customer service',
                'doctor/health care',
                'executive/managerial',
                'farmer',
                'homemaker',
                'K-12 student',
                'lawyer',
                'programmer',
                'retired',
                'sales/marketing',
                'scientist',
                'self-employed',
                'technician/engineer',
                'tradesman/craftsman',
                'unemployed',
                'writer'],
            selectedGenre: ['Action', 'War']
        };
    },
    computed: {
        ...mapState({
            token: (state) => state.data.token,
            user: (state) => state.data.user,
            genres: (state) => state.info.genres
        })
    },
    mounted() {
        if (this.user === null) {
            this.getUserBySession(this.token).then(() => {
                this.username = this.user.username;
            });
        } else {
            this.username = this.user.username;
        }
    }
};
</script>

<style scoped>
.appMountPoint {
  background: #f3f3f3;
}

.setting-page {
  margin: auto auto;
  padding: 55px;
  color: #121218;
  background: #f3f3f3;

  width: 95%;
  max-width: 1024px;
}

.mg-top-none {
  padding-top: 0px;
}

.pd-right-none {
  padding-right: 0px;
}

.pd-none {
  padding: 0px;
}
</style>
