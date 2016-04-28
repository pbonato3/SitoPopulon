<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">

<html>
<head>
    <title>Populon</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="title" content="Populon" />
    <meta name="description" content="Gioco di ruolo di..." />
    <meta name="keywords" content="Gioco, ruolo, gdr, fantasy, dadi" />
    <meta name="author" content="Mattia Biggeri, Tommaso Padovan, Diego Baratto, Paolo Bonato" />
    <meta name="language" content="italian it" />
    <link href="../PopStyle.css" rel="stylesheet" type="text/css" media="screen"/>
</head>
<body>
	<div id="header">
		<!--Titolo fuori dallo schermo-->
		<h1>Populon</h1>
		<img src="../img/titolo.png" />
	</div>
	<!--Barra di navigazione come lista di link e span per la pagina corrente-->
	<div id="nav">
		<ul>
			<li><a href="/populon/Home.html">Home</a></li>
			<li><a href="/populon/IlMondoDiGioco.html">Il mondo di gioco</a></li>
			<li><a href="/populon/IPersonaggi.html">I personaggi</a></li>
			<li><span>Notizie</span></li>
			<li><a href="/populon/Chi.html">Chi Siamo</a></li>
		</ul>
	</div>
	<div id="content">
	
		<h2> Notizie </h2>
		<xsl:for-each select="notizie/notizia">
			<div class="news">
				<h3><xsl:value-of select="titolo"/></h3>
				<p><span class="newsTag">Data:  </span><span><xsl:value-of select="data"/></span></p>
				<p><span class="newsTag">Ora:   </span><span><xsl:value-of select="ora"/></span></p>
				<p><span class="newsTag">Luogo: </span><span><xsl:value-of select="luogo"/></span></p>
				<p><span class="newsTag">Descrizione: </span><p><xsl:value-of select="descrizione"/></p></p>
			</div>
		</xsl:for-each>

	</div>
	<div id="footer">contatti: populon@gmail.com</div>
</body>
</html>

</xsl:template>
</xsl:stylesheet>

