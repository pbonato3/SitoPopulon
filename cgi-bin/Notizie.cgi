#!"C:\xampp\perl\bin\perl.exe"
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);
use XML::LibXML;

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI
my $admin = getSession();

my $file = '../database/news.xml';		#salvo il percorso del file xml

my $admin = getSession();

my $parser = XML::LibXML->new();		#creazione oggetto parser
my $doc = $parser->parse_file($file);	#apertura file e lettura input
my $root= $doc->getDocumentElement;		#estrazione elemento radice

my @notizie = $root->findnodes("notizia");	#array dei nodi notizia, inizzializzato con tutti i nodi. Successivamente va filtrato e usato per l'output

############## filtra per titolo ##############
$titolo = $page->param('titolo');							#prendo il parametro dall'url
if($titolo){												#se il parametro è vuoto non lo considero
	@temp = ();												#inizializzo un array temporaneo nel quale mettere le notizie corrispondenti
		foreach(@notizie){									#scorro l'array delle notizie
			$value = lc $_->findnodes("titolo");			#salvo il valore del nodo (trasformato in lower case)
			$search = lc $titolo;							#trasformo in lower case il parametro di ricerca
			if($value =~ /$search/){push @temp,$_;};		#se il nodo contiene la stringa cercata la inserisco nell'array temporaneo
		};
	@notizie=@temp;											#l'array delle notizie è stato filtrato
}
############## filtra per data ##############
$data = $page->param('data');								#prendo il parametro dall'url
if($data){													#se il parametro è vuoto non lo considero
	@temp = ();												#inizializzo un array temporaneo nel quale mettere le notizie corrispondenti
		foreach(@notizie){									#scorro l'array delle notizie eventualmente filtrato
			$value = $_->findnodes("data");					#salvo il valore del nodo
			if($value =~ /$data/){push @temp,$_;};			#se il nodo contiene la stringa cercata la inserisco nell'array temporaneo
		};
	@notizie=@temp;											#l'array delle notizie è stato filtrato
}
############## filtra per luogo ##############
$luogo = $page->param('luogo');								#prendo il parametro dall'url
if($luogo){													#se il parametro è vuoto non lo considero
	@temp = ();												#inizializzo un array temporaneo nel quale mettere le notizie corrispondenti
		foreach(@notizie){									#scorro l'array delle notizie eventualmente filtrato
			$value = lc $_->findnodes("luogo");				#salvo il valore del nodo (trasformato in lower case)
			$search = lc $luogo;							#trasformo in lower case il parametro di ricerca
			if($value =~ /$search/){push @temp,$_;};		#se il nodo contiene la stringa cercata la inserisco nell'array temporaneo
		};
	@notizie=@temp;											#l'array delle notizie è stato filtrato
}
############## ricerca standard ##############
if(!$titolo and !$data and !$luogo){								#non è stato inserito nessun parametro di ricerca
	my $n_notizie = 10; 												#massimo numero di notize nella pagina standard
	@notizie = $root->findnodes("notizia[0<=position()<=$n_notizie]");		#l'array delle notizie contiene solo le ultime n_notizie
}



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

print $page->div({-id => 'header'}, h1("Populon"), img({-src => "/populon/img/titolo.png"})), "\n";

#################		nav		#################

print $page->div({-id => 'nav'}, ul(
li(a({-href => '/populon/Home.html'},"Home")),
li(a({-href => '/populon/IlMondoDiGioco.html'},"Il mondo di gioco")),
li(a({-href => '/populon/IPersonaggi.html'},"I personaggi")),
li(span("Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 

#################		content		#################

print "<div id='content'>";
if($admin){
	print "<form action='ScriviNotizia.cgi' method='post'>";
	print "</p><input type='submit' value='Scrivi Una Notizia'/></p>";
	print "</form>";
};





#genero l'array contenete i link per la paginazione delle notizie
my $totNotizie=0;
foreach(@notizie) {$totNotizie+=1;}

my $notiziePerPagina=10;		#<------------ 	QUI SI IMPOSTA IL NUMERO MASSIMO DI NOTIZIE PER OGNI PAGINA


#salvo in $from e in $to i numeri delle notizie che devono essere visualizzate
my $from=$page->param('from');
my $to=$page->param('to');
if (!$from) {$from=1;}
if (!$to) {
	if ($totNotizie<$notiziePerPagina) {$to=$totNotizie}
	else {$to=$notiziePerPagina;}
}


my @arrLink=();					# l'array contenente i link per navigare tra le pagine

my $urlAttuale=CGI->new->url()."?titolo=".$page->param('titolo')."&data=".$page->param('data')."&luogo=".$page->param('luogo');

if ($totNotizie<$notiziePerPagina) {$notiziePrimaPagina=$totNotizie}
else {$notiziePrimaPagina=$notiziePerPagina;}
push @arrLink,"<a href='".$urlAttuale."&from=1&to=$notiziePrimaPagina'>Prima pagina</a>";
my $c=1;
while ($c<=$totNotizie) {
	if ($c!=$from) {
		if ($c+$notiziePerPagina-1 <= $totNotizie) {
			my $str="<a href='".$urlAttuale."&from=$c&to=".($c+$notiziePerPagina-1)."'>".$c.'-'.($c+$notiziePerPagina-1)."</a>";
			push @arrLink,$str;
		}
		else {
			my $str="<a href='".$urlAttuale."&from=$c&to=$totNotizie'>".$c.'-'.$totNotizie."</a>";
			push @arrLink,$str;
		}
	} else {
		if ($c+$notiziePerPagina-1 <= $totNotizie) {
			my $str=$c.'-'.($c+$notiziePerPagina-1);
			push @arrLink,$str;
		}
		else {
			my $str=$c.'-'.$totNotizie;
			push @arrLink,$str;
		}
	}
	$c+=$notiziePerPagina;
}
$c-=$notiziePerPagina;
push @arrLink,"<a href='".$urlAttuale."&from=$c&to=$totNotizie'>Ultima pagina</a>";








# spengo il link alla pagina attuale nella barretta di navigazione
foreach(@arrLink) {

}



print "<h2> Notizie dalla $from alla $to</h2>";
print "<form action='/populon/cgi-bin/Notizie.cgi' method='GET'>";
print "<span>Filtro notizie</span>";
print "<p>Titolo: <input name='titolo' type='text'/></p>";
print "<p>Data: <input name='data' type='date'/></p>";
print "<p>Luogo: <input name='luogo' type='text'/></p>";
print "</p><input type='submit' value='Filtra'/></p>";
print "</form>";



print " | ";
foreach(@arrLink) {
	print;
	print " | ";
}





## Output delle notizie ##
my $i=1;
foreach(@notizie){									#scorro l'array delle notizie
	if ($from <= $i and $i <= $to ) {
		print "<div class='news'>";
		my $titolo = $_->findnodes("titolo");				#salvo il valore del nodo titolo
		print "<h3>",$titolo,"</h3>";
		my $data = $_->findnodes("data");					#salvo il valore del nodo data
		if($data){print "<p><span class='newsTag'>Data:</span><span class='newsValue'>",$data,"</span></p>";}
	#	my $ora = $_->findnodes("ora");					#salvo il valore del nodo ora
	#	if($ora){print "<p><span class='newsTag'>Ora:</span><span class='newsValue'>",$ora,"</span></p>";}
	#	my $luogo = $_->findnodes("luogo");				#salvo il valore del nodo luogo
	#	if($luogo){print "<p><span class='newsTag'>Luogo:</span><span class='newsValue'>",$luogo,"</span></p>";}
	#	my $descrizione = $_->findnodes("descrizione");	#salvo il valore del nodo descrizione
	#	if($descrizione){print "<p><span class='newsTag'>Descrizione:</span><p class='newsValue'>",$descrizione,"</p></p>";}
		my $id=$_->findnodes('@id');
		if($admin) {
			print "<a href='dettagliNotizia.cgi?id=$id'>Modifica...</a>";
			print "<a href='process_deleteNotizia.cgi?id=$id'>Cancella</a>";
		}
		else {print "<a href='dettagliNotizia.cgi?id=$id'>Pi&ugrave dettagli...</a>";}
		print "</div>";
	}
	$i+=1;
}






print " | ";
foreach(@arrLink) {
	print;
	print " | ";
}

print "</div>";

	
print $page->end_html, "\n"; # fine pagina HTML
