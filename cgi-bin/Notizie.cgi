#!"C:\xampp\perl\bin\perl.exe"
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);

#creazione oggetto CGI
my $page = CGI->new;

use XML::LibXML;
my $file = '../database/news.xml';
#creazione oggetto parser
my $parser = XML::LibXML->new();
#apertura file e lettura input
my $doc = $parser->parse_file($file);
#estrazione elemento radice
my $root= $doc->getDocumentElement;
#array dei nodi notiza
my @notizie = $root->findnodes("notizia");

############## filtra per titolo ##############
$titolo = $page->param('titolo');
if($titolo){
	@temp = ();
		foreach(@notizie){
			$t=$_->findnodes("titolo");
			if($t =~ /$titolo/){push @temp,$_;};
		};
	@notizie=@temp;
}
############## filtra per data ##############
$data = $page->param('data');
if($data){
	@temp = ();
		foreach(@notizie){
			$t=$_->findnodes("data");
			if($t =~ /$data/){push @temp,$_;};
		};
	@notizie=@temp;
}
############## filtra per luogo ##############
$luogo = $page->param('luogo');
if($luogo){
	@temp = ();
		foreach(@notizie){
			$t=$_->findnodes("luogo");
			if($t =~ /$luogo/){push @temp,$_;};
		};
	@notizie=@temp;
}
############## ricerca standard ##############
if(!$titolo and !$data and !$luogo){
my $n_notizie = 10; #massimo numero di notize nella pagina standard
@notizie = $root->findnodes("notizia[position()<=$n_notizie]");
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
print "<h2> Notizie </h2>";

print "<form action='/populon/cgi-bin/Notizie.cgi' method='GET'>";
print "<span>Filtro notizie</span>";
print "<p>Titolo: <input name='titolo' type='text'/></p>";
print "<p>Data: <input name='data' type='text'/></p>";
print "<p>Luogo: <input name='luogo' type='text'/></p>";
print "</p><input type='submit' value='Filtra'/></p>";
print "</form>";

foreach(@notizie){
	print "<div class='news'>",
	"<h3>",$_->findnodes("titolo"),"</h3>";
	$data = $_->findnodes("data");
	if($data){print "<p><span class='newsTag'>Data:</span><span class='newsValue'>",$data,"</span></p>";}
	$ora = $_->findnodes("ora");
	if($ora){print "<p><span class='newsTag'>Ora:</span><span class='newsValue'>",$ora,"</span></p>";}
	$luogo = $_->findnodes("luogo");
	if($luogo){print "<p><span class='newsTag'>Luogo:</span><span class='newsValue'>",$luogo,"</span></p>";}
	$descrizione = $_->findnodes("descrizione");
	if($descrizione){print "<p><span class='newsTag'>Descrizione:</span><p class='newsValue'>",$descrizione,"</p></p>";}
	print "</div>";
}

print "</div>";

	
print $page->end_html, "\n"; # fine pagina HTML
