<template>
    <!-- <div class="flex-grow-1" /> -->
    <v-app id="inspire">
    <v-container>
        <v-text-field
            v-model="model"
            :counter="max"
            :rules="rules"
            label="Training Name"
        ></v-text-field>
        <fieldset>
            <legend>Hyper Parameter</legend>
            <br/>
            
            - Learning Rate
            <v-flex xs6>
                <v-slider thumb-label 
                    v-model="max"
                >
                </v-slider>
            </v-flex>
            
            - Epoch
            <v-slider
            v-model="max">
            </v-slider>
            
            - Regular Term
            <v-slider
            v-model="max">
            </v-slider>
        </fieldset>
        <br/><br/>

        <fieldset>
            <legend>Test 비율</legend>
                <v-flex xs8>
                    <v-slider thumb-label
                        v-model="testAndTraining.val"
                        :color="testAndTraining.color"
                        :label="testAndTraining.label">
                    </v-slider>
                </v-flex>

                <v-flex>알고리즘 선택
                    <v-row align="center">
                        <v-col class="d-flex" cols="12" sm="6">
                        <v-select
                            :items="items"
                            label="Outlined style"
                            outlined
                        ></v-select>
                        </v-col>
                    </v-row>
                </v-flex>

                <v-flex>Recommend System
                    <v-row align="center">
                        <v-col class="d-flex" cols="12" sm="6">
                        <v-select
                            :items="items"
                            label="Outlined style"
                            outlined
                        ></v-select>
                        </v-col>
                    </v-row>
                </v-flex>
        </fieldset>
    </v-container>
  </v-app>
</template>

<script>

export default {
    data() {
        return {
            testAndTraining: { label: '테스트/트레이닝 비율', val: 25, color: 'red' },
            items: ['1', '2', '3', '4'],
        }
    }
}
</script>


<style scoped>
    .container{
        margin-top: 50px;
        margin-left: 30px;
    }
</style>