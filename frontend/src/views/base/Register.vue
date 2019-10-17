<template>
    <div id="background-cover">
        <div id="background-img" />

        <div
            id="loginForm-setting"
            class="white--text"
        >
            <div class="input-title">
                회원가입
            </div>

            <input
                id="username"
                v-model="username"
                class="input-setting input-top-radius"
                type="text"
                placeholder="닉네임 (홍길동)"
            >

            <input
                id="email"
                v-model="email"
                class="input-setting"
                type="text"
                placeholder="아이디 (example@gmail.com)"
            >

            <input
                id="pwd"
                v-model="pwd"
                class="input-setting"
                type="password"
                placeholder="비밀번호 (6자 이상)"
            >

            <select
                id="age"
                class="select-setting"
                name="age"
            >
                <option value>
                    Age
                </option>
                <option value="1">
                    Under 18
                </option>
                <option value="18">
                    18-24
                </option>
                <option value="25">
                    25-34
                </option>
                <option value="35">
                    35-44
                </option>
                <option value="45">
                    45-49
                </option>
                <option value="50">
                    50-55
                </option>
                <option value="56">
                    56+
                </option>
            </select>

            <select
                id="gender"
                class="a4a4a4--text select-setting"
                name="gender"
            >
                <option value>
                    Gender
                </option>
                <option value="male">
                    Male
                </option>
                <option value="female">
                    Female
                </option>
                <option value="other">
                    Other
                </option>
            </select>

            <select
                id="occupation"
                class="#a4a4a4--text select-setting"
                name="occupation"
            >
                <option value>
                    Occupation
                </option>
                <option value="other">
                    other
                </option>
                <option value="academic/educator">
                    academic/educator
                </option>
                <option value="artist">
                    artist
                </option>
                <option value="clerical/admin">
                    clerical/admin
                </option>
                <option value="college/grad student">
                    college/grad student
                </option>

                <option value="customer service">
                    customer service
                </option>
                <option value="doctor/health care">
                    doctor/health care
                </option>
                <option value="executive/managerial">
                    executive/managerial
                </option>
                <option value="farmer">
                    farmer
                </option>
                <option value="homemaker">
                    homemaker
                </option>

                <option value="K-12 student">
                    K-12 student
                </option>
                <option value="lawyer">
                    lawyer
                </option>
                <option value="programmer">
                    programmer
                </option>
                <option value="retired">
                    retired
                </option>
                <option value="sales/marketing">
                    sales/marketing
                </option>

                <option value="scientist">
                    scientist
                </option>
                <option value="self-employed">
                    self-employed
                </option>
                <option value="technician/engineer">
                    technician/engineer
                </option>
                <option value="tradesman/craftsman">
                    tradesman/craftsman
                </option>
                <option value="unemployed">
                    unemployed
                </option>
                <option value="writer">
                    writer
                </option>
            </select>

            <input
                class="#a4a4a4--text input-bottom-radius input-setting"
                type="button"
                value="Genre Preferences"
                @click="genres_select = true; dialog = true;"
            >

            <div style="margin-top: 10px;">
                <div>
                    <v-btn
                        v-if="!totalAgreeFlag"
                        color="#757575"
                        icon
                        x-small
                        dark
                        @click="totalAgree()"
                    >
                        <span class="mdi mdi-checkbox-blank-circle-outline mdi-18px" />
                    </v-btn>

                    <v-btn
                        v-else
                        type="icon"
                        color="#fc426a"
                        icon
                        x-small
                    >
                        <span class="mdi mdi-checkbox-marked-circle mdi-18px" />
                    </v-btn>

                    <span class="agreement">전체 약관에 동의합니다.</span>
                </div>
                <div>
                    <v-btn
                        v-if="agreeFlag1"
                        type="icon"
                        color="#fc426a"
                        icon
                        x-small
                        @click="agreeFlag1 = !agreeFlag1"
                    >
                        <span class="mdi mdi-checkbox-marked-circle mdi-18px" />
                    </v-btn>

                    <v-btn
                        v-else
                        color="#757575"
                        icon
                        x-small
                        dark
                        @click="agreeFlag1 = !agreeFlag1"
                    >
                        <span class="mdi mdi-checkbox-blank-circle-outline mdi-18px" />
                    </v-btn>

                    <a>유플릭스 이용 약관</a>
                    <span class="agreement">에 동의합니다.</span>
                </div>
                <div>
                    <v-btn
                        v-if="agreeFlag2"
                        type="icon"
                        color="#fc426a"
                        icon
                        x-small
                        @click="agreeFlag2 = !agreeFlag2"
                    >
                        <span class="mdi mdi-checkbox-marked-circle mdi-18px" />
                    </v-btn>

                    <v-btn
                        v-else
                        color="#757575"
                        icon
                        x-small
                        dark
                        @click="agreeFlag2 = !agreeFlag2"
                    >
                        <span class="mdi mdi-checkbox-blank-circle-outline mdi-18px" />
                    </v-btn>

                    <a>유플릭스 서비스 이용 약관</a>
                    <span class="agreement">에 동의합니다.</span>
                </div>
                <div>
                    <v-btn
                        v-if="agreeFlag3"
                        type="icon"
                        color="#fc426a"
                        icon
                        x-small
                        @click="agreeFlag3 = !agreeFlag3"
                    >
                        <span class="mdi mdi-checkbox-marked-circle mdi-18px" />
                    </v-btn>

                    <v-btn
                        v-else
                        color="#757575"
                        icon
                        x-small
                        dark
                        @click="agreeFlag3 = !agreeFlag3"
                    >
                        <span class="mdi mdi-checkbox-blank-circle-outline mdi-18px" />
                    </v-btn>

                    <a>개인정보 취급 방침</a>
                    <span class="agreement">에 동의합니다.</span>
                </div>
                <div>
                    <v-btn
                        v-if="agreeFlag4"
                        type="icon"
                        color="#fc426a"
                        icon
                        x-small
                        @click="agreeFlag4 = !agreeFlag4"
                    >
                        <span class="mdi mdi-checkbox-marked-circle mdi-18px" />
                    </v-btn>

                    <v-btn
                        v-else
                        color="#757575"
                        icon
                        x-small
                        dark
                        @click="agreeFlag4 = !agreeFlag4"
                    >
                        <span class="mdi mdi-checkbox-blank-circle-outline mdi-18px" />
                    </v-btn>

                    <a>신작 알림, 이벤트 정보 수신</a>
                    <span class="agreement">에 동의합니다.</span>
                </div>
            </div>

            <div class="register">
                <input
                    class="register-button"
                    type="button"
                    value="가입 완료"
                    @click="register()"
                >

                <p class="page-payment">
                    결제 정보요? 충분히 둘러보시고 입력해도 늦지 않아요
                </p>
            </div>
        </div>

        <v-row justify="center">
            <v-dialog
                v-model="dialog"
                max-width="1000"
            >
                <v-card>
                    <v-card-title class="headline">
                        Select Genres
                    </v-card-title>
                    <v-divider />
                    <div style="margin: 10px;">
                        <v-row>
                            <v-col
                                v-for="(genre, index) in genres.length"
                                :key="index"
                                cols="12"
                                sm="3"
                                md="3"
                            >
                                <v-checkbox
                                    v-model="selectGenres"
                                    :label="genres[index]"
                                    color="red"
                                    :value="genres[index]"
                                    hide-details
                                />
                            </v-col>
                        </v-row>
                    </div>
                    <v-card-actions>
                        <div class="flex-grow-1" />
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="dialog = !dialog"
                        >
                            OK
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import swal from 'sweetalert';

