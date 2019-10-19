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
                                    {{ userInfo.username }}
                                    <br>
                                    {{ userInfo.email }}
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
                            <v-divider />

                            <v-row>
                                <v-col>
                                    <v-form v-model="passwordFlag">
                                        <v-text-field
                                            v-model="newPassword"
                                            type="password"
                                            label="비밀번호 (최소 6자리이상, 30자리 이하)"
                                            :rules="[rules.passwordCheck, rules.passwordLenCheck]"
                                        />
                                    </v-form>
                                </v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>
                                    <v-form v-model="nicknameFlag">
                                        <v-text-field
                                            v-model="nickname"
                                            label="닉네임 (최소 2자리 이상, 10자리 이하)"
                                            :rules="[rules.nicknameCheck, rules.nicknameLenCheck]"
                                        />
                                    </v-form>
                                </v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>Age: {{ userInfo.age }}</v-col>
                            </v-row>

                            <v-divider />

                            <v-row>
                                <v-col>Gender: {{ userInfo.gender }}</v-col>
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
                        <v-btn
                            class="primary"
                            style="margin: 10px;"
                            @click="modify()"
                        >
                            수정하기
                        </v-btn>
                    </v-col>

                    <v-col>
                        <v-btn
                            class="error"
                            style="margin: 10px;"
                            @click="$router.go(-1)"
                        >
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
import { createNamespacedHelpers } from 'vuex';
// import SweetAlert
import swal from 'sweetalert';

const { mapState, mapActions } = createNamespacedHelpers('users');
const infoMapState = createNamespacedHelpers('infos').mapState;

export default {
    data() {
        return {
            nickname: '',
            newPassword: '',
            nicknameFlag: false,
            passwordFlag: false,
            userInfo: {},
            selectedOccupation: '',
            selectedGenre: []
        };
    },
    computed: {
        ...mapState(['token', 'user']),
        ...infoMapState(['rules', 'genres', 'occupations'])
    },
    mounted() {
        if (this.user === null) {
            this.getSession().then(() => {
                this.userInfo = this.user;
                this.selectedGenre = this.userInfo.movie_taste;
                this.selectedOccupation = this.userInfo.occupation;
            });
        } else {
            this.userInfo = this.user;
            this.selectedGenre = this.userInfo.movie_taste;
            this.selectedOccupation = this.userInfo.occupation;
        }
    },
    methods: {
        ...mapActions(['getSession']),
        ...mapActions(['updateUserInfo']),
        modify() {
            if (!this.passwordFlag || !this.nicknameFlag) {
                swal({
                    title: 'Warning',
                    text: '양식에 맞춰서 입력해주세요.',
                    icon: 'warning',
                    button: false
                });
                return;
            }
            this.updateUserInfo({
                token: this.token,
                email: this.userInfo.email,
                username: this.nickname,
                password: this.newPassword,
                occupation: this.selectedOccupation,
                genres: this.selectedGenre
            }).then((ret) => {
                if (ret) {
                    swal({
                        title: '수정 성공',
                        text: '정상적으로 변경 되었습니다.',
                        icon: 'success',
                        button: false
                    }).then(() => {
                        this.$router.push('/home');
                    });
                } else {
                    swal({
                        title: '수정 실패',
                        text: '관리자에게 문의하시길 바랍니다.',
                        icon: 'error',
                        button: false
                    }).then(() => {
                        this.$router.push('/home');
                    });
                }
            });
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

.error_area {

    color: red;
}
</style>
