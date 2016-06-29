#!"C:\xampp\perl\bin\perl.exe"
use CGI::Session;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);
use XML::LibXML;

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI

my $nome_utente= getSession();

if(!$nome_utente){		#qualcuno sta facendo il furbo
	print $page->redirect("/populon/restricted.html");
}

print $page->header,
$page->start_html( # inizio pagina HTML
-title => 'Populon',									# Qui va il titolo
-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',				# DTD
'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'
],
-lang =>'it',											# Lingua del documento
-meta => {'title' => 'Populon',							# Tutti i meta
'description' => 'Area Amministratori',
'keywords' => 'Gioco, ruolo, gdr, fantasy, dadi',
'author' => 'Mattia Biggeri, Tommaso Padovan, Diego Baratto, Paolo Bonato',
'language' => 'italian it'},
-style =>{'src' => '../PopStyle.css'},			# Link al CSS
-author => 'paolo.bonato.12@gmail.com');				# Mail all'autore

#################		header		#################

print $page->div({-class => 'sbarra'}), "\n";

print $page->div({-id => 'header'}, h1("Populon"), img({-class => 'head', -src => "../img/titolo.png", -alt => "Populon"}), a({-class => 'saltamenu', -href => '#saltamenu'}, "Salta il menu di navigazione")), "\n";

#################		nav		#################

print $page->div({-class => 'nav'}, ul({-class => 'navbar'},
li({-class => 'button link', -onclick => 'location.href="../Home.html";'}, a({-href => '../Home.html', -class => 'link'},"Home")),
li({-class => 'button link', -onclick => 'location.href="../IlMondoDiGioco.html";'}, a({-href => '../IlMondoDiGioco.html', -class => 'link'},"Il mondo di gioco")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/personaggi.cgi";'}, a({-href => '../cgi-bin/personaggi.cgi', -class => 'link'},"Personaggi")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/Notizie.cgi";'}, a({-href => '../cgi-bin/Notizie.cgi', -class => 'link'},"Notizie")),
li({-class => 'button link', -onclick => 'location.href="../Chi.html";'}, a({-href => '../Chi.html', -class => 'link'},"Chi siamo")))), "\n"; 

print $page->div({-class => 'breadcrumbs'}, a({-name => 'saltamenu'}), strong("Ti trovi in: "), "Area Amministratori"), "\n";

#################		content		#################

print "<div class='content'>";

if($nome_utente){											#se questo è vero la sessione è corretta
	print "<h2>Benvenuto $nome_utente</h2>";
	print "<form action='ScriviNotizia.cgi' method='post'>";
	print "</p><input type='submit' value='Scrivi Una Notizia'/></p>";
	print "</form>";
	print "<form action='logout.cgi' method='post'>";
	print "</p><input type='submit' value='Logout'/></p>";
	print "</form>";
	
}
else{														#questo perchè non si sa mai
	print "IMPOSTORE";							
};

print "<a href='#header' class='goup'>Vai a inizio pagina</a></div>";

print "<div id='footer'>Contatti: populon(at)gmail.com
		<div class='login'>
			<span>Login Amministratori</span>
			<form action='login.cgi' method='post'>
				<p>Username:
					<input name='username' type='text' />
					Password:
					<input name='password' type='password' />
					<input value='Login' type='submit' />
				</p>
			</form>
			<form action='cgi-bin/logout.cgi' method='post'>
				<p><input value='Logout' type='submit' /></p>
			</form>
		</div>
	</div>
	</div>";
	
print $page->end_html, "\n"; # fine pagina HTML
