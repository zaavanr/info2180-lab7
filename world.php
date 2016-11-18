<?php

// accept a term (keyword)
// respond with a value

$query = $_GET['q'];
$definition = [
    "definition" => "A statement of the exact meaning of a word, especially in a dictionary.",
    "bar" => "A place that sells alcholic beverages",
    "ajax" => "Technique which involves the use of javascript and xml (or JSON)",
    "html" => "The standard markup language for creating web pages and web applications.",
    "css" => "A style sheet language used for describing the presentation of a document written in a markup language.",
    "javascript" => "A lightweight, interpreted programming language with first-class functions that adds interactivity to your website.",
    "php" => "A server-side scripting language, and a powerful tool for making dynamic and interactive websites",
];

$xmldef = '<?xml version="1.0" encoding="UTF-8"?>

    <findW>
        <word>
            <sr>definition</sr>
            <defn>A statement of the exact meaning of a word, especially in a dictionary.</defn>
        </word>
        <word>
            <sr>bar</sr>
            <defn>A place that sells alcholic beverages.</defn>
        </word>
        <word>
            <sr>ajax</sr>
            <defn>Technique which involves the use of javascript and xml (or JSON)</defn>
        </word>
        <word>
            <sr>html</sr>
            <defn>The standard markup language for creating web pages and web applications.</defn>
        </word>
        <word>
            <sr>css</sr>
            <defn>A style sheet language used for describing the presentation of a document written in a markup language.</defn>
        </word>
        <word>
            <sr>javascript</sr>
            <defn>A lightweight, interpreted programming language with first-class functions that adds interactivity to your website.</defn>
        </word>
        <word>
            <sr>php</sr>
            <defn>A server-side scripting language, and a powerful tool for making dynamic and interactive websites</defn>
        </word>
    </findW>';
    
    if (isset($_GET['all']) && $_GET['all'] == 'true') {
    // output your XML
     header('Content-Type: text/xml');
        $output = new SimpleXMLElement($xmldef);
        echo $output->asXML();
    } 
    else { 
        print "<h3>" . strtoupper($query) . "</h3>";
        print "<p>" . $definition[$query] . "</p>"; 
    }