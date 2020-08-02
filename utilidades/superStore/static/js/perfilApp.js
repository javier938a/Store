$(document).ready(function(){

    $("#foto").change(function(e){
        var ruta = e.target.files[0];
        imageType = /image.*/;
        if(!ruta.type.match(imageType))
         return;
        
        var reader = new FileReader();
        reader.onload = function(e){
            var resultado = e.target.result;
            $("#fotoPerfil").attr("src",resultado);
        };
        reader.readAsDataURL(ruta);

    });
});