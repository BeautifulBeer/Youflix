<template>
        <v-row class="grey lighten-5 justify-center mx-3">
        <v-flex xs12 md6 sm6>
            <fieldset>
                <legend align="center">Page Test1</legend>
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
             </fieldset>
        </v-flex>
        <v-flex  xs12 md6 sm6>
            <fieldset>
                <legend align="center">Page Test2</legend>
                    <v-radio-group row class="justify-center" v-model="method">
                        <v-radio label="Test1" color="error" value="test1"/>
                        <v-radio label="Test2" color="success" value="test2"/>
                        <v-radio label="Test3" color="info" value="test3"/>
                    </v-radio-group>
                    <v-col class="pr-4" col-4>
                        <v-slider thumb-label 
                                v-model="slider2"
                                class="align-center"
                                :max="max"
                                :min="min"
                                hide-detail
                    >
                        <template v-slot:append>
                            <v-text-field
                                    v-model="slider2"
                                    class="mt-0 pt-0"
                                    hide-details
                                    single-line
                                    type="number"
                                    style="width: 60px"
                            />
                         </template>
                    </v-slider>
                 </v-col>
             </fieldset>
        </v-flex>
        <v-flex xs12 md12 sm12>
            <v-card>
                <basicLine></basicLine>
            </v-card>
        </v-flex>
        </v-row>
</template>

<script>
import BasicLine from './lineChart.vue';

export default {
    components: {
        BasicLine,
    },
    data() {
        return {
            min: 1,
            max: 100,
            slider: 20,
            slider2:10,
            method: 'Test1',
        }
    }
}
</script>