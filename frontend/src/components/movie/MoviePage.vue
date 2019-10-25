<template>
    <div v-show="isActive">
        <input
            id="button"
            type="checkbox"
        >
        <label for="button">YOUFLEX</label>
        <div class="modal">
            <div class="content">
                Pure CSS Modal! No JS!
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MoviePage',
    computed: {
        isActive() {
            return this.$store.state.movieVisible;
        }
    },
    watch: {
        isActive(newVal) {
            document.getElementById('button').checked = newVal;
        }
    }
};
</script>

<style lang="scss" scoped>
.modal {
    background: dodgerblue;
    height: 1px;
    overflow: hidden;
    position: fixed;
    top: 50%;
    left: 50%;
    z-index: 1000;
    transform: translate(-50%, -50%);
    transition: width 0.5s ease 0.5s,
                height 0.5s ease;
    width: 0;
}

.content {
    color: transparent;
    font-family: 'Consolas', arial, sans-serif;
    font-size: 2em;
    position: absolute;
    top: 50%;
    text-align: center;
    transform: translate3d(0,-50%,0);
    transition: color 0.5s ease;
    width: 100%;
}

label {
    color: dodgerblue;
    cursor: pointer;
    font-family: 'Consolas', arial, sans-serif;
    font-size: 2em;
    position: fixed;
    left: 50%;
    top: 50%;
    text-transform: uppercase;
    transform: translate(-50%, -50%);
    transition: color 0.5s ease 0.5s;
}

input {
    cursor: pointer;
    height: 0;
    opacity: 0;
    width: 0;

    &:focus {
        outline: none;
    }
}

input:checked {
    height: 40px;
    opacity: 1;
    position: fixed;
    right: 20px;
    top: 20px;
    z-index: 2001;
    -webkit-appearance: none;
    width: 40px;

    &::after,
    &:before {
        border-top: 1px solid #FFF;
        content: '';
        display: block;
        position: absolute;
        top: 50%;
        transform: rotate(45deg);
        width: 100%;
    }

    &::after {
        transform: rotate(-45deg);
    }
}

input:checked + label {
    color: #FFF;
    transition: color 0.5s ease;
}

input:checked ~ .modal {
    height: 100%;
    width: 100%;
    transition: width 0.5s ease,
                height 0.5s ease 0.5s;
    .content {
    color: #FFF;
    transition: color 0.5s ease 0.5s;
    }
}
</style>
