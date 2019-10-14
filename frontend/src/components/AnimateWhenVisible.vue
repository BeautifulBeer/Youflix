<template>
    <div>
        <transition
            :name="name"
            :appear="appear"
        >
            <div
                v-if="isVisible"
                :style="{ animationDuration: `${duration}s`, transitionDuration: `${duration}s` }"
            >
                <slot />
            </div>
        </transition>
    </div>
</template>

<script>
let isPassiveSupported = false;

try {
    const options = Object.defineProperty({}, 'passive', {
        get: () => {
            isPassiveSupported = true;
            return isPassiveSupported;
        },
    });

    window.addEventListener('test', null, options);
} catch (err) {
    console.log(err); // eslint-disable-line no-console
}

export default {
    name: 'AnimateWhenVisible',
    props: {
        name: String,
        appear: { type: Boolean, default: false },
        offsetTop: { type: Number, default: 0 },
        duration: { type: Number, default: 1 },
        updatedFlag: { type: Boolean, default: true },
    },
    data: () => ({
        isVisible: false,
    }),
    watch: {
        updatedFlag(newVal, oldVal) {
            if (oldVal && !newVal) {
                this.isVisible = false;
            } else if (!oldVal && newVal) {
                this.isVisible = true;
            }
        },
    },
    mounted() {
        this.$nextTick(this.detectVisibility);
        window.addEventListener('scroll', this.detectVisibility, isPassiveSupported ? { passive: true } : false);
        window.addEventListener('resize', this.detectVisibility, isPassiveSupported ? { passive: true } : false);
        window.addEventListener('orientationchange', this.detectVisibility, isPassiveSupported ? { passive: true } : false);
    },
    destroyed() {
        window.removeEventListener('scroll', this.detectVisibility);
        window.removeEventListener('resize', this.detectVisibility);
        window.removeEventListener('orientationchange', this.detectVisibility);
    },
    methods: {
        inViewport() {
            const rect = this.$el.getBoundingClientRect();
            return rect.top <= (window.innerHeight - this.offsetTop) && rect.left <= window.innerWidth;
        },
        detectVisibility() {
            this.isVisible = this.inViewport();
        },
    },
};
</script>
