<template>
    <div class="sign-in-page">
        <div class="sign-in-page__centerer">
            <div class="sign-in-page__label">
                <span id="login__label">로그인</span>
                <router-link to="/loginhelp">
                    <a class="sign-in-page__password">도움이 필요하신가요?</a>
                </router-link>
            </div>

            <div class="sign-in-page__form">
                <div class="sign-in-page__input-group">
                    <label class="sign-input">
                        <input
                            id="userId"
                            v-model="userId"
                            type="email"
                            required
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
                            id="userPassword"
                            v-model="password"
                            type="password"
                            required
                            placeholder="비밀번호 (6자 이상)"
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
                </div>

                <div v-if="idCheck == 1 && passwordCheck == 1">
                    <input
                        class="sign-in-page__submit"
                        type="button"
                        value="LOGIN"
                        @click="userLogin()"
                    >
                </div>
                <div v-else>
                    <input
                        class="sign-in-page__submit"
                        type="button"
                        value="LOGIN"
                        style="opacity: 0.3"
                        disabled
                    >
                </div>
                <div class="sign-in-page__divider" />

                <p class="sign-in-page__fb-joined">
                    이전에 Facebook, Google으로 가입하셨나요?
                </p>

                <a
                    class="sign-in-page__facebook"
                    @click="alert()"
                >
                    <div class="btn-icon">
                        <span class="mdi mdi-facebook-box mdi-24px" />
                    </div>

                    <div style="width: 80%; display:inline-block">
                        <span>
                            Facebook으로 로그인
                        </span>
                    </div>
                </a><br>

                <a
                    class="sign-in-page__google"
                    @click="alert()"
                >
                    <div class="btn-icon">
                        <span class="mdi mdi-google-plus mdi-24px" />
                    </div>

                    <div
                        style="width: 80%; display:inline-block"
                    >
                        <span>
                            Google로 로그인
                        </span>
                    </div>
                </a><br>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex';
import swal from 'sweetalert';

export default {
    data() {
        return {
            userId: '',
            password: '',
            idCheck: 0,
            passwordCheck: 0
        };
    },
    watch: {

        userId() {
            if (this.userId === undefined || this.userId.length === 0) {
                this.idCheck = 0;
                return;
            }
            const re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;

            if (!re.test(this.userId)) {
                this.idCheck = -1;
                return;
            }
            this.idCheck = 1;
        },

        password() {
            if (this.password === undefined || this.password.length === 0) {
                this.passwordCheck = 0;
                return;
            }

            if (this.password.length < 6) {
                this.passwordCheck = -1;
                return;
            }
            this.passwordCheck = 1;
        }
    },
    methods: {
        ...mapActions('data', ['login']),
        ...mapActions(['commingSoon']),

        userLogin() {
            document.getElementById('userId').disabled = true;
            document.getElementById('userPassword').disabled = true;
            this.login({ email: this.userId, password: this.password }).then((ret) => {
                if (ret === true) {
                    swal({
                        title: '로그인 성공',
                        text: 'Welcome To YOUFLIX!',
                        icon: 'success',
                        button: false
                    }).then(() => {
                        this.$router.push('/home');
                    });
                } else {
                    swal({
                        title: '로그인 실패',
                        text: '이메일이나 비밀번호가 맞지 않습니다.',
                        icon: 'error',
                        button: false
                    });
                    document.getElementById('userId').disabled = false;
                    document.getElementById('userPassword').disabled = false;
                }
            });
        },
        alert() {
            this.commingSoon();
        }
    }
};
</script>

<style scoped>

div {

    display: block;
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

.sign-in-page {
    height: 100vh;
    background: url("../../assets/img/chernobyl.jpg") no-repeat center center;
    position: relative;
    background-size: cover;
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

#login__label {

    color: white;
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

.sign-in-page__facebook {
    color: #ffffff;
    background-color: #4065b3;
    display: inline-block;
    position: relative;
    text-align: center;
    -webkit-border-radius: 40px;
    -khtml-border-radius: 40px;
    -moz-border-radius: 40px;
    -ms-border-radius: 40px;
    -o-border-radius: 40px;
    border-radius: 40px;
    width: 300px;
    height: 52px;
    line-height: 52px;
    font-size: 15px;
    margin-bottom: 15px;
}

.sign-in-page__google {
    color: #ffffff;
    background-color: #FF3376;
    display: inline-block;
    position: relative;
    text-align: center;
    -webkit-border-radius: 40px;
    -khtml-border-radius: 40px;
    -moz-border-radius: 40px;
    -ms-border-radius: 40px;
    -o-border-radius: 40px;
    border-radius: 40px;
    width: 300px;
    height: 52px;
    line-height: 52px;
    font-size: 15px;
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
