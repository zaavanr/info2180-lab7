$(document).ready(function(){
    $('#lookup').on('click',hRequest)
   
});
function hRequest(wrd){
    wrd.preventDefault();
    if(($('#country').val()=='') && ($('#all').prop('checked')== false)){
        alert('Enter a country tick the view all box');
    }
    var htpR = new XMLHttpRequest();
    if( $('#all').prop('checked')){
        var url = 'world.php?all=true';
        htpR.onreadystatechange = hResponse;
        htpR.open('GET',url);
        htpR.send();
        }
        else{
        var url = 'world.php?c='+ $('#country').val();
        htpR.onreadystatechange = hResponse;
        htpR.open('GET',url);
        htpR.send();
        }
}

function hResponse(){
    if(this.readyState==XMLHttpRequest.DONE){
        if(this.status==200){
            var answ=this.responseText;
            $('#result').html(answ);
        }
        else{
            $('#result').html('Error');
        }
    }
}