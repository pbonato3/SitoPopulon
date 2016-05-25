 
document.addEventListener('DOMContentLoaded', function(event) {
    cookieChoices.showCookieConsentBar('Il tuo messaggio per i visitarori.',
        'Chiudi', 'Maggiori Informazioni');
  });

var selectedRazza = document.getElementById('SelRazza'); 
 
selectedRazza.addEventListener('change', function() { 
  document.getElementById('immagineRazza').src = selezionaImg(this.value); 
}); 
 
function selezionaimg(razza){ 
  return "img/"+razza+".jpg" 
} 

var settedLevelAC = document.getElementById('setLevelAC'); 
settedLevel.addEventListener('change', function() { 
	if(document.getElementById('corpo')!= null){
  		document.getElementById('setLevelAC').src = setLevelAC+setBonus("corpo")
	} 
}); 

var settedLevelAC = document.getElementById('corpo'); 
settedLevel.addEventListener('change', function() { 
	if(document.getElementById('setLevelAC')!= null){
  		document.getElementById('setLevelAC').src = setLevelAC+setBonus("corpo")
	} 
}); 
 
function setBonus(tipo){ 
  	if(tipo=="corpo"){
		return Math.floor(document.getElementById('corpo')-20) / 10);
	} 
} 
