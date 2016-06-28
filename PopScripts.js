 
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
	if(document.getElementById('corpo')!= null && document.getElementById('setLevelAC') < 5){
  		document.getElementById('setLevelAC').src = setLevelAC+setBonus("corpo")
	} 
}); 

var settedLevelAC = document.getElementById('corpo'); 
settedLevel.addEventListener('change', function() { 
	if(document.getElementById('setLevelAC')!= null && document.getElementById('setLevelAC') < 5){
  		document.getElementById('setLevelAC').src = setLevelAC+setBonus("corpo")
	} 
}); 
 
function setBonus(tipo){ 
  	if(tipo=="corpo"){
		if(document.getElementById('corpo')-20 > 0)
		return 1
		else
		return 0
	} 
} 



function checkC(i) {
	var x = document.getElementById('acInput'.concat(i)).value;
	if (x!='') {
	   document.getElementById('ac'.concat(i+1)).style.display = 'block';
	} else {
	   document.getElementById('ac'.concat(i+1)).style.display = 'none';
	}
}

function checkM(i) {
	var x = document.getElementById('amInput'.concat(i)).value;
	if (x!='') {
	   document.getElementById('am'.concat(i+1)).style.display = 'block';
	} else {
	   document.getElementById('am'.concat(i+1)).style.display = 'none';
	}
}

function checkS(i) {
	var x = document.getElementById('asInput'.concat(i)).value;
	if (x!='') {
	   document.getElementById('as'.concat(i+1)).style.display = 'block';
	} else {
	   document.getElementById('as'.concat(i+1)).style.display = 'none';
	}
}


function clearRedundant() {
	for (i = 1; i < 10; i++) { 
		document.getElementById('ac'.concat(i)).style.display = 'none';	
	}
	for (j = 1; j < 10; j++) { 
		document.getElementById('am'.concat(j)).style.display = 'none';	
	}
	for (k = 1; k < 10; k++) { 
		document.getElementById('as'.concat(k)).style.display = 'none';	
	}
}

function checkEta() {
	var x = document.getElementsByName('eta')[0].value;
	if (isNumber(x) && Number(x)<1000) {
		document.getElementById('errEta').style.display = 'none';	
	} else {
		document.getElementById('errEta').style.display = 'block';
	}
}


function checkCorpo() {
	var x = document.getElementsByName('corpo')[0].value;
	if (isNumber(x) && Number(x)<1000) {
		document.getElementById('errCorpo').style.display = 'none';	
	} else {
		document.getElementById('errCorpo').style.display = 'block';
	}
}

function checkMente() {
	var x = document.getElementsByName('mente')[0].value;
	if (isNumber(x) && Number(x)<1000) {
		document.getElementById('errMente').style.display = 'none';	
	} else {
		document.getElementById('errMente').style.display = 'block';
	}
}

function checkSpirito() {
	var x = document.getElementsByName('spirito')[0].value;
	if (isNumber(x) && Number(x)<1000) {
		document.getElementById('errSpirito').style.display = 'none';	
	} else {
		document.getElementById('errSpirito').style.display = 'block';
	}
}

function isNumber(obj) { return !isNaN(parseFloat(obj)) }


function checkNome() {
	var x = document.getElementsByName('nome')[0].value;
	if (x!='') {
		document.getElementById('errNome').style.display = 'none';	
	} else {
		document.getElementById('errNome').style.display = 'block';
	}
}
