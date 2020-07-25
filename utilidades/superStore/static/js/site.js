const seguirPush = document.getElementById('btnSeguir');
const errorMsg = document.querySelector('.error');
seguirPush.addEventListener('click', async function(e){
    e.preventDefault();
    const usuario = document.querySelector('meta[name="name_user"]');
    button = document.getElementById('btnSeguir');
    errorMsg.innerText='';
    const head = "Nuevo Seguidor";
    const body = usuario.content+" te sigue en tu cuenta, probablemente un posible cliente";
    const meta = document.querySelector('meta[name="prove_id"]');
    const id = meta ? meta.content : null;
    
    if(head && body && id){
        button.innerText='Enviando...';
        button.disabled=true;
        const res = await fetch('/superStore/send_push', {
            method:'POST',
            body: JSON.stringify({head, body, id}),
            headers:{
                'content-type':'application/json'
            }
        });
        //alert(res.status);
        if(res.status==200){
            button.innerText='siguiendo';
            button.disabled=false;
        }else{
            errorMsg.innerText= res.message;
            button.innerText='hubo un error';
            button.disabled = false;
        }
    }
});
