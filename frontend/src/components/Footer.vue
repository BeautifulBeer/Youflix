<template>
    <v-container
        fluid
        class="footer-wapper"
    >
        <v-row justify="center">
            <v-col
                sm="12"
                md="3"
            >
                <v-row justify="center">
                    <v-col cols="9">
                        <v-row class="icon-row">
                            <v-col>
                                <i class="fa fa-facebook-square fa-2x" />
                            </v-col>
                            <v-col>
                                <i class="fa fa-instagram fa-2x" />
                            </v-col>
                            <v-col>
                                <i class="fa fa-twitter fa-2x" />
                            </v-col>
                            <v-col>
                                <i class="fa fa-youtube-square fa-2x" />
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                <v-row justify="center">
                    <v-col cols="9">
                        자막 및 음성
                    </v-col>
                    <v-col cols="9">
                        미디어센터
                    </v-col>
                    <v-col cols="9">
                        개인정보
                    </v-col>
                    <v-col cols="9">
                        문의하기
                    </v-col>
                </v-row>
            </v-col>
            <v-col
                sm="12"
                md="3"
            >
                <v-row justify="center">
                    <v-col
                        cols="9"
                        style="height: 92px;"
                    />
                    <v-col cols="9">
                        음성 지원
                    </v-col>
                    <v-col cols="9">
                        투자 정보(IR)
                    </v-col>
                    <v-col cols="9">
                        법적 고지
                    </v-col>
                </v-row>
            </v-col>
            <v-col
                sm="12"
                md="3"
            >
                <v-row justify="center">
                    <v-col
                        cols="9"
                        style="height: 92px;"
                    />
                    <v-col cols="9">
                        고객 센터
                    </v-col>
                    <v-col cols="9">
                        입사 정보
                    </v-col>
                    <v-col cols="9">
                        쿠키 설정
                    </v-col>
                </v-row>
            </v-col>
            <v-col
                sm="12"
                md="3"
            >
                <v-row justify="center">
                    <v-col
                        cols="9"
                        style="height: 92px;"
                    />
                    <v-col cols="9">
                        기프트카드
                    </v-col>
                    <v-col cols="9">
                        이용 약관
                    </v-col>
                    <v-col cols="9">
                        회사 설정
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
        <v-row justify="start">
            <v-col
                sm="12"
                md="3"
            >
                <v-row justify="center">
                    <v-col cols="9">
                        <span class="service-code">서비스 코드</span>
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col style="text-align:center;">
                <span>유플릭스서비시스코리아 유한회사 통신판매업신고번호: 제2019-구미인동-0426호 전화번호: 00-308-321-0058</span>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {

};
</script>

<style lang="scss" scoped>
@import '@/style/variables.scss';

.footer-wapper{
    min-height: 400px;
    margin: 20px;
    color: $text-color;

    .icon-row{
        justify: space-between;
    }

    .fa-facebook-square, .fa-instagram , .fa-youtube-square, .fa-twitter{
        color: $text-color;
        background-color: $background-color;
    }

    .service-code{
        border: 1px solid white;
        box-sizing: border-box;
        padding: 10px;
    }
}

</style>