export default {
    data() {
        return {
            username: '',
            email: '',
            pwd: '',
            totalAgreeFlag: false,
            agreeFlag1: false,
            agreeFlag2: false,
            agreeFlag3: false,
            agreeFlag4: false,
            dialog: false,
            genres_select: false,
            selectGenres: []
        };
    },
    computed: {
        ...mapState({
            genres: (state) => state.infoStore.genres
        })
    },
    watch: {
        agreeFlag1() {
            if (this.agreeFlag1 === false) {
                this.totalAgreeFlag = false;
            } else if (this.agreeFlag1 && this.agreeFlag2 && this.agreeFlag3 && this.agreeFlag4) {
                this.totalAgreeFlag = true;
            }
        },
        agreeFlag2() {
            if (this.agreeFlag2 === false) {
                this.totalAgreeFlag = false;
            } else if (this.agreeFlag1 && this.agreeFlag2 && this.agreeFlag3 && this.agreeFlag4) {
                this.totalAgreeFlag = true;
            }
        },
        agreeFlag3() {
            if (this.agreeFlag3 === false) {
                this.totalAgreeFlag = false;
            } else if (this.agreeFlag1 && this.agreeFlag2 && this.agreeFlag3 && this.agreeFlag4) {
                this.totalAgreeFlag = true;
            }
        },
        agreeFlag4() {
            if (this.agreeFlag4 === false) {
                this.totalAgreeFlag = false;
            } else if (this.agreeFlag1 && this.agreeFlag2 && this.agreeFlag3 && this.agreeFlag4) {
                this.totalAgreeFlag = true;
            }
        }
    },
    methods: {
        ...mapActions('data', ['registerMember']),
        totalAgree() {
            this.totalAgreeFlag = true;
            this.agreeFlag1 = true;
            this.agreeFlag2 = true;
            this.agreeFlag3 = true;
            this.agreeFlag4 = true;
        },
        validityCheck(age, job, gender) {
            if (this.username === '' || this.email === '' || this.pwd === '' || age === '' || job === '' || gender === '') {
                swal({
                    title: 'Warning',
                    text: '모든 값을 입력 해주세요.',
                    icon: 'warning',
                    button: false
                });
                return false;
            }
            const re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;

            if (!re.test(this.email)) {
                swal({
                    title: 'Warning',
                    text: '이메일 양식을 지켜주세요.',
                    icon: 'warning',
                    button: false
                });
                return false;
            }
            if (this.selectGenres.length === 0) {
                swal({
                    title: 'Warning',
                    text: '선호 장르는 하나 이상 선택해주세요.',
                    icon: 'warning',
                    button: false
                });
                return false;
            }
            if (!this.agreeFlag1 || !this.agreeFlag2 || !this.agreeFlag3 || !this.agreeFlag4) {
                swal({
                    title: 'Warning',
                    text: '이용약관에 모두 동의해주세요.',
                    icon: 'warning',
                    button: false
                });
                return false;
            }
            return true;
        },
        register() {
            const ageDocument = document.getElementById('age');
            const ageVal = ageDocument.options[ageDocument.selectedIndex].value;
            const jobDocument = document.getElementById('occupation');
            const jobVal = jobDocument.options[jobDocument.selectedIndex].value;
            const genderDocument = document.getElementById('gender');
            const genderVal = genderDocument.options[genderDocument.selectedIndex].value;

            if (!this.validityCheck(ageVal, jobVal, genderVal)) return;

            const params = {
                email: this.email,
                username: this.username,
                password: this.pwd,
                age: ageVal,
                gender: genderVal,
                occupation: jobVal,
                genres: this.selectGenres
            };
            this.$log.debug('Register.vue', params);
            this.registerMember(params).then((ret) => {
                if (ret.statusText === 'Created') {
                    swal({
                        title: 'Success',
                        text: '회원가입을 성공하였습니다.',
                        icon: 'success'
                    }).then(() => {
                        window.location = '/login';
                    });
                } else {
                    swal({
                        title: 'Fail',
                        text: '회원가입을 실패했습니다. 관리자에게 문의하세요.',
                        icon: 'warning',
                        button: false
                    });
                }
            });
        }
    }
};
</script>

<style lang="scss" scoped>
input {
  color: black;
}

#loginForm-setting {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 300px;
  -khtml-transform: translate(-50%, -50%);
  -moz-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  -o-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}

.input-title {
  font-size: 18px;
  margin-bottom: 14px;
  letter-spacing: -1px;
  font-weight: 300;
}

#background-img {
  background: url("../../assets/img/chernobyl.jpg") no-repeat center center;
  background-color: #121218;
  opacity: 0.22;

  height: 100%;
  background-size: cover;
}

#background-cover {
  background: #121218;
  position: relative;
  height: 100vh;
  overflow-x: hidden;

  -webkit-font-smoothing: antialiased;
}

.input-setting {
  position: relative;
  display: block;
  border-bottom: 1px solid rgba(154, 151, 161, 0.2);
  width: 300px;
  height: 46px;
  line-height: 24px;
  padding: 10px 14px;
  padding-right: 42px;
  background-color: #ffffff;
}

.input-top-radius {
  border-top-right-radius: 4px;
  border-top-left-radius: 4px;
}

.select-setting {
  margin: 0px;

  position: relative;
  display: block;
  border-bottom: 1px solid rgba(154, 151, 161, 0.2);
  width: 300px;
  height: 46px;
  line-height: 24px;
  padding: 10px 14px;
  padding-right: 42px;
  background-color: #ffffff;
}

.input-bottom-radius {
  border-bottom-right-radius: 4px;
  border-bottom-left-radius: 4px;
}

select {
  color: #757575;
}

option {
  color: black;
}

.agreement {
  opacity: 0.5;
  font-size: 12px;
}

.checkbox {
  margin: 0px;
}

.register {
  color: white;
}

.register-button {
  display: inline-block;
  position: relative;
  text-align: center;

  border-radius: 40px;
  margin-top: 16px;
  background-color: #fc426a;
  color: #ffffff;
  width: 300px;
  height: 48px;
  line-height: 48px;
  margin-bottom: 14px;
  font-size: 18px;
}

.page-payment {
  opacity: 0.5;

  text-align: center;
  font-size: 12px;
  letter-spacing: -0.5px;
}

a {
  text-decoration: none;
  color: #ffffff;
  font-size: 12px;

  opacity: 0.7;
}

a:hover {
  text-decoration: underline;
}

.v-application a {
  color: white;
}

a:visited a:link {
  text-decoration: none;
  color: white;
}
</style>
