#!"C:\xampp\perl\bin\perl.exe"
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI

my $admin = getSession();

print $page->header,
$page->start_html( # inizio pagina HTML
-title => 'Populon',									# Qui va il titolo
-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',				# DTD
'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'
],
-lang =>'it',											# Lingua del documento
-meta => {'title' => 'Populon',							# Tutti i meta
'description' => 'Gioco di ruolo di...',
'keywords' => 'Gioco, ruolo, gdr, fantasy, dadi',
'author' => 'Mattia Biggeri, Tommaso Padovan, Diego Baratto, Paolo Bonato',
'language' => 'italian it'},
-style =>{'src' => '/populon/PopStyle.css'},			# Link al CSS
-author => 'paolo.bonato.12@gmail.com');				# Mail all'autore

#################		header		#################

print $page->div({-id => 'header'}, h1("Populon"), img({-src => "/populon/img/titolo.png", -alt => "Populon"})), "\n";

#################		nav		#################

print $page->div({-id => 'nav'}, ul(
li(a({-href => '/populon/Home.html'},"Home")),
li(a({-href => '/populon/IlMondoDiGioco.html'},"Il mondo di gioco")),
li(a({-href => '/populon/cgi-bin/personaggi.cgi'},"I personaggi")),
li(a({-href => '/populon/cgi-bin/Notizie.cgi'},"Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 

#################		content		#################
#massimo numero di abilità
my $max = 10;
my $campiObbligatori = 0;
my $esito = "Mancano i seguenti campi obbligatori: ";

my $nome = $page->param('nome');
if(!$nome){
$esito.= "Nome; ";
$campiObbligatori = 1;
}
my $razza = $page->param('razza');
if(!$razza){
$esito.= "Razza; ";
$campiObbligatori = 1;
}
my $sesso = $page->param('sesso');
if(!$sesso){
$esito.= "Sesso; ";
$campiObbligatori = 1;
}
my $eta = $page->param('eta');
if(!$eta){
$esito.= "Et&agrave; ";
$campiObbligatori = 1;
}
else{
	if(!($eta=~ /^(\d|\d\d|\d\d\d)$/)){
		$esito = "Operazione fallita: L'et&agrave; deve essere un numero di massimo tre cifre";
		$campiObbligatori = 1;
	}
}
my $punti_c = $page->param('corpo');
if(!($punti_c =~ /^(\d|\d\d|\d\d\d)$/)){
	$esito = "Operazione fallita: I punti corpo devono essere un numero di massimo tre cifre";
	$campiObbligatori = 1;
}
my $punti_m = $page->param('mente');
if(!($punti_m =~ /^(\d|\d\d|\d\d\d)$/)){
	$esito = "Operazione fallita: I punti mente devono essere un numero di massimo tre cifre";
	$campiObbligatori = 1;
}
my $punti_s = $page->param('spirito');
if(!($punti_s =~ /^(\d|\d\d|\d\d\d)$/)){
	$esito = "Operazione fallita: I punti spirito devono essere un numero di massimo tre cifre";
	$campiObbligatori = 1;
}
for(my $i=0; $i < $max; $i++){
	my $aux = $page->param('value_c'.$i);
	if($aux && !($aux =~ /(1|2|3|4|5)/)){
		$esito = "Operazione fallita: I livelli delle abilità devono essere numeri compresi tra 1 e 5";
		$campiObbligatori = 1;
	}
	my $aux = $page->param('value_m'.$i);
	if($aux && !($aux =~ /(1|2|3|4|5)/)){
		$esito = "Operazione fallita: I livelli delle abilità devono essere numeri compresi tra 1 e 5";
		$campiObbligatori = 1;
	}
	my $aux = $page->param('value_s'.$i);
	if($aux && !($aux =~ /(1|2|3|4|5)/)){
		$esito = "Operazione fallita: I livelli delle abilità devono essere numeri compresi tra 1 e 5";
		$campiObbligatori = 1;
	}
}
my $bio = $page->param('bio');

if($campiObbligatori == 0 ){
	$esito="Operazione completata";
	my $punti_c = $page->param('corpo');
	my $punti_m = $page->param('mente');
	my $punti_s = $page->param('spirito');
	my $bio = $page->param('bio');

	my $file = '../database/characters.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $esito = undef;
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root= $doc->getDocumentElement;		#estrazione elemento radice

	#calcolo nuovo id
	my $topId=0;
	my @IDs = $doc->findnodes("//character/\@id");
	foreach (@IDs) {
		my $actualID=$_->string_value();
		if ($actualID>$topId) {
			$topId=$actualID;
		}
	}
	$topId ++;
	
	my $nuovo="\n<character id=\"$topId\">";
	$nuovo.="\n\t<name>".$nome."</name>";
	$nuovo.="\n\t<race>".$razza."</race>";
	$nuovo.="\n\t<sex>".$sesso."</sex>";
	$nuovo.="\n\t<age>".$eta."</age>";
	$nuovo.="\n\t<body value=\"$punti_c\">";
	for(my $i=0; $i < $max; $i++){
		my $aux_n = $page->param('name_c'.$i);
		my $aux_v = $page->param('value_c'.$i);
		if($aux_n && $aux_v){
			$nuovo.="\n\t\t<ability name=\"".$aux_n."\" level=\"".$aux_v."\"/>";
		}
		else {$i = $max;}
	}
	$nuovo.="\n\t</body>";
	$nuovo.="\n\t<mind value=\"$punti_m\">";
	for(my $i=0; $i < $max; $i++){
		my $aux_n = $page->param('name_m'.$i);
		my $aux_v = $page->param('value_m'.$i);
		if($aux_n && $aux_v){
			$nuovo.="\n\t\t<ability name=\"".$aux_n."\" level=\"".$aux_v."\"/>";
		}
		else {$i = $max;}
	}
	$nuovo.="\n\t</mind>";
	$nuovo.="\n\t<heart value=\"$punti_s\">";
	my $arrSize = @abilita_s;
	for(my $i=0; $i < $max; $i++){
		my $aux_n = $page->param('name_s'.$i);
		my $aux_v = $page->param('value_s'.$i);
		if($aux_n && $aux_v){
			$nuovo.="\n\t\t<ability name=\"".$aux_n."\" level=\"".$aux_v."\"/>";
		}
		else {$i = $max;}
	}
	$nuovo.="\n\t</heart>";
	$nuovo.="\n\t<bio>".$bio."</bio>";
	$nuovo.="\n</character>";
	
	$frammento = $parser->parse_balanced_chunk($nuovo);	#controllo la buona formazione e creo un nodo
	$root->insertBefore($frammento,$root->firstChild);	#inserisco un nuovo in testa alla lista (prima del primo figlio)
	open OUT, ">$file";			#apro l'output sul file xml
	print OUT $doc->toString;	#stampo sul file il documento parsato
	close(OUT);
}

print "<div id='content'>";
print "<h2> $esito </h2>";
print "<form action='/populon/cgi-bin/personaggi.cgi' method='post'>";
print "<p><input type='submit' value='Torna ai Personaggi'/></p>";
print "</form>";
print "</div>";

	
print $page->end_html, "\n"; # fine pagina HTML