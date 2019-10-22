<template>
    <v-layout wrap col-6 class="grey lighten-5">
        <v-flex >
            <v-radio-group row class="justify-center" v-model="method">
                <v-radio label="Test1" color="error" value="test1"/>
                <v-radio label="Test2" color="success" value="test2"/>
                <v-radio label="Test3" color="info" value="test3"/>
            </v-radio-group>
            <v-col class="pr-4" col-4>
            <v-slider thumb-label 
                        v-model="slider"
                        class="align-center"
                        :max="max"
                        :min="min"
                        hide-detail
                >

                <template v-slot:append>
                    <v-text-field
                        v-model="slider"
                        class="mt-0 pt-0"
                        hide-details
                        single-line
                        type="number"
                        style="width: 60px"
                    />
                </template>
            </v-slider>
            </v-col>
        </v-flex>
    </v-layout>
</template>

<script>
export default {
    data() {
        return {
            min: 1,
            max: 100,
            slider:20,
            method: 'Test1',
        }
    }
}
</script>