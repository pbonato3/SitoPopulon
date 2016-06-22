#!"C:\xampp\perl\bin\perl.exe"
use CGI::Session;
use CGI::Cookie;
use CGI;
use XML::LibXML;
use Encode qw(decode encode);

######### Creare la sessione ########
#parametri in ingresso:
#	$_[0] username		Stringa
#	$_[1] password		Stringa

#parametri in uscita:
#	Boolean	vero se la sessione è stata creata falso altrimenti

sub createSession{
	my $cgi = CGI->new;
	my $file = '../database/admin.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root = $doc->getDocumentElement;		#estrazione elemento radice
	
	my $admin = $root->findnodes("admin[\@username='$_[0]' and \@password='$_[1]']");
	if($admin){
		$session=CGI::Session->new();
		$session->param('admin',$_[0]);
		$sid=$session->id();
		my $cookie = $cgi->cookie(
			-name=>'MY-COOKIE',
			-value=>$sid,
			-expires=>'+1h',
			-path=>'/');
		print $cgi->header( -cookie=>$cookie );	#invio il cookie al client
		return 1;
	};
	return undef;
};

######### prendere la sessione ########
#parametri in uscita:
#	$utente				Stringa che contiene il nome dell'utente della sessione. undef se non esite la sessione.
sub getSession{
	my $cgi = CGI->new;										#creo un nuovo oggetto cgi
	$cookie = $cgi->cookie('MY-COOKIE');					#provo a prendere il cookie
	$session=CGI::Session->load(undef,$cookie) or die $!;	#provo a prendere la sessione
	if ($session->is_expired || $session->is_empty ) {		#se la sessione non esiste o è scaduta
		return undef;										#ritorno undef
	} else {												#altrimenti
		my $utente = $session->param('admin');				#se la sessione è valida
		return $utente;										#ritorno il nome dell'amministratore
	};
};

######### distruzione sessione ########

sub destroySession() {
	my $cgi = CGI->new;										#creo un nuovo oggetto cgi
	$cookie = $cgi->cookie('MY-COOKIE');					#provo a prendere il cookie
	$session=CGI::Session->load(undef,$cookie) or die $!;	#provo a prendere la sessione
	$session->close();										#close elimina i campi dati della sessione
	$session->delete();										#delete elimina la sessione
	$session->flush();										#flush pulisce il buffer
}


######### Inserimento nuova notizia ########
#parametri in ingresso:
#	$_[0] titolo		Stringa
#	$_[1] data			ora formato yyyy-mm-dd
#	$_[2] ora			ora formato hh:mm:ss
#	$_[3] luogo			Stringa
#	$_[4] descrizione	Stringa
#	$_[5] id			Intero da usare solo in caso di modifica

#parametri in uscita:
#	$esito				Stringa da stampare a video per indicare l'esito dell'operazione così da segnalare eventuali errori specifici.

sub nuovaNotizia{
	my $file = '../database/news.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $esito = undef;
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root= $doc->getDocumentElement;		#estrazione elemento radice

	foreach (@_) {										#magia, non toccare, che va.
		$_=encode('UTF-8', $_, Encode::FB_CROAK);		#serve a codificare tutte le stringhe in input in UTF8 (accenti)
	}

	my $topId = undef;
	if ($_[5]) {			#se è impostato l'id
		#voglio modificare una notizia quindi tengo l'id
		$topId=$_[5];
	} else {
		#altrimenti voglio aggiungere una nuova notizia e devo calcolare il nuovo id
		$topId=0;
		my @IDs = $doc->findnodes("//notizia/\@id");
		foreach (@IDs) {
			my $actualID=$_->string_value();
			if ($actualID>$topId) {
				$topId=$actualID;
			}
		}
		$topId ++;
	};

	
	#creo una stringa con un nuovo elemento
	if(!$_[0]){$esito="Operazione fallita: Il titolo &egrave obbligatorio"; return $esito;}
	else{
		my $nuovo="\n<notizia id=\"$topId\">";
		$nuovo.="\n\t<titolo>".$_[0]."</titolo>";
		if($_[1]){$nuovo.="\n\t<data>".$_[1]."</data>";};
		if($_[2]){$nuovo.="\n\t<ora>".$_[2]."</ora>";};
		if($_[3]){$nuovo.="\n\t<luogo>".$_[3]."</luogo>";};
		if($_[4]){$nuovo.="\n\t<descrizione>".$_[4]."</descrizione>";};
		$nuovo.="\n</notizia>";

		$frammento = $parser->parse_balanced_chunk($nuovo);	#controllo la buona formazione e creo un nodo
		$root->insertBefore($frammento,$root->firstChild);	#inserisco un nuovo in testa alla lista (prima del primo figlio)
		open OUT, ">$file";			#apro l'output sul file xml
		print OUT $doc->toString;	#stampo sul file il documento parsato
		close(OUT);
		$esito="Operazione completata";
		return $esito;
	};
	$esito = "operazione fallita";
	return $esito;
};

######### Ricerca notizia tramite id ########
#parametri in ingresso:
#	$_[0] id			Intero

#parametri in uscita:
#	$notizia			Oggetto di tipo notizia. undef se non trovata

sub trovaNotizia{
	my $file = '../database/news.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root= $doc->getDocumentElement;		#estrazione elemento radice
	my $notizia = $doc->findnodes("//notizia[\@id ='$_[0]']")->get_node(1);	#trovo il nodo tramite l'id
	return $notizia;
};

######### Eliminazione notizia ########
#parametri in ingresso:
#	$_[0] id			Intero

#parametri in uscita:
#	$esito				Stringa da stampare a video per indicare l'esito dell'operazione così da segnalare eventuali errori specifici.

sub eliminaNotizia{
	my $file = '../database/news.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $esito= undef;
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root= $doc->getDocumentElement;		#estrazione elemento radice
	my $da_eliminare = $doc->findnodes("//notizia[\@id ='$_[0]']")->get_node(1);	#trovo il nodo da eliminare tramite l'id
	if($da_eliminare){							#notizia trovata
		my $padre = $da_eliminare->parentNode;	#mi sposto sul padre
		$padre->removeChild($da_eliminare);		#elimino il figlio
		open OUT, ">$file";						#apro l'output sul file xml
		print OUT $doc->toString;				#stampo sul file il documento parsato
		close(OUT);
		$esito="Operazione completata";
		return $esito;
	}
	else{										#notizia non trovata
		$esito="Notizia non trovata";
		return $esito;
	};
};


######### Ricerca personaggio tramite id ########
#parametri in ingresso:
#	$_[0] id			Intero

#parametri in uscita:
#	$personaggio		Oggetto di tipo notizia. undef se non trovato

sub trovaPersonaggio{
	my $file = '../database/characters.xml';#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root= $doc->getDocumentElement;		#estrazione elemento radice
	my $personaggio = $doc->findnodes("//character[\@id ='$_[0]']")->get_node(1);	#trovo il nodo tramite l'id
	return $personaggio;
};

######### Eliminazione personaggio ########
#parametri in ingresso:
#	$_[0] id			Intero

#parametri in uscita:
#	$esito				Stringa da stampare a video per indicare l'esito dell'operazione così da segnalare eventuali errori specifici.

sub eliminaPersonaggio{
	my $file = '../database/characters.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $esito= undef;
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root= $doc->getDocumentElement;		#estrazione elemento radice
	my $da_eliminare = $doc->findnodes("//character[\@id ='$_[0]']")->get_node(1);	#trovo il nodo da eliminare tramite l'id
	if($da_eliminare){							#personaggio trovato
		my $padre = $da_eliminare->parentNode;	#mi sposto sul padre
		$padre->removeChild($da_eliminare);		#elimino il figlio
		open OUT, ">$file";						#apro l'output sul file xml
		print OUT $doc->toString;				#stampo sul file il documento parsato
		close(OUT);
		$esito="Operazione completata";
		return $esito;
	}
	else{										#personaggio non trovato
		$esito="Personaggio non trovato";
		return $esito;
	};
};


1	# NON toccare questo uno! deve stare in fondo alla pagina!