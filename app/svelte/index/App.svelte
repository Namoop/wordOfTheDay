<script lang="ts">
	let posts = document.data.posts as Posts[]
</script>

<main class="flex flex-col items-center justify-center w-screen bg-neutral-900 text-white py-40">
	<div class="p-10 border border-red-500 rounded-lg hover:bg-black w-5/6">
		<h1 class="text-3xl text-red-500 font-bold tracking-tight text-center mb-5">
			Wordgrid Daily Word
		</h1>
		<p class="mb-2">
			Below is a daily word that you can use to improve your vocabulary.
			It may or may not happen to meet some conditions for a certain
			<a href="https://wordgrid.clevergoat.com" class="hover:text-blue-600 active:text-red-600 text-blue-400 ">wordgrid</a> game.
		</p>
	</div>

	<div class="h-10"></div>

	<div class="p-10 border border-red-500 rounded-lg w-5/6">
		<h1 class="text-3xl text-red-500 font-bold tracking-tight text-center mb-5">
			Posts
		</h1>
		{#each posts.reverse() as post}
			<div class="p-5 hover:bg-black rounded-lg whitespace-pre-wrap">
				<h2 class="text-2xl text-red-500 font-bold tracking-tight text-center mb-5">
					{post.title}
				</h2>
				<p class="mb-2">
					{post.content}
				</p>
				<p class="text-xs">
					{post.created}
				</p>
				<a class="text-xs" href='mailto:{post.author_email}'>
					{post.author}
				</a>
			</div>
		{/each}
	</div>
</main>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>
