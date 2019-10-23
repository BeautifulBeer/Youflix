<template>
    <div class="text-center">
        <v-dialog
            v-model="dialog"
            width="500"
        >
            <v-card>
                <v-card-text>
                    신작, 인기, 추천 콘텐츠 안내 및 이벤트, 마케팅 정보 안내 등을 주 목적으로 하며 수신 동의 시 메일, 문자 메시지, 푸시 알림에 수신 동의 처리 됩니다. 동의하지 않으셔도 서비스 이용이 가능하며 동의하신 이후에도 정보 수신 시 안내에 따라 수신 동의를 철회할 수 있습니다.
                </v-card-text>
                <v-card-actions>
                    <v-btn
                        color="primary"
                        text
                        @click="dialog = false"
                    >
                        I accept
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
export default {

    props: {
        dialog: { type: Boolean, default: false }
    }
};
</script>
