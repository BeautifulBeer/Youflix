<template>
    <div class="wrapper">
        <div class="loader">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
        </div>
    </div>
</template>

<style lang="scss" scoped>

$base-duration: 500ms;

// Colors
$color-1: #2c3e50;
$color-2: #3498db;
$color-3: #2ecc71;

// Breakpoints
$sm: new-breakpoint(min-width 320px);
$med: new-breakpoint(min-width 768px);
$lg: new-breakpoint(min-width 1024px);

*, *:before, *:after {
	box-sizing: border-box;
	outline: none;
}

.wrapper {
	position: absolute;
	display: flex;
	align-items: center;
	justify-content: center;
    top: 0;
    left: 0;
	width: 100vw;
	height: 100vh;
    z-index: 1000;
	background-color:darken($color-1, 4%);
    opacity: 0.9;
}

.loader {
	position: relative;
	display: grid;
	grid-template-columns: 33% 33% 33%;
	grid-gap: 2px;
	width: 100px;
	height: 100px;
	
	> div {
		position: relative;
		width: 100%;
		height: 100%;
		background: tomato;
		transform: scale(0.0);
		transform-origin: center center;
		animation: loader 2s infinite linear;
		
		&:nth-of-type(7) {}
		
		&:nth-of-type(1),
		&:nth-of-type(5), 
		&:nth-of-type(9) {
			animation-delay: 0.4s;
		}
		
		&:nth-of-type(4),
		&:nth-of-type(8) {
			animation-delay: 0.2s;
		}
		
		&:nth-of-type(2),
		&:nth-of-type(6) {
			animation-delay: 0.6s;
		}
		
		&:nth-of-type(3) {
			animation-delay: 0.8s;
		}
	}
}

@keyframes loader {
	0%   { transform: scale(0.0); }
	40%  { transform: scale(1.0); }
	80%  { transform: scale(1.0); }
	100% { transform: scale(0.0); }
}
</style>