$(document).ready(function(){
    $(".foto").hover(function(){
        var ubi = $(this).attr("src");
        //alert(ubi);
        $("#foto_producto").attr("src",ubi);
    })
});