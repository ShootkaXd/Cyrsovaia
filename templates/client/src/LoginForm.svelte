<script>
    async function login() {
        if (!(name || password))
            return;
        await fetch("/login", {
            headers: {"Content-Type": "application/json"},
            "body": JSON.stringify({name, password}),
            "method": "POST",
        }).then(response => {
            if (response.ok)
                return;
            if (response.status == 403) {
                register()
                return;
            }
            throw new SQLError()
        })
    }

    async function register(){
        await fetch("/register", {
            headers:{"Content-Type":"application/json"},
            "body": JSON.stringify({name, password}),
            "method": "POST",
        }).then(response => response.json())
    }

    let name, password;

</script>

<form on:submit|preventDefault={login}>
    <input placeholder="Логин" bind:value={name}>
    <input placeholder="Пароль" bind:value={password}>
    <button type="submit">
        Войти
    </button>
</form>