<?xml version="1.0" encoding="UTF-8"?>
<!--
  Copyright (c) 2013 – The MITRE Corporation
  All rights reserved. See LICENSE.txt for complete terms.
 -->
<!--
CybOX XML to HTML transform v2.0
Compatible with CybOX v2.0

This is an xslt to transform a cybox 2.0 document of observables into html for
easy viewing.  The series of observables are turned into collapsible elements
on the screen.  Details about each observable's contents are displayed in a
format representing the nested structure of the original document.

Below the main observable, Object, Event, and Observable_Composition are
displayed.  For composite observables, the nested structure of the composition
and the logical relationships is displayed via nested tables with operators
("and" and "or) on the left and then a series of component expressions on rows
on the right.

Objects which are referred to by reference can be expanded within the context
of the parent object, unless the reference points to an external document

This is a work in progress.  Feedback is most welcome!

requirements:
 - XSLT 2.0 engine (this has been tested with Saxon 9.5)
 - a CybOX 2.0 input xml document

Updated 2013
mcoarr@mitre.org & mdunn@mitre.org

Updated 9/11/2012
ikirillov@mitre.org
  
-->


<xsl:stylesheet 
    version="2.0"
    xmlns:cybox="http://cybox.mitre.org/cybox-2"
    xmlns:Common="http://cybox.mitre.org/common-2"
    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:fn="http://www.w3.org/2005/xpath-functions"

    xmlns:EmailMessageObj="http://cybox.mitre.org/objects#EmailMessageObject-2"
    exclude-result-prefixes="cybox Common xsi fn EmailMessageObj">


    <!-- import reusable cybox_common templates -->
    <xsl:import href="cybox_common.xsl" />
    <xsl:output method="html" omit-xml-declaration="yes" indent="yes" media-type="text/html" version="4.0" />

    <!--
      This is the main template that sets up the html page that sets up the
      html structure, includes the base css and javascript, and adds the
      content for the metadata summary table up top and the heading and
      surrounding content for the Observables table.
    --> 
    <xsl:template match="/">
            <html>
               <head>
                <title>CybOX Output</title>
                <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
                <style type="text/css">
                    
                    body
                    {
                      font-family: Arial,Helvetica,sans-serif;
                    }
                    /* define table skin */
                    table.grid {
                    margin: 0px;
                    margin-left: 25px;
                    padding: 0;
                    border-collapse: separate;
                    border-spacing: 0;
                    width: 100%;
                    border-style:solid;
                    border-width:1px;
                    }
                    
                    table.grid thead, table.grid .collapsible {
                    background-color: #c7c3bb;
                    }
                    
                    table.grid th {
                    color: #565770;
                    padding: 4px 16px 4px 0;
                    padding-left: 10px;
                    font-weight: bold;
                    text-align: left;
                    } 
                    
                    table.grid td {
                    color: #565770;
                    padding: 4px 6px;
                    }

                    table.grid tr.even {
                    background-color: #EDEDE8;
                    }

                    body {
                    /*font: 11px Arial, Helvetica, sans-serif;*/
                    /*font-size: 13px;*/
                    }
                    #wrapper { 
                    margin: 0 auto;
                    width: 80%;
                    }
                    #header {
                    color: #333;
                    padding: 10px;
                    /*border: 2px solid #ccc;*/
                    margin: 10px 0px 5px 0px;
                    /*background: #BD9C8C;*/
                    }
                    #content { 
                    width: 100%;
                    color: #333;
                    border: 2px solid #ccc;
                    background: #FFFFFF;
                    margin: 0px 0px 5px 0px;
                    padding: 10px;
                    /*font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;*/
                    font-size: 11px;
                    color: #039;
                    }
                    
                    #hor-minimalist-a
                    {
                      font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                      font-size: 12px;
                    }
                    #hor-minimalist-a > thead > tr > th
                    {
                      border-bottom: 2px solid #6678b1;
                      text-align: left;
                    }
                    .one-column-emphasis
                    {
                    /*font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;*/
                    /*font-size: 12px;*/
                    margin: 0px;
                    text-align: left;
                    /*border-collapse: collapse;*/
                    width: 100%;
                    border-spacing: 0;
                    }
                    .one-column-emphasis > tbody > tr > td
                    {
                    padding: 5px 10px;
                    color: #200;
                    }
                    .oce-first
                    {
                    background: #d0dafd;
                    border-right: 10px solid transparent;
                    border-left: 10px solid transparent;
                    }
                    .oce-first-obs
                    {
                    background: #EFF8F4;
                    /*border-right: 10px solid transparent;*/
                    border-right: 10px solid black;
                    }
                    .oce-first-obscomp-or
                    {
                    background: #E9EEF4;
                    border-right: 10px solid transparent;
                    }
                    .oce-first-obscomp-and
                    {
                    background: #F2F4E9;
                    border-right: 10px solid transparent;
                    }
                    .oce-first-inner
                    {
                    background: #EFF8F4;
                    border-right: 10px solid transparent;
                    border-left: 10px solid transparent;
                    }
                    .oce-first-inner-inner
                    {
                    background: #E5F4EE;
                    border-right: 10px solid transparent;
                    border-left: 10px solid transparent;
                    }
                    .oce-first-inner-inner-inner
                    {
                    background: #DBEFE6;
                    border-right: 10px solid transparent;
                    border-left: 10px solid transparent;
                    }
                    .oce-first-inner-inner-inner-inner
                    {
                    background: #D0EAE0;
                    border-right: 10px solid transparent;
                    border-left: 10px solid transparent;
                    }
                    .oce-first-inner-inner-inner-inner-inner
                    {
                    background: #B7D1C6;
                    border-right: 10px solid transparent;
                    border-left: 10px solid transparent;
                    }
                    #container { 
                    color: #333;
                    border: 1px solid #ccc;
                    background: #FFFFFF;
                    margin: 0px 0px 10px 0px;
                    padding: 10px;
                    }
                    #section { 
                    color: #333;
                    background: #FFFFFF;
                    margin: 0px 0px 5px 0px;
                    }
                    #object_label_div div {
                    /*display: inline;*/
                    /*width: 30%;*/
                    }
                    #object_type_label {
                    width:200px;
                    background: #e8edff;
                    border-top: 1px solid #ccc;
                    border-left: 1px solid #ccc;
                    border-right: 5px solid #ccc;
                    padding: 1px;
                    }
                    #defined_object_type_label {
                    width:400px;
                    background: #E9F3CF;
                    border-top: 1px solid #ccc;
                    border-left: 1px solid #ccc;
                    border-right: 1px solid #ccc;
                    padding: 1px;
                    }
                    #associated_object_label {
                    /*font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;*/
                    font-size: 12px;
                    margin-bottom: 2px;
                    }
                    .heading,
                    .eventTypeHeading
                    {
                      margin-bottom: 0.5em;
                      font-weight: bold;
                    }
                    .contents,
                    .eventDescription
                    {
                      margin-top: 0.5em;
                      margin-bottom: 0.5em;
                    }
                    .container
                    {
                      margin-left: 1em;
                      padding-left: 0.5em;
                    }
                    .eventDescription,
                    .description
                    {
                      font-style: italic!important;
                      margin-top: 0.5em;
                      margin-bottom: 0.5em;
                    }
                    .description::before
                    {
                      font-weight: bold;
                      content: "Description: "
                    }
                    .emailDiv
                    {
                      display: block!important;
                    }
                    .relatedTarget
                    {
                    animation: targetHighlightAnimation 0.2s 10;
                    animation-direction: alternate;
                    -webkit-animation: targetHighlightAnimation 0.2s;
                    -webkit-animation-direction: alternate;
                    -webkit-animation-iteration-count: 10;
                    }
                    @keyframes targetHighlightAnimation
                    {
                    0% {background: hsla(360, 100%, 50%, .3); }
                    100% {background: hsla(360, 100%, 50%, .7); }
                    }
                    @-webkit-keyframes targetHighlightAnimation
                    {
                    0% {background: hsla(360, 100%, 50%, .3); }
                    100% {background: hsla(360, 100%, 50%, .7); }
                    }
                    
                    .highlightTargetLink
                    {
                    color: blue;
                    text-decoration: underline;
                    }
                    
                    table.compositionTableOperator > tbody > tr > td
                    {
                      padding: 0.5em;
                    }
                    table.compositionTableOperand > tbody > tr > td
                    {
                      padding: 0;
                    }
                    table.compositionTableOperator > tbody > tr > td,
                    table.compositionTableOperand > tbody > tr > td
                    {
                      /* border: solid gray thin; */
                      /* border-collapse: collapse; */
                      border: none;
                      padding: 0.5em;
                    }
                    .compositionTable,
                    .compositionTableOperator,
                    .compositionTableOperand
                    {
                      border-collapse: collapse;
                      padding: 0!important;
                      border: none;
                    }
                    td.compositionTable,
                    td.compositionTableOperator,
                    td.compositionTableOperand
                    {
                      padding: 0!important;
                      border: none;
                    }
                    .compositionTableOperand
                    {
                      padding: 0.5em;
                    }
                    .compositionTableOperand > tbody > tr > td > div 
                    {
                      background-color: lightcyan;
                      padding: 0.7em;
                    }
                    
                    /* make DL look like a table */
                    dl.table-display
                    {
                    float: left;
                    width: 520px;
                    margin: 1em 0;
                    padding: 0;
                    border-bottom: 1px solid #999;
                    }
                    
                    .table-display dt
                    {
                    clear: left;
                    float: left;
                    width: 200px;
                    margin: 0;
                    padding: 5px;
                    border-top: 1px solid #999;
                    font-weight: bold;
                    }
                    
                    .table-display dd
                    {
                    float: left;
                    width: 300px;
                    margin: 0;
                    padding: 5px;
                    border-top: 1px solid #999;
                    }
                    
                    .verbatim
                    {
                      white-space: pre-line;
                      margin-left: 1em;
                    }
                    table
                    {
                      empty-cells: show;
                    }
                    
                    .externalLinkWarning
                    {
                      font-weight: bold;
                      color: red;
                    }
                    
                    .inlineOrByReferenceLabel
                    {
                      font-style: italic!important;
                      color: lightgray;
                    }
                    
                    .contents
                    {
                      padding-left: 1em;
                    }
                    
                    .cyboxPropertiesValue
                    {
                      font-weight: normal;
                    }
                    
                    .cyboxPropertiesConstraints
                    {
                      font-weight: normal;
                      font-style: italic!important;
                      color: red;
                    }
                    
                    .cyboxPropertiesConstraints .objectReference
                    {
                      color: black;
                    }
                    
                    .objectReference
                    {
                      margin-left: 1em;
                    }
                    
                    .expandableContainer.collapsed > .expandableToggle::before,
                    .expandableContainer.collapsed.expandableToggle::before
                    {
                      content: "+";
                    }
                    .expandableContainer.expanded > .expandableToggle::before,
                    .expandableContainer.expanded.expandableToggle::before
                    {
                      /*
                        this is the minus character, which is the
                        same width as the plus character
                      */
                      content: "\2212";

                    }
                    .expandableContainer > .expandableToggle::before,
                    .expandableContainer.expandableToggle::before,
                    .nonexpandableContainer::before
                    {
                      color: goldenrod;
                      /*
                      display: inline-block;
                      width: 1em;
                      */
                    }
                    .nonexpandableContainer::before
                    {
                      content: "";
                    }

                    .expandableToggle
                    {
                      cursor: pointer; 
                      padding-left: 1.0em;
                      text-indent: -0.5em;
                    }
                    .expandableContainer > .expandableContents
                    {
                      background-color: #A8CBDE;
                      padding-top: 0.25em;
                      padding-right: 1em;
                      padding-left: 0.5em;
                      padding-bottom: 0.5em;
                    }
                    
                    .expandableSeparate.expandableContainer.collapsed > .expandableContents
                    {
                      display: none;
                    }

                    .longText
                    {
                       width: 60em;
                    }
                    .expandableSame.expandableContainer.collapsed
                    {
                      overflow: hidden;
                      height: 1em;
                    }
                    .expandableSame.expandableContainer.expanded
                    {
                        word-wrap: break-word;
                    }

                    .associatedObjectContents
                    {
                        font-weight: normal;
                    }
                    .baseobj
                    {
                    }
                    .copyobj
                    {
                    }
                    .baseobserv
                    {
                    }
                    .copyobserv
                    {
                    }
                    
                    .debug
                    {
                      display: none;
                    }
                </style>
                
                <script type="text/javascript">
                  <![CDATA[
                  /*! @source http://purl.eligrey.com/github/classList.js/blob/master/classList.js*/
                  if(typeof document!=="undefined"&&!("classList" in document.createElement("a"))){(function(j){if(!("HTMLElement" in j)&&!("Element" in j)){return}var a="classList",f="prototype",m=(j.HTMLElement||j.Element)[f],b=Object,k=String[f].trim||function(){return this.replace(/^\s+|\s+$/g,"")},c=Array[f].indexOf||function(q){var p=0,o=this.length;for(;p<o;p++){if(p in this&&this[p]===q){return p}}return -1},n=function(o,p){this.name=o;this.code=DOMException[o];this.message=p},g=function(p,o){if(o===""){throw new n("SYNTAX_ERR","An invalid or illegal string was specified")}if(/\s/.test(o)){throw new n("INVALID_CHARACTER_ERR","String contains an invalid character")}return c.call(p,o)},d=function(s){var r=k.call(s.className),q=r?r.split(/\s+/):[],p=0,o=q.length;for(;p<o;p++){this.push(q[p])}this._updateClassName=function(){s.className=this.toString()}},e=d[f]=[],i=function(){return new d(this)};n[f]=Error[f];e.item=function(o){return this[o]||null};e.contains=function(o){o+="";return g(this,o)!==-1};e.add=function(){var s=arguments,r=0,p=s.length,q,o=false;do{q=s[r]+"";if(g(this,q)===-1){this.push(q);o=true}}while(++r<p);if(o){this._updateClassName()}};e.remove=function(){var t=arguments,s=0,p=t.length,r,o=false;do{r=t[s]+"";var q=g(this,r);if(q!==-1){this.splice(q,1);o=true}}while(++s<p);if(o){this._updateClassName()}};e.toggle=function(p,q){p+="";var o=this.contains(p),r=o?q!==true&&"remove":q!==false&&"add";if(r){this[r](p)}return !o};e.toString=function(){return this.join(" ")};if(b.defineProperty){var l={get:i,enumerable:true,configurable:true};try{b.defineProperty(m,a,l)}catch(h){if(h.number===-2146823252){l.enumerable=false;b.defineProperty(m,a,l)}}}else{if(b[f].__defineGetter__){m.__defineGetter__(a,i)}}}(self))};
                  ]]>
                </script>

                <script type="text/javascript">
                    <![CDATA[
                    <!-- toggle top-level Observables -->
                    function toggleDiv(divid, spanID) {
                        if (document.getElementById(divid).style.display == 'none') {
                            document.getElementById(divid).style.display = 'block';
                            if (spanID) {
                                document.getElementById(spanID).innerText = "-";
                            }
                        }
                        else {
                            document.getElementById(divid).style.display = 'none';
                            if (spanID) {
                                document.getElementById(spanID).innerText = "+";
                            }
                        }
                    }

                    <!-- onload, make a clean copy of all top level Observables for compositions before they are manipulated at runtime -->
                    function embedCompositions() {
                        var divCompBaseList = getElementsByClass('baseobserv');
                        var divCompCopyList = getElementsByClass('copyobserv');

                        for (i = 0; i < divCompCopyList.length; i++) {
                            for (j = 0; j < divCompBaseList.length; j++) {
                                if (divCompCopyList[i].id == 'copy-' + divCompBaseList[j].id) {
                                    divCompCopyList[i].innerHTML = divCompBaseList[j].innerHTML;
                                }
                            }
                        }

                        return false;
                    }

                    <!-- copy object from clean src copy to dst destination and then toggle visibility -->
                    function embedObject(container, src, dst) {
                        <!-- deep copy the source div's html into the destination div --> 
                        <!-- (typically a RelatedObjects's content expanded into a parent Object's RO container) -->
                        var objDiv = document.getElementById(src).cloneNode(true);

                        for (i = 0; i < container.children.length; i++) {
                            if ((typeof (container.children[i].id) != "undefined") && (container.children[i].id == dst)) {
                                container.children[i].innerHTML = objDiv.innerHTML;
                            }
                        }

                        <!-- finally, toggle the visibility state of the div  -->
                        toggle(container);

                        return false;
                    }

                    <!-- onload, make a clean copy of all id'd objects/actions for runtime copying -->
                    function runtimeCopyObjects() {
                        embedCompositions()

                        var divSrcList = getElementsByClass('baseobj');
                        var divDstList = getElementsByClass('copyobj');

                        for (i = 0; i < divSrcList.length; i++) {
                            divDeepCopy = divSrcList[i].cloneNode(true);

                            <!-- remove heading from copied content since expandable reference will contain header info -->
                            for (j = 0; j < divDeepCopy.children.length; j++) {
                                if ((typeof (divDeepCopy.children[j].className) != "undefined") && (divDeepCopy.children[j].className.indexOf("heading") > -1)) {
                                    divDeepCopy.removeChild(divDeepCopy.children[j]);
                                    break;
                                }
                            }

                            for (k = 0; k < divDstList.length; k++) {
                                if ('copy-' + divDeepCopy.id == divDstList[k].id)
                                    divDstList[k].innerHTML = divDeepCopy.innerHTML;
                            }
                        }

                        return false;
                    }

                    <!-- identify all elements in the document which have the parameterized class applied -->
                    function getElementsByClass(inClass) {
                        var children = document.body.getElementsByTagName('*');
                        var elements = [],
                            child;
                        for (var i = 0, length = children.length; i < length; i++) {
                            child = children[i];
                            if ((typeof (child.className) != "undefined") && (child.className.indexOf(inClass) > -1)) {
                                elements.push(child);
                            }
                        }
                        return elements;
                    }

                    <!-- toggle visibility of a container element -->
                    function toggle(containerElement) {
                      // now using a shim to support classList in IE8/9
                      containerElement.classList.toggle("collapsed");
                      containerElement.classList.toggle("expanded");
                    }
                 ]]>
                </script>
               </head>
                <body onload="runtimeCopyObjects();">
                    <div id="wrapper">
                        <div id="header"> 
                            <H1>CybOX Output</H1>
                            <table id="hor-minimalist-a" width="100%">
                                <thead>
                                    <tr>
                                        <th scope="col">Major Version</th>
                                        <th scope="col">Minor Version</th>
                                        <th scope="col">Filename</th>
                                        <th scope="col">Generation Date</th>
                                    </tr>
                                </thead>
                                <TR>
                                    <TD><xsl:value-of select="//cybox:Observables/@cybox_major_version"/></TD>
                                    <TD><xsl:value-of select="//cybox:Observables/@cybox_minor_version"/></TD>
                                    <TD><xsl:value-of select="tokenize(document-uri(.), '/')[last()]"/></TD>
                                    <TD><xsl:value-of select="current-dateTime()"/></TD>
                                </TR>   
                            </table>
                        </div>
                        <h2><a name="analysis">Observables</a></h2>
                          <xsl:call-template name="processObservables" />
                   </div>
                </body>
            </html>
    </xsl:template>
</xsl:stylesheet>
