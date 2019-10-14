<template>
    <v-toolbar>
        <v-toolbar-title>
            <v-icon>mdi-settings</v-icon> <font
                size="5"
                bold
            >
                ADMIN PAGE
            </font>
        </v-toolbar-title>

        <div class="flex-grow-1" />

        <template v-if="$vuetify.breakpoint.smAndUp">
            <v-btn to="/adminPage/dashboard">
                <i class="material-icons">dashboard</i>
                DashBoard
            </v-btn>
            <v-btn to="/adminPage/userlist">
                <v-icon>people</v-icon>
                User List
            </v-btn>
            <v-btn to="/adminPage/movielist">
                <v-icon>movie</v-icon>
                Movie List
            </v-btn>
        </template>
    </v-toolbar>
</template>

<script>
export default {};
</script>

<style scoped>
* {
  font-family: 'Oswald', sans-serif;
}
</style>
