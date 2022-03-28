<script>
    function getAllNotes() {
        fetch('/notes').then(res => {
            if (res.ok)
                return res.json()
            return []
        }).then(data => notes = data)
    }
    function post(){
        fetch("/notes", {
            headers: {"Content-Type": "application/json"},
            "body": JSON.stringify({note: noteText}),
            "method": "POST",
        }).then(response => {
            if (response.ok) {
                getAllNotes()
                return;
            }

            throw new SQLError()
        })
    }
    let notes = [];
    let noteText;
    $: {
        getAllNotes()
    }
</script>

<form on:submit|preventDefault={post}>
    <input placeholder="Записка" bind:value={noteText}>
    <button type="submit">
        Отправить
    </button>
</form>

<div>
    {#each notes as {id, note}}
        <span>{id}, {note}</span> <br>
    {/each}
</div>