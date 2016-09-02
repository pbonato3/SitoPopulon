#!"C:\xampp\perl\bin\perl.exe"
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI

my $admin = getSession();

print '
<!DOCTYPE html
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">
<head>
<title>Populon</title>
<link rev="made" href="mailto:paolo.bonato.12%40gmail.com" />
<meta name="keywords" content="Gioco, ruolo, gdr, fantasy, dadi" />
<meta name="language" content="italian it" />
<meta name="author" content="Mattia Biggeri, Tommaso Padovan, Diego Baratto, Paolo Bonato" />
<meta name="title" content="Populon" />
<meta name="description" content="Compila la tua scheda online" />
<link rel="stylesheet" type="text/css" href="../PopStyle.css" />
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<meta http-equiv="Content-Script-Type" content="text/javascript"/>
</head>
<body onload=\'clearRedundant()\'>
';

#################		header		#################

print "<div class=\"sbarra\" >\n";

print $page->div({-id => 'header'}, h1("Populon"), img({-class => 'head', -src => "../img/titolo.png", -alt => "Populon"}), a({-class => 'saltamenu', -href => '#saltamenu'}, "Salta il menu di navigazione")), "\n";

#################		nav		#################

print $page->div({-class => 'nav'}, ul({-class => 'navbar'},
li({-class => 'button link', -onclick => 'location.href="../index.html";'}, a({-href => '../index.html', -class => 'link'},"Home")),
li({-class => 'button link', -onclick => 'location.href="../IlMondoDiGioco.html";'}, a({-href => '../IlMondoDiGioco.html', -class => 'link'},"Il mondo di gioco")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/personaggi.cgi";'}, a({-href => '../cgi-bin/personaggi.cgi', -class => 'link'},"Personaggi")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/Notizie.cgi";'}, a({-href => '../cgi-bin/Notizie.cgi', -class => 'link'},"Notizie")),
li({-class => 'button link', -onclick => 'location.href="../Chi.html";'}, a({-href => '../Chi.html', -class => 'link'},"Chi siamo")))), "\n"; 

print "
<div class=\"breadcrumbs\">
 <a name=\"saltamenu\"></a>
  <strong>
    Ti trovi in:
  </strong>
  <a href=\"personaggi.cgi\"> Personaggi </a>
  &gt; &gt; Aggiungi Personaggio
</div>
";

#################		content		#################
#massimo numero di abilità
my $max = 10;




print "<script type=\"text/javascript\" src=\"../PopScripts.js\"></script>";






print "<div class='content'>";
print "<h2> Compila la tua scheda </h2>";

print "<div class='scheda'>";
# form per l'input dei dati di un personaggio
	print "<form action='inserimentoPersonaggio.cgi' method='post' enctype='multipart/form-data'>";
	# Insermento nome
	print "<p> Nome: <input title='nome' name='nome' type='text' oninput='checkNome()'/></p>";
	print "<p class='errore' id='errNome'>Il nome &egrave; obbligatorio</p>";
	# Inserimento razza
	print "<p>Razza: <select name='razza'>",
		"<option value='Akquor'>Akquor</option>",
		"<option value='Elfo'>Elfo</option>",
		"<option value='Mustelan'>Mustelan</option>",
		"<option value='Nano'>Nano</option>",
		"<option value='Spyrian'>Spyrian</option>",
		"<option value='Tesserian'>Tesserian</option>",
		"<option value='Troll'>Troll</option>",
		"<option value='Umano'>Umano</option>",
		"<option value='Ur-Aluk'>Ur-Aluk</option>",
		"</select></p>";
	# Inserimento sesso
	print "<p>Sesso: <input title='sesso' type='radio' name='sesso' value='M' checked='checked' /> M",
		"<input title='gender' type='radio' name='gender' value='F' /> F </p>";
	# Inserimento età
	print "<p>Et&agrave;: <input title='eta' name='eta' type='text' oninput='checkEta()' /></p>";
	print "<p class='errore' id='errEta'>L'et&agrave; deve essere un numero di massimo tre cifre</p>";
	# Inserimento punti corpo
	print "<p>Punti corpo: <input title='corpo' name='corpo' type='text' oninput='checkCorpo()'/></p>";
	print "<p class='errore' id='errCorpo'>I punti corpo devono essere un numero di massimo tre cifre</p>";
		print "<div class='elencoFormAbilita'>";
		for(my $i=0; $i < $max; $i++){
			print "<p id='ac$i'>Abilit&agrave;: <input title='name_c$i' name='name_c$i' type='text' oninput='checkC($i)' id='acInput$i' />";
			print "Livello: <select name='value_c$i' id='lc$i'>";
			for(my $j=1; $j<=5; $j++){
				print"<option value=\"$j\">$j</option>";
			}
			print "</select></p>";
		}
		print "</div>";
	# Inserimento punti mente
	print "<p>Punti mente: <input title='mente' name='mente' type='text' oninput='checkMente()' /></p>";
	print "<p class='errore' id='errMente'>I punti mente devono essere un numero di massimo tre cifre</p>";
		print "<div class='elencoFormAbilita'>";
		for(my $i=0; $i < $max; $i++){
			print "<p id='am$i'>Abilit&agrave;: <input title='name_m$i' name='name_m$i' type='text' oninput='checkM($i)' id='amInput$i' />";
			print "Livello: <select name='value_m$i'>";
			for(my $j=1; $j<=5; $j++){
				print"<option value=\"$j\">$j</option>";
			}
			print "</select></p>";
		}
		print "</div>";
	# Inserimento punti spirito
	print "<p>Punti spirito: <input title='spirito' name='spirito' type='text' oninput='checkSpirito()'/></p>";
	print "<p class='errore' id='errSpirito'>I punti spirito devono essere un numero di massimo tre cifre</p>";
		print "<div class='elencoFormAbilita'>";
		for(my $i=0; $i < $max; $i++){
			print "<p id='as$i'>Abilit&agrave;: <input title='name_s$i' name='name_s$i' type='text' oninput='checkS($i)' id='asInput$i'/>";
			print "Livello: <select name='value_s$i'>";
			for(my $j=1; $j<=5; $j++){
				print"<option value=\"$j\">$j</option>";
			}
			print "</select></p>";
		}
		print "</div>";
	# Inserimento biografia
	print "<p>Biografia: </p><p><textarea name='bio' rows='10' cols='50'></textarea></p>";
	print "<p><input type='submit' value='Conferma'/></p>";
	print "</form>";
print "</div><a href='#header' class='goup'>Vai a inizio pagina</a>
</div>";

print "<div id='footer'>Contatti: populon(at)gmail.com
		<div class='login'>
			<span>Login Amministratori</span>
			<form action='login.cgi' method='post'>
				<p>Username:
					<input title='username' name='username' type='text' />
					Password:
					<input title='password' name='password' type='password' />
					<input value='Login' type='submit' />
				</p>
			</form>
			<form action='logout.cgi' method='post'>
				<p><input value='Logout' type='submit' /></p>
			</form>
		</div>
	</div>
	</div>";

	
print $page->end_html, "\n"; # fine pagina HTML
