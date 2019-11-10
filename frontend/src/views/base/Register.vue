<template>
    <div id="background-cover">
        <div id="background-img" />
        <div id="loginForm-setting">
            <div class="input-title white--text">
                회원가입
            </div>
            <div class="sign-in-page__input-group">
                <label class="sign-input">
                    <input
                        id="username"
                        v-model="username"
                        type="text"
                        placeholder="닉네임 (2-10자, 영어,한글,숫자)"
                    >
                    <i
                        v-if="nickNameCheck == -1"
                        class="mdi mdi-close-circle-outline mdi-24px fail-icon"
                    />
                    <i
                        v-else-if="nickNameCheck == 1"
                        class="mdi mdi-check-circle-outline mdi-24px success-icon"
                    />
                </label>
                <label class="sign-input">
                    <input
                        id="email"
                        v-model="email"
                        type="email"
                        placeholder="이메일 (example@gmail.com)"
                    >
                    <i
                        v-if="idCheck == -1"
                        class="mdi mdi-close-circle-outline mdi-24px fail-icon"
                    />
                    <i
                        v-else-if="idCheck == 1"
                        class="mdi mdi-check-circle-outline mdi-24px success-icon"
                    />
                </label>

                <label class="sign-input">
                    <input
                        id="pwd"
                        v-model="pwd"
                        type="password"
                        placeholder="비밀번호 (6-30자, 영어,숫자,특수문자)"
                    >
                    <i
                        v-if="passwordCheck == -1"
                        class="mdi mdi-close-circle-outline mdi-24px fail-icon"
                    />
                    <i
                        v-else-if="passwordCheck == 1"
                        class="mdi mdi-check-circle-outline mdi-24px success-icon"
                    />
                </label>

                <label class="sign-input">
                    <select
                        id="age"
                        v-model="age"
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
                    <i
                        v-if="ageCheck == -1"
                        class="mdi mdi-close-circle-outline mdi-24px fail-icon"
                    />
                    <i
                        v-else-if="ageCheck == 1"
                        class="mdi mdi-check-circle-outline mdi-24px success-icon"
                    />
                </label>

                <label class="sign-input">
                    <select
                        id="gender"
                        v-model="gender"
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
                    <i
                        v-if="genderCheck == -1"
                        class="mdi mdi-close-circle-outline mdi-24px fail-icon"
                    />
                    <i
                        v-else-if="genderCheck == 1"
                        class="mdi mdi-check-circle-outline mdi-24px success-icon"
                    />
                </label>

                <label class="sign-input">
                    <select
                        id="occupation"
                        v-model="occupation"
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
                    <i
                        v-if="occupationCheck == -1"
                        class="mdi mdi-close-circle-outline mdi-24px fail-icon"
                    />
                    <i
                        v-else-if="occupationCheck == 1"
                        class="mdi mdi-check-circle-outline mdi-24px success-icon"
                    />
                </label>
                <label class="sign-input">
                    <input
                        class="#a4a4a4--text"
                        type="button"
                        value="Genre Preferences"
                        @click="genres_select = true; dialog = true;"
                    >
                    <i
                        v-if="genresCheck == -1"
                        class="mdi mdi-close-circle-outline mdi-24px fail-icon"
                    />
                    <i
                        v-else-if="genresCheck == 1"
                        class="mdi mdi-check-circle-outline mdi-24px success-icon"
                    />
                </label>
            </div>

            <div
                class="white--text"
                style="margin-top: 10px;"
            >
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

                    <a @click="agreeFlag1 = true">유플릭스 이용 약관</a>
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

                    <a @click="agreeFlag2 = true">유플릭스 서비스 이용 약관</a>
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

                    <a @click="agreeFlag3 = true">개인정보 취급 방침</a>
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

                    <a @click="agreeFlag4 = true">신작 알림, 이벤트 정보 수신</a>
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
                    평가정보요? 충분히 둘러보시고 입력해도 늦지 않아요
                </p>
            </div>

            <v-row
                justify="center"
            >
                <v-dialog
                    v-model="dialog"
                    max-width="1000"
                    justify="center"
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
    </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';
import swal from 'sweetalert';

const { mapActions } = createNamespacedHelpers('users');
const infoMapState = createNamespacedHelpers('infos').mapState;

