<template>
    <div>
        <v-img
            src="/static/img/loginHelp.jpg"
            style="height: 100vh;"
        >
            <v-card
                id="content"
                width="480"
                height="550"
                class="mx-auto"
            >
                <v-card-title class="display-1 sub-content">
                    이메일/비밀번호를
                    <br>잊으셨나요?
                </v-card-title>
                <div class="text--primary subtitle-1 sub-content">
                    비밀번호 재설정 안내를 받을 방법을 선택하세요.
                </div>
                <div
                    id="radioBox"
                    class="text--primary"
                >
                    <v-radio-group
                        v-model="radios"
                        :mandatory="false"
                    >
                        <v-radio
                            label="이메일 주소"
                            value="email"
                        />
                        <v-radio
                            label="카카오톡 메세지"
                            value="kakaotalk"
                        />
                        <v-radio
                            label="챗봇 메세지"
                            value="chatbot"
                        />
                    </v-radio-group>
                </div>
                <div class="text--primary subtitle-1 sub-content">
                    비밀번호 재설정 안내 이메일을 보내드리겠습니다.
                </div>
                <v-text-field
                    placeholder="name@example.com"
                    solo
                />
                <div>
                    <v-btn
                        width="100%"
                        height="50"
                        color="#2490FD"
                        dark
                    >
                        SEND
                    </v-btn>
                </div>
            </v-card>
        </v-img>
    </div>
</template>

<script>
export default {
    data() {
        return {
            radios: 'email'
        };
    }
};
</script>

<style scoped>
#content {
  margin-top: 150px;
  padding: 40px;
}

.sub-content {
  padding: 0px;
  margin-top: 10px;
  margin-left: 0px;
  margin-right: 0px;
  margin-bottom: 10px;
}

#radioBox {
  margin: 20px;
}
</style>
