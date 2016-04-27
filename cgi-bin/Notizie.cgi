#!"C:\xampp\perl\bin\perl.exe"

use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

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
my @notizie = $root->findnodes("notizia");
my @titoli = $root->findnodes("notizia/titolo");
my @date = $root->findnodes("notizia/data");
my @orari = $root->findnodes("notizia/ora");
my @luoghi = $root->findnodes("notizia/luogo");


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
$var=0;
foreach(@notizie){
	print "<div>",
	"<h3>",@notizie[$var]->findnodes("titolo"),"</h3>";
	$data = @notizie[$var]->findnodes("data");
	if($data){print "<p> Data:        ",$data,"</p>";}
	$ora = @notizie[$var]->findnodes("ora");
	if($ora){print "<p> Ora:        ",$ora,"</p>";}
	$luogo = @notizie[$var]->findnodes("luogo");
	if($luogo){print "<p> Luogo:        ",$luogo,"</p>";}
	print "</div>";
	$var++;
}

print "</div>";

	
print $page->end_html, "\n"; # fine pagina HTML
