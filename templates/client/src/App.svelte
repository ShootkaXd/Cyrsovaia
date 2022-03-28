<script>
	import LoginForm from "./LoginForm.svelte";
	import Notes from "./Notes.svelte";
	import {getCookie} from "./storage";

	let userId = getCookie('auth');
	$:{
		console.log(getCookie('auth'))
	}
</script>

<main>
	{#if !userId}
		<LoginForm></LoginForm>
	{:else}
		<Notes></Notes>
	{/if}
</main>

<style>
	
</style>