<template>
    <div id="content">
        <AdminHeader />
        <router-view />
    </div>
</template>

<script>
import AdminHeader from '../../components/admin/AdminHeader.vue';

export default {

    components: {

        AdminHeader,
    },
};
</script>

<style scoped>

    #content {

        height: 100%;

        margin-top: 90px;
        margin-left: 14px;
        margin-right: 14px;
        margin-bottom: 14px;
        background-color: ghostwhite;
    }

</style>