export default {
    data() {
        return {
            username: '',
            email: '',
            pwd: '',
            age: '',
            gender: '',
            occupation: '',
            selectGenres: [],

            totalAgreeFlag: false,
            agreeFlag1: false,
            agreeFlag2: false,
            agreeFlag3: false,
            agreeFlag4: false,
            dialog: false,
            genres_select: false,

            nickNameCheck: 0,
            idCheck: 0,
            passwordCheck: 0,
            ageCheck: 0,
            genderCheck: 0,
            occupationCheck: 0,
            genresCheck: 0
        };
    },
    computed: {
        ...infoMapState({
            genres: (state) => state.genres
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
        },
        username() {
            if (this.username === undefined || this.username.length === 0) {
                this.nickNameCheck = 0;
                return;
            }
            const re = /^[가-힣a-zA-Z0-9]+$/;

            if (!re.test(this.username) || this.username.length < 2 || this.username.length > 10) {
                this.nickNameCheck = -1;
                return;
            }
            this.nickNameCheck = 1;
        },
        email() {
            if (this.email === undefined || this.email.length === 0) {
                this.idCheck = 0;
                return;
            }
            const re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;

            if (!re.test(this.email)) {
                this.idCheck = -1;
                return;
            }
            this.idCheck = 1;
        },
        pwd() {
            if (this.pwd === undefined || this.pwd.length === 0) {
                this.passwordCheck = 0;
                return;
            }

            if (this.pwd.length < 6) {
                this.passwordCheck = -1;
                return;
            }
            this.passwordCheck = 1;
        },
        age() {
            if (this.age.length === 0) {
                this.ageCheck = -1;
                return;
            }
            this.ageCheck = 1;
        },
        gender() {
            if (this.gender.length === 0) {
                this.genderCheck = -1;
                return;
            }
            this.genderCheck = 1;
        },
        occupation() {
            if (this.occupation.length === 0) {
                this.occupationCheck = -1;
                return;
            }
            this.occupationCheck = 1;
        },
        selectGenres() {
            if (this.selectGenres.length === 0) {
                this.genresCheck = -1;
                return;
            }
            this.genresCheck = 1;
        }
    },
    mounted() {
        this.username = '';
        this.email = '';
        this.pwd = '';
        this.age = '';
        this.gender = '';
        this.occupation = '';
        this.selectGenres = [];
    },
    methods: {
        ...mapActions(['registerMember', 'checkDuplicateEmail']),
        totalAgree() {
            this.totalAgreeFlag = true;
            this.agreeFlag1 = true;
            this.agreeFlag2 = true;
            this.agreeFlag3 = true;
            this.agreeFlag4 = true;
        },
        validityCheck() {
            if (this.username === '' || this.email === '' || this.pwd === '' || this.age === '' || this.occupation === '' || this.gender === '') {
                swal({
                    title: 'Warning',
                    text: '모든 값을 입력 해주세요.',
                    icon: 'warning',
                    button: false
                });
                this.idCheck = -1;
                return false;
            }
            if (!this.checkDuplicateEmail(this.email).then((ret) => {
                if (ret) {
                    swal({
                        title: 'Warning',
                        text: '이미 가입되어 있는 이메일 입니다.',
                        icon: 'warning',
                        button: false
                    });
                    return false;
                }
                return true;
            })) return false;
            if (this.username.length < 2 || this.username > 10) {
                swal({
                    title: 'Warning',
                    text: '이름의 글자 수는 최소2자 최대 10자입니다.',
                    icon: 'warning',
                    button: false
                });
                return false;
            }
            if (!(/^[a-zA-Z0-9!@#$%^&*]*$/).test(this.pwd) || this.pwd.length < 6 || this.pwd.length > 30) {
                swal({
                    title: 'Warning',
                    text: '비밀번호는 영어, 숫자, 특수문자(!@#$%^&*) 조합만 가능합니다.',
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
            if (!this.validityCheck()) return;

            const params = {
                email: this.email,
                username: this.username,
                password: this.pwd,
                age: this.age,
                gender: this.gender,
                occupation: this.occupation,
                genres: this.selectGenres
            };
            this.$log.debug('Register.vue', params);
            this.registerMember(params).then((ret) => {
                if (ret) {
                    swal({
                        title: 'Success',
                        text: '회원가입을 성공하였습니다.',
                        icon: 'success',
                        button: false
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

@import '@/style/variables.scss';

input {
  color: black;
}

select {
  color: black;
  width: 90%;
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
  background: url("/static/img/chernobyl.jpg") no-repeat center center;
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

input {

    outline-width: 0;
}

p {
    margin: 0;
    padding: 0;
}

.success-icon {

    color: lightgreen;
    float: right;
}

.fail-icon {

    color: lightcoral;
    float: right;
}

.sign-in-page:after {
    content: "";
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: #121218;
    opacity: 0.8;
}

.sign-in-page__centerer {
    position: absolute;
    top: 50%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    -khtml-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    z-index: 100;
}

.sign-in-page__label {
    font-size: 18px;
    margin-bottom: 14px;
    letter-spacing: -1px;
}

.sign-in-page__password {
    opacity: 0.5;
    filter: alpha(opacity=50);
    float: right;
    padding-top: 4px;
    font-size: 12px;
    color: #ffffff;
}

.sign-input {
    position: relative;
    display: block;
    border-bottom: 1px solid rgba(154,151,161,0.2);
    width: 300px;
    height: 46px;
    line-height: 24px;
    padding: 10px 14px;
    background-color: #ffffff;
}

.sign-input:first-child {
    border-top-right-radius: 4px;
    border-top-left-radius: 4px;
}

.sign-input:last-child {
    border-bottom-right-radius: 4px;
    border-bottom-left-radius: 4px;
}

.sign-input>input {
    width: 90%;
    color: #121218;
    font-size: 16px;
    letter-spacing: -.5px;
}

.sign-in-page .sign-in-page__centerer .sign-in-page__submit {
    display: inline-block;
    position: relative;
    text-align: center;
    -webkit-border-radius: 40px;
    -khtml-border-radius: 40px;
    -moz-border-radius: 40px;
    -ms-border-radius: 40px;
    -o-border-radius: 40px;
    border-radius: 40px;
    margin-top: 16px;
    background-color: #fc426a;
    color: #ffffff;
    width: 300px;
    height: 48px;
    line-height: 48px;
    margin-bottom: 21px;
    font-size: 18px;
}

.btn-icon {
    width: 20%;
    text-align: right;
    vertical-align: middle;
    display:inline-block;
}

.sign-in-page .sign-in-page__centerer .sign-in-page__divider {
    display: block;
    width: 300px;
    height: 1px;
    background-color: rgba(154,151,161,0.2);
    margin: 0 auto 15px;
}

.sign-in-page .sign-in-page__centerer .sign-in-page__fb-joined {
    margin-bottom: 13px;
    color: #d5d4d7;
    font-size: 12px;
    letter-spacing: -.5px;
}

</style>
