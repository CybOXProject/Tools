<?xml version="1.0" encoding="UTF-8"?>
<!--
  Copyright (c) 2013 – The MITRE Corporation
  All rights reserved. See LICENSE.txt for complete terms.
 -->
<!--
CybOX XML to HTML transform v2.0beta1
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

Any time objects are referred to by reference, a clickable "link" is displayed
in the output html.  When the user clicks on the link, the target will be
scrolled to and highlighted on the screen with a red background.

This is a work in progress.  Feedback is most welcome!

requirements:
 - XSLT 2.0 engine (this has been tested with Saxon 9.5)
 - a CybOX 2.0 input xml document

Updated Fall 2013
david_renne@yahoo.com - Added indicator/taxii support and configruation options

Updated 2013
mcoarr@mitre.org

Updated 9/11/2012
ikirillov@mitre.org

DEVELOPER NOTES

1. The inline expandable content is presents some chances for infinite
   loops/recursions.  This should be detected.  The variable $idStack is
   a sequence that contains all @id attributes that have been processed in the
   the current output tree (it is similar to a call stack).  This is
   accomplished by using "idStack" params in the templates and that param
   is a sequence of string ids.  Each time a new id is processed, it gets
   added to the current sequence (and will be visible for all templates
   called within the current template - - essentially the current output
   subtree).
   
   If you need to debug this, you can look in two places.  First, each
   time an object, @object_reference, or observable is processed, debug
   messages are printed out.  This should show up in the console (in
   Oxygen, they show up in the "messages" window).  This is useful if the
   stylesheet is failing.  You can see how far it is getting and where it
   might be failing.
   
   Second, if the stylesheet is working and outputs html, each object or
   @object_reference/@idref, will print out the current idStack.  You can
   look in the source, or change the css for the class "debug" (it defaults
   to "display: none").
   html
-->



<xsl:stylesheet
    version="2.0"
    xmlns:cybox="http://cybox.mitre.org/cybox-2"
    xmlns:Common="http://cybox.mitre.org/common-2"
    xmlns:ArtifactObj="http://cybox.mitre.org/objects#ArtifactObject-2"

    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:fn="http://www.w3.org/2005/xpath-functions"

	xmlns:taxii="http://taxii.mitre.org/messages/taxii_xml_binding-1"
	xmlns:stix="http://stix.mitre.org/stix-1"
    xmlns:SystemObj="http://cybox.mitre.org/objects#SystemObject-2"
    xmlns:FileObj="http://cybox.mitre.org/objects#FileObject-2"
    xmlns:ProcessObj="http://cybox.mitre.org/objects#ProcessObject-2"
    xmlns:PipeObj="http://cybox.mitre.org/objects#PipeObject-2" 
    xmlns:PortObj="http://cybox.mitre.org/objects#PortObject-2" 
    xmlns:AddressObj="http://cybox.mitre.org/objects#AddressObject-2"
    xmlns:SocketObj="http://cybox.mitre.org/objects#SocketObject-2"
    xmlns:MutexObj="http://cybox.mitre.org/objects#MutexObject-2"
    xmlns:MemoryObj="http://cybox.mitre.org/objects#MemoryObject-2"
    xmlns:URIObj="http://cybox.mitre.org/objects#URIObject-2"
    xmlns:LibraryObj="http://cybox.mitre.org/objects#LibraryObject-2"
    xmlns:EmailMessageObj="http://cybox.mitre.org/objects#EmailMessageObject-2"
    xmlns:WinHandleObj="http://cybox.mitre.org/objects#WinHandleObject-2"
    xmlns:WinMutexObj="http://cybox.mitre.org/objects#WinMutexObject-2"
    xmlns:WinServiceObj="http://cybox.mitre.org/objects#WinServiceObject-2"
    xmlns:WinRegistryKeyObj="http://cybox.mitre.org/objects#WinRegistryKeyObject-2"
    xmlns:WinPipeObj="http://cybox.mitre.org/objects#WinPipeObject-2"
    xmlns:WinDriverObj="http://cybox.mitre.org/objects#WinDriverObject-2"
    xmlns:WinFileObj="http://cybox.mitre.org/objects#WinFileObject-2"
    xmlns:WinExecutableFileObj="http://cybox.mitre.org/objects#WinExecutableFileObject-2"
    xmlns:indicator="http://stix.mitre.org/Indicator-2"
    xmlns:WinProcessObj="http://cybox.mitre.org/objects#WinProcessObject-2" >

    <!-- <CONFIG> -->

        <!-- debug will allow you to conditionally inject information in the XSLT routine -->
        <xsl:variable name="debug" select="'false'"/>

        <!-- include_html_body will inline all CSS and javascript as well as wrap the HTML node around the Cybox object HTML output -->
        <xsl:variable name="include_html_body" select="'true'"/>

        <!-- include_cybox_version_info will inject information and headers about the Cybox version -->
        <xsl:variable name="include_cybox_version_info" select="'true'"/>

        <!-- include_cybox_version_info will inject information and headers about the Cybox version -->
        <xsl:variable name="show_id_and_type_header_row" select="'true'"/>

        <!-- if ID tag not found, set your desired text -->
        <xsl:variable name="default_observable_missing_id" select="'Untitiled Observable ID'"/>

        <!-- default display for observables and description "'none'" for collapsed and "''block'" for shown -->
        <xsl:variable name="default_collapse" select="'block'"/>

        <!-- Raw Stix and Indicator Specific Configuration -->

            <!-- Show a 24px header title containing the below prefix and then the stix:STIX_Header/stix:Title -->
            <xsl:variable name="show_indicator_package_title" select="'true'"/>

            <!-- if the below prefix variable ends in #, it will show an incrementer for multiple stix packages in your prefix. -->
            <!-- if left blank, it will just show any applicable stix:Title's --> 
            <xsl:variable name="show_indicator_package_prefix" select="'Indicator Package #'"/>

            <!-- Next to the header, show a link (Show Long Description) which will collapse the description stix:STIX_Header/stix:Description -->
            <xsl:variable name="show_indicator_package_description" select="'true'"/>

            <!-- Next to the indicator ID, show a link (Show Long Description) which will collapse the indicator description  -->
            <xsl:variable name="show_indicator_description" select="'true'"/>

    <!-- </CONFIG> -->
        
<xsl:output method="html" omit-xml-declaration="yes" indent="yes" media-type="text/html" version="4.0" />
   <xsl:key name="observableID" match="cybox:Observable | indicator:Observable" use="@id"/>
    <!--
      This is the main template that sets up the html page that sets up the
      html structure, includes the base css and javascript, and adds the
      content for the metadata summary table up top and the heading and
      surrounding content for the Observables table.
    --> 
    <xsl:template match="/">
        <xsl:variable name="include_html_body" select="$include_html_body"/>

        <xsl:if test="$include_html_body = 'true'">
            <xsl:call-template name="inlineOuterShell"/>
        </xsl:if>

        <xsl:if test="$include_html_body != 'true'">
            <xsl:call-template name="cleanOuterShell"/>
        </xsl:if>
    </xsl:template>
    
    <!--
      draw the main table on the page that represents the list of Observables.
      these are the elements that are directly below the root element of the page.
      
      each observable will generate two rows in the table.  the first one is the
      heading that's always visible and is clickable to expand/collapse the
      second row.
    -->
    <xsl:template name="processObservables">

      <xsl:for-each select="cybox:Observables | //stix:STIX_Package/stix:Indicators | //stix:STIX_Package/stix:Observables | //taxii:Inbox_Message/taxii:Content/stix:STIX_Package/stix:Indicators | //taxii:Inbox_Message/taxii:Content/stix:STIX_Package/stix:Observables">
          <xsl:variable name="show_indicator_package_title" select="$show_indicator_package_title"/>
          <xsl:variable name="show_indicator_package_prefix" select="$show_indicator_package_prefix"/>
          <xsl:variable name="show_indicator_package_description" select="$show_indicator_package_description"/>
          <xsl:variable name="show_indicator_description" select="$show_indicator_description"/>
          <xsl:variable name="default_collapse" select="$default_collapse"/>
          <xsl:variable name="show_id_and_type_header_row" select="$show_id_and_type_header_row"/>
          <xsl:variable name="item" select="." />
          <xsl:variable name="previous" select=".." />
          <xsl:variable name="show_long_text" select="if($default_collapse = 'none') then 'Show Long Description' else 'Hide Long Description'" />
          <div id="observablesspandiv" style="font-weight:bold; margin:5px; color:#BD9C8C;">
            <TABLE class="grid tablesorter" cellspacing="0">
                <COLGROUP>
                    <COL width="90%"/>
                    <COL width="10%"/>
                </COLGROUP>
                <THEAD>

                    <xsl:if test="name() = 'stix:Indicators' and $show_indicator_package_title = 'true'">
                        <!-- If is indicator, show indicator group title for this box -->
                        <TR>
                            <TH colspan="2" class="header">
                                <span style="font-size: 24px;">
                                    <xsl:if test="$show_indicator_package_prefix != '' and $previous/stix:STIX_Header/stix:Title">
                                        <xsl:value-of select="$show_indicator_package_prefix"/>
                                        <xsl:if test="substring($show_indicator_package_prefix,string-length($show_indicator_package_prefix),string-length($show_indicator_package_prefix)-1) = '#'">
                                            <xsl:value-of select="position()"/>
                                        </xsl:if>
                                         -
                                    </xsl:if>
                                    <xsl:value-of select="$previous/stix:STIX_Header/stix:Title"/>
                                    <xsl:if test="$show_indicator_package_description = 'true' and $previous/stix:STIX_Header/stix:Description">
                                        <a style="font-size:18px; cursor:pointer; color:mintcream;">
                                            <xsl:attribute name="onclick"><xsl:value-of select="concat('showLongDescription(this, ', position(),');')"/></xsl:attribute>
                                            (<xsl:value-of select="$show_long_text"/>)
                                        </a>
                                    </xsl:if>
                                </span>

                                <xsl:if test="$show_indicator_package_description = 'true' and $previous/stix:STIX_Header/stix:Description">
                                    <div style="font-size:13px; font-style: italic; display:{$default_collapse};">
                                        <xsl:attribute name="id"><xsl:value-of select="concat(position(),'_description')"/></xsl:attribute>
                                        <xsl:value-of select="$previous/stix:STIX_Header/stix:Description"/>
                                    </div>
                                </xsl:if>
                            </TH>
                        </TR>
                    </xsl:if>
                    <xsl:if test="$show_id_and_type_header_row = 'true'">
                        <TR>
                            <TH class="header">
                                ID
                            </TH>
                            <TH class="header">
                                Type
                            </TH>
                        </TR>
                    </xsl:if>
                </THEAD>
                <TBODY>
                    <xsl:for-each select="cybox:Observable | $item/stix:Indicator/indicator:Observable">
                        <!-- <xsl:sort select="cybox:Observable_Composition" order="descending"/> -->
                        <xsl:variable name="parent" select="parent::node()"/>
                        <xsl:variable name="evenOrOdd" select="if(position() mod 2 = 0) then 'even' else 'odd'" />

                        <xsl:choose>

                            <xsl:when test="$parent/@xsi:type ='indicator:IndicatorType'">
                                <xsl:if test="not(./preceding-sibling::node()/@id)">
                                    <TR style="width:100%;font-style:italic;">
                                        <TD style="background-color:#0088cc !important; color:white;">

                                            <strong>
                                                <xsl:value-of select="$parent/@id"/>
                                                <xsl:if test="not($parent/@id)">
                                                    Unknown Indicator ID
                                                </xsl:if>
                                            </strong>

                                            <xsl:if test="$show_indicator_description = 'true' and $parent/indicator:Description">
                                                <div style="font-size:13px; font-style: italic; display:{$default_collapse};">
                                                    <xsl:attribute name="id"><xsl:value-of select="concat(position(),'_description')"/></xsl:attribute>
                                                    <xsl:value-of select="$previous/stix:STIX_Header/stix:Description"/>
                                                </div>

                                                <a style="cursor:pointer; color:mintcream;">
                                                    <xsl:attribute name="onclick"><xsl:value-of select="concat('showLongIndicatorDescription(this, ', position(),');')"/></xsl:attribute>
                                                    (<xsl:value-of select="$show_long_text"/>)
                                                </a>
                                            </xsl:if>
                                        </TD>
                                        <TD style="background-color:#0088cc !important; color:white;">
                                            <xsl:if test="$parent/indicator:Type">
                                                (<xsl:value-of select="$parent/indicator:Type"/>)
                                            </xsl:if>
                                            <xsl:if test="not($parent/indicator:Type)">
                                                Unknown Type
                                            </xsl:if>
                                        </TD>
                                    </TR>
                                </xsl:if>


                                <xsl:if test="$show_indicator_description = 'true' and $parent/indicator:Description">
                                    <TR style="width:100%;font-style:italic;">
                                        <TD colspan="2">
                                            <!--@todo, there is a bug with multiple indicator packages where the ID's will collide and descriptions wont collapse properly -->
                                            <div style="font-size:13px; font-style: italic; display:{$default_collapse};">
                                                <xsl:attribute name="id"><xsl:value-of select="concat(position(),'_ind_description')"/></xsl:attribute>
                                                <xsl:value-of select="$parent/indicator:Description"/>
                                            </div>
                                        </TD>
                                    </TR>
                                </xsl:if>

                                <xsl:call-template name="processObservable"><xsl:with-param name="evenOrOdd" select="''"/></xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:call-template name="processObservable"><xsl:with-param name="evenOrOdd" select="$evenOrOdd"/></xsl:call-template>
                            </xsl:otherwise>
                        </xsl:choose>


                    </xsl:for-each>
                </TBODY>
            </TABLE>    
        </div>
        </xsl:for-each>
    </xsl:template>



    <!--
      Simple output without full HTML payload.

      Note: This XSLT file will inject xlmns namespaces into attributes inside the outer div#wrapper in which you should strip before using as a partial Cybox object HTML output and inject these namespaces in your outer shell of your page showing these Cybox details
    -->

    <xsl:template name="cleanOuterShell">

        <!--
            Copy your external style sheets if you want to test your cleanOuterShell
            <link href="http://localhost:8000/static/css/cybox.css" rel="stylesheet"/>
            <script src="http://localhost:8000/static/js/cybox.js"><![CDATA[    //]]></script>
        -->
        <xsl:variable name="include_cybox_version_info" select="$include_cybox_version_info"/>
        <div id="wrapper">
            <xsl:if test="$include_cybox_version_info = 'true'">
                <xsl:call-template name="cyboxHeader"/>
            </xsl:if>
            <xsl:call-template name="processObservables"/>
        </div>

    </xsl:template>


    <!--
      Inline output with all inline CSS and JS and no external files
    -->

    <xsl:template name="inlineOuterShell">
        <xsl:variable name="include_cybox_version_info" select="$include_cybox_version_info"/>

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
                    }
                    #wrapper {
                    margin: 0 auto;
                    width: 80%;
                    }
                    #header {
                    color: #333;
                    padding: 10px;
                    margin: 10px 0px 5px 0px;
                    }
                    #content {
                    width: 100%;
                    color: #333;
                    border: 2px solid #ccc;
                    background: #FFFFFF;
                    margin: 0px 0px 5px 0px;
                    padding: 10px;
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
                    margin: 0px;
                    text-align: left;
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
                      content: "description: "
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
                    /*
                    border-style: solid;
                    border-witdh: thin;
                    border=color: hsla(360, 100%, 50%, 1);
                    */
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
                      content: "-";
                    }
                    .expandableContainer > .expandableToggle::before,
                    .expandableContainer.expandableToggle::before,
                    .nonexpandableContainer::before
                    {
                      color: goldenrod;
                      display: inline-block;
                      width: 1.5em;
                    }
                    .nonexpandableContainer::before
                    {
                      content: "";
                    }

                    .expandableToggle
                    {
                      cursor: pointer;
                    }
                    .expandableContainer > .expandableContents
                    {
                      background-color: #A8CBDE;
                      padding: 1em;
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

                    .debug
                    {
                      display: none;
                    }
                </style>

                <script type="text/javascript">
                    <![CDATA[
                    //Collapse functionality
                    function toggleDiv(divid, spanID, span2)
                    {
                      if(document.getElementById(divid).style.display == 'none')
                      {
                        document.getElementById(divid).style.display = 'block';
                        if(spanID)
                        {
                          document.getElementById(spanID).innerText = "-";
                        }
                        if(span2)
                        {
                          document.getElementById(span2).innerText = "-";
                        }
                      } // end of if-then
                      else
                      {
                        document.getElementById(divid).style.display = 'none';
                        if(spanID)
                        {
                          document.getElementById(spanID).innerText = "+";
                        }
                        if(span2)
                        {
                          document.getElementById(span2).innerText = "+";
                        }
                      } // end of else
                    } // end of function toggleDiv()
                    ]]>
                </script>

<script type="text/javascript">
<![CDATA[
var currentTarget = null;
var previousTarget = null;

/*
  when a user clicks on a idref link, find, scroll to, and highlight the
  target element.  this is usually an object, event, observable, related
  object, or associated object.

  the highlighting is done via css transitions.
*/
function highlightTarget(targetId)
{
    var targetElement = document.getElementById(targetId);
    if (targetElement == null)
    {
      alert("target not in present document");
      return;
    }
    targetElement.setAttribute("class", "");
    findAndExpandTarget(targetElement);
    targetElement.scrollIntoView(false);
    targetElement.setAttribute("class", "relatedTarget");
}

/*
  When a user clicks on an indicator long description
*/

function showLongDescription(obj, targetId)
{
    toggleText(obj, targetId,'_description');
}

function showLongIndicatorDescription(obj, targetId)
{
    toggleText(obj, targetId,'_ind_description');
}

function toggleText(obj, targetId, id_convention)
{
    var targetElement = document.getElementById(targetId + id_convention);
    if (targetElement == null)
    {
        alert("target not in present document");
        return;
    }
    if(targetElement.style.display == 'block')
    {
        targetElement.style.display = 'none';
        obj.innerHTML = '(Show Long Description)';
    }
    else
    {
        targetElement.style.display = 'block';
        obj.innerHTML = '(Hide Long Description)';
    }
}

/*
  When a user clicks on an idref link, this function will find that referenced
  element and expand the parent Observable table row (if it's collapsed).
*/
function findAndExpandTarget(targetElement)
{
    var currentAncestor = targetElement.parentNode;
    var isFound = false;
    while (currentAncestor != null && !isFound)
    {
        isFound = currentAncestor.classList.contains("collapsibleContent");
        if (!isFound) { currentAncestor = currentAncestor.parentNode; }
    }

    if (isFound)
    {
        //var collapsibleLabel = currentAncestor.previousSibling;
        currentAncestor.style.display = 'block';
    }
}


function toggle(containerNode)
{
  console.log("starting toggle");
  //var parent = currentNode.parentNode;

  containerNode.classList.toggle("collapsed");
  containerNode.classList.toggle("expanded");

  console.log("finished toggle");
}
]]>
</script>
               </head>
                <body>
                    <div id="wrapper">
                        <xsl:if test="$include_cybox_version_info = 'true'">
                            <xsl:call-template name="cyboxHeader"/>
                        </xsl:if>
                        <xsl:call-template name="processObservables"/>
                   </div>
                </body>
            </html>
    </xsl:template>

    <xsl:template name="cyboxHeader">
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
    </xsl:template>
    
    <!--
      This is the template that produces the rows in the main table (the
      observables table) on the page.  These are the observables just below the
      root element of the document.
      
      Each observable produces two rows.  The first row is the heading and is
      clickable to expand/collapse the second row with all the details.
      
      The heading row contains the observable id and the observable type.
      The type is one of the following categories:
       - "Compostion"
       - "Event"
       - Object (the value of the cybox:Properties/xsi:type will be used)
       - "Object (no properties set)"
       - "Other"
    -->
    <xsl:template name="processObservable">
        <xsl:param name="idStack" select="()" />
        <xsl:param name="evenOrOdd" />

        <xsl:variable name="idStack" select="($idStack, fn:data(@id))" />
        <xsl:variable name="debug" select="$debug"/>
        <xsl:variable name="default_observable_missing_id" select="$default_observable_missing_id"/>
        <xsl:variable name="default_collapse" select="$default_collapse"/>
        <xsl:variable name="contentVar" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
        <xsl:variable name="imgVar" select="generate-id()"/>
        <xsl:variable name="parent" select="parent::node()"/>

        <xsl:if test="$debug = 'true'">
            <xsl:message>PROCESS OBSERVABLE current: <xsl:value-of select="@id"/>; stack: <xsl:value-of select="fn:string-join($idStack, ',')" /></xsl:message>
        </xsl:if>

        <xsl:if test="$debug != 'true'">
            <!-- for production output 1\n for each observable to ensure something is output -->
            <xsl:message>1</xsl:message>
        </xsl:if>

        <xsl:variable name="plus_minus" select="if($default_collapse = 'none') then '+' else '-'" />

        <TR>
            <xsl:attribute name="class"><xsl:value-of select="$evenOrOdd" /></xsl:attribute>
            <TD>
                <div id="fileObjAtt" class="collapsibleLabel" style="cursor: pointer;" onclick="toggleDiv('{$contentVar}','{$imgVar}','{$imgVar}-2')">
                    <span id="{$imgVar}" style="font-weight:bold; margin:5px; color:#BD9C8C;">
                        <xsl:value-of select="$plus_minus"/>
                    </span>

                    <xsl:choose>
                        <xsl:when test="@id">
                            <xsl:value-of select="@id"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="$default_observable_missing_id"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </div>
            </TD>
            <TD>
                <div style="cursor: pointer;" onclick="toggleDiv('{$contentVar}','{$imgVar}','{$imgVar}-2')">
                <span id="{$imgVar}-2" style="font-weight:bold; margin:5px; color:#BD9C8C;">
                    <xsl:value-of select="$plus_minus"/>
                </span>
                    <xsl:choose>
                        <xsl:when test="cybox:Observable_Composition">
                            Composition
                        </xsl:when>
                        <xsl:when test="cybox:Event">
                            Event
                        </xsl:when>
                        <xsl:when test="cybox:Object/cybox:Properties/@xsi:type">
                            <xsl:value-of select="fn:local-name-from-QName(fn:resolve-QName(cybox:Object/cybox:Properties/@xsi:type, cybox:Object/cybox:Properties))" />
                        </xsl:when>
                        <xsl:when test="cybox:Object/cybox:Properties/@xsi:type and not(cybox:Object/cybox:Properties/@xsi:type)">
                            Object (no properties set)
                        </xsl:when>
                        <xsl:otherwise>
                            Other
                        </xsl:otherwise>
                    </xsl:choose>
                </div>
            </TD>
        </TR>
        <TR><xsl:attribute name="class"><xsl:value-of select="$evenOrOdd" /></xsl:attribute>
        <TD colspan="2">
          <div id="{$contentVar}"  class="collapsibleContent" style="overflow:hidden; display:{$default_collapse}; padding:0px 7px;">
              <div><xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
                  <xsl:if test="cybox:Title">
                    <br/>
                    <div id="section">
                        <table class="one-column-emphasis">
                            <colgroup>
                                <col class="oce-first-obs" />
                            </colgroup>
                            <tbody>
                                <tr>
                                    <td>Title</td>
                                    <td>
                                        <xsl:for-each select="cybox:Title">
                                            <xsl:value-of select="."/>
                                        </xsl:for-each>
                                    </td>
                                </tr>
                            </tbody>
                        </table> 
                    </div>
                </xsl:if>              
              <!-- <xsl:if test="cybox:Observable"> -->
                  <xsl:if test="not(cybox:Observable_Composition)">
                  <br/>
                  <div id="section">
                      <table class="one-column-emphasis">
                          <colgroup>
                              <col class="oce-first-obs" />
                          </colgroup>
                          <tbody>
                              <tr>
                                  <!-- <td>Observable</td> -->
                                  <td>
                                      <xsl:apply-templates select="cybox:Object|cybox:Event">
                                          <xsl:with-param name="idStack" select="$idStack" />
                                      </xsl:apply-templates>
                                      <!-- <xsl:for-each select="cybox:Observable"> -->
                                      <!--    <xsl:call-template name="processPlainObservable"/> -->
                                      <!-- </xsl:for-each> -->
                                  </td>
                              </tr>
                          </tbody>
                      </table> 
                  </div>
                  </xsl:if>
              <!-- </xsl:if> -->
              <xsl:if test="cybox:Observable_Composition">
                  <br/>
                  <div id="section">
                      <table class="one-column-emphasis">
                          <colgroup>
                              <col class="oce-first-obs" />
                          </colgroup>
                          <tbody>
                              <tr>
                                  <td>Observable Composition</td>
                                  <td>
                                      <xsl:for-each select="cybox:Observable_Composition">
                                          <xsl:call-template name="processObservableCompositionSimple">
                                              <xsl:with-param name="idStack" select="$idStack" />
                                          </xsl:call-template>
                                      </xsl:for-each>
                                  </td>
                              </tr>
                          </tbody>
                      </table> 
                  </div>
              </xsl:if>
            </div>
            </div>
        </TD>
        </TR>

        <xsl:if test="$parent/@xsi:type ='indicator:IndicatorType' and not(./following-sibling::node()/@id)">
            <TR>
                <TD colspan="2">
                    <hr/>
                </TD>
            </TR>
        </xsl:if>
    </xsl:template>
    
    <!--
      Produce the details for an observable composition.
      
      This creates a table with a big cell on the left that includes the binary
      operator ("and" or "or").  Then on the right is a sequence of rows
      representing the expressions that are joined by the operator.
      
      This is visualized with colored backgrounds via css.
    -->
    <xsl:template name="processObservableCompositionSimple">
        <xsl:param name="idStack" select="()" />
        <table class="compositionTableOperator">
            <colgroup>
                <xsl:choose>
                    <xsl:when test="@operator='AND'">
                        <col class="oce-first-obscomp-and"/>
                    </xsl:when>
                    <xsl:when test="@operator='OR'">
                        <col class="oce-first-obscomp-or"/>
                    </xsl:when>
                </xsl:choose>
            </colgroup>
            <tbody>
                <tr>
                    <th>
                        <xsl:attribute name="rowspan"><xsl:value-of select="count(cybox:Observable)"/></xsl:attribute>
                        <span><xsl:value-of select="@operator"/></span>
                    </th>
                    <td>
                        <table class="compositionTableOperand">
                            <xsl:for-each select="cybox:Observable">
                                <tr>
                                    <td>
                                        <!-- [insert observable here] -->
                                        <xsl:call-template name="processObservableInObservableCompositionSimple">
                                            <xsl:with-param name="idStack" select="$idStack" />
                                        </xsl:call-template>
                                    </td>
                                </tr>
                                
                            </xsl:for-each>
                            <tr>
                            </tr>
                        </table>
                    </td>
                </tr>
                
            </tbody>
        </table> 
    </xsl:template>
    
    <!--
      Print out the heading for an inline object instance (it has an id
      attribute and does not have an idref attribute).
    -->
    <xsl:template name="inlineObjectHeading">
        <xsl:param name="type"/>
        <xsl:param name="currentObject"/>
        <xsl:param name="relationshipOrAssociationType" select="''"/>
        <xsl:param name="id"/>
        
        <xsl:variable name="currentObjectType">
            <xsl:choose>
                <!-- case 1: cybox objects have a cybox:Properties child with an xsi type,
                     or an observable has a child that is an object that has cybox:Properties
                -->
                <xsl:when test="($currentObject/cybox:Properties|$currentObject/cybox:*/cybox:Properties)/@xsi:type"><xsl:value-of select="fn:local-name-from-QName(fn:resolve-QName(($currentObject/cybox:Properties|$currentObject/cybox:*/cybox:Properties)/@xsi:type, ($currentObject/cybox:Properties|$currentObject/cybox:*/cybox:Properties)))"/></xsl:when>
                <!-- case 2: the current item is a cybox event or an observable that contains an event  -->
                <xsl:when test="$currentObject/cybox:Type|$currentObject/cybox:Event/cybox:Type"><xsl:value-of select="($currentObject/cybox:Type|$currentObject/cybox:Event/cybox:Type)/text()"/></xsl:when>
                <!-- catch all -->
                <xsl:otherwise></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <!-- <xsl:variable name="currentObjectType" select="if (local-name($currentObject) = 'Observable') then (local-name(($currentObject/*)[0])) else (if ($currentObject/cybox:Properties/@xsi:type) then (fn:local-name-from-QName(fn:resolve-QName($currentObject/cybox:Properties/@xsi:type, $currentObject/cybox:Properties))) else ('')) "/> -->
        
        <xsl:if test="$relationshipOrAssociationType">
            <xsl:value-of select="$relationshipOrAssociationType/text()" />
            <xsl:text> &#x25CB; </xsl:text>
        </xsl:if>
        
        <xsl:if test="$currentObjectType">
            <xsl:text> </xsl:text>
            <xsl:value-of select="$currentObjectType" />
            <xsl:text> &#x25CB; </xsl:text>
        </xsl:if>
        
        <xsl:element name="span">
            <xsl:attribute name="class" select="'inlineObject'" />
            
            <!-- THIS IS THE MAIN LINK TEXT -->
            <xsl:value-of select="$id"/>
            
        </xsl:element>
        <xsl:text> </xsl:text>
        
    </xsl:template>
    
    <!--
      This generates a "link" for an idref.  The link is really just text with
      an onclick event listener that calls highlightTarget().  
      
      When the user clicks the link, the referenced object (any element) will
      be found, it's parent top-level observable will be expanded, and the
      referenced object will be highlighted (the background will flash red a
      few times via css transitions).
    -->
    <xsl:template name="objectHeaderOnly">
        <xsl:param name="targetObject"/>
        <xsl:param name="relationshipOrAssociationType" select="''"/>
        <xsl:param name="idStack" />
        <xsl:param name="idref"/>
        
        <xsl:variable name="targetObjectType">
            <xsl:choose>
                <!-- case 0: targetObject not present -->
                <xsl:when test="not($targetObject)"></xsl:when>
                <!-- case 1: cybox objects have a cybox:Properties child with an xsi type,
                     or an observable has a child that is an object that has cybox:Properties
                -->
                <xsl:when test="($targetObject/cybox:Properties|$targetObject/cybox:*/cybox:Properties)/@xsi:type"><xsl:value-of select="fn:local-name-from-QName(fn:resolve-QName(($targetObject/cybox:Properties|$targetObject/cybox:*/cybox:Properties)/@xsi:type, ($targetObject/cybox:Properties|$targetObject/cybox:*/cybox:Properties)))"/></xsl:when>
                <!-- case 2: the current item is a cybox event or an observable that contains an event  -->
                <xsl:when test="$targetObject/cybox:Type|$targetObject/cybox:Event/cybox:Type"><xsl:value-of select="($targetObject/cybox:Type|$targetObject/cybox:Event/cybox:Type)/text()"/></xsl:when>
                <!-- catch all -->
                <xsl:otherwise></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        
        <xsl:if test="$relationshipOrAssociationType">
           <xsl:value-of select="$relationshipOrAssociationType/text()" />
           <xsl:text> &#x25CB; </xsl:text>
        </xsl:if>
        
        <xsl:if test="not($targetObject)">
            <xsl:text> </xsl:text><span class="externalLinkWarning">[external]</span>
            <!-- <xsl:text> &#x25CB; </xsl:text> -->
        </xsl:if>

        <xsl:if test="$targetObjectType">
            <xsl:text> </xsl:text>
            <xsl:value-of select="$targetObjectType" />
            <xsl:text> &#x25CB; </xsl:text>
        </xsl:if>
        
        <!-- THIS IS THE MAIN LINK TEXT -->
        <xsl:value-of select="$idref"/>

        <!--
        ###
        ### DISABLING "JUMP TO TARGET" LINKS
        ###
        <xsl:if test="$targetObject">
        <xsl:element name="span">
            <xsl:variable name="linkClass" select="if ($targetObject) then ('highlightTargetLink') else ('externalTargetLink')" />
            <xsl:attribute name="class"><xsl:value-of select="$linkClass" /></xsl:attribute>
            
            <!- - this is what makes the "link" - ->
            <xsl:if test="$targetObject">
                <xsl:attribute name="onclick"><xsl:value-of select='concat("highlightTarget(&apos;", $idref, "&apos;)")'/></xsl:attribute>
            </xsl:if>
            
            <!- - THIS IS THE MAIN LINK TEXT - ->
            [ jump to target ]
            
        </xsl:element>
        </xsl:if>
        ### END OF DISABLING "JUMP TO TARGET" LINKS
        -->
        
        <xsl:text> </xsl:text>
        
    </xsl:template>

    <!--
      This template formats the output for an observable that is contained
      within an observable composition.
      
      If it's an idref link, it will produce a clickable "link".
      
      If it's actual content, it will call the template
      processObservableCompositionSimple to print it out.
    -->
    <xsl:template name="processObservableInObservableCompositionSimple">
        <xsl:param name="idStack" select="()" />
        <xsl:if test="@idref">
            <div class="foreignObservablePointer">
                <xsl:variable name="targetId" select="string(@idref)"/>
                <xsl:variable name="relationshipOrAssociationType" select="''" />
                
                <xsl:call-template name="headerAndExpandableContent">
                    <xsl:with-param name="targetId" select="$targetId"/>
                    <xsl:with-param name="relationshipOrAssociationType" select="''" />
                    <xsl:with-param name="idStack" select="$idStack" />
                </xsl:call-template>
                
                
            </div>
        </xsl:if>
        
        <xsl:for-each select="cybox:Observable_Composition">
            <xsl:call-template name="processObservableCompositionSimple">
                <xsl:with-param name="idStack" select="$idStack" />
            </xsl:call-template>
        </xsl:for-each>
        
   </xsl:template>
    
    <!--
      shows the object header (relationship/assocation type, object type, and
      object id) and its associated expandable contents.
    -->
    <xsl:template name="headerAndExpandableContent">
        <xsl:param name="targetId" />
        <xsl:param name="targetObject" select="//*[@id = $targetId]" />
        <xsl:param name="relationshipOrAssociationType" />
        <xsl:param name="idStack" select="()" />
        <xsl:variable name="default_collapse" select="$default_collapse"/>
        <xsl:variable name="collapse_class" select="if($default_collapse = 'none') then 'collapsed' else 'expanded'" />

        <xsl:choose>
            <xsl:when test="$targetObject and not(fn:exists($idStack[. = $targetId]))">
                <div class="expandableContainer expandableSeparate {$collapse_class}">
                    <div class="expandableToggle objectReference" onclick="toggle(this.parentNode)">
                        <xsl:call-template name="objectHeaderOnly">
                            <xsl:with-param name="targetObject" select="$targetObject" />
                            <xsl:with-param name="relationshipOrAssociationType" select="$relationshipOrAssociationType"/>
                            <xsl:with-param name="idref" select="$targetId"/>
                            <xsl:with-param name="idStack" select="$idStack" />
                        </xsl:call-template>
                    </div>
                    <div class="expandableContents">
                        <!-- TODO <xsl:apply-templates select="$targetObject/*"/> -->
                        <xsl:apply-templates select="$targetObject">
                            <xsl:with-param name="idStack" select="$idStack" />
                            <xsl:with-param name="includeHeading" select="fn:false()" />
                        </xsl:apply-templates>
                    </div>
                </div>
            </xsl:when>
            <xsl:otherwise>
                <div class="objectReference nonexpandableContainer">
                  <xsl:call-template name="objectHeaderOnly">
                      <xsl:with-param name="targetObject" select="$targetObject" />
                      <xsl:with-param name="relationshipOrAssociationType" select="''"/>
                      <xsl:with-param name="idref" select="$targetId"/>
                      <xsl:with-param name="idStack" select="$idStack" />
                  </xsl:call-template>
                </div>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    
    
    <!--
      Simple template to print out the xsi:type in parenthesis.  This is used
      in several places including printing out Actions and cybox:Properties.
    -->
    <xsl:template match="@xsi:type"> (<xsl:value-of select="."/>)</xsl:template>
    
    <!--
      template to print out the list of related or related objects (prints
      the heading and call the template to print out actual related/associated
      objects).
    -->
    <xsl:template match="cybox:Related_Objects|cybox:Associated_Objects">
        <xsl:param name="idStack" select="()" />
        
        <xsl:variable name="relatedOrAssociated" select="if (local-name() = 'Related_Objects') then ('related') else if (local-name() = 'Associated_Objects') then ('associated') else ('other')" />
        <xsl:variable name="relatedOrAssociatedCapitalized" select="if (local-name() = 'Related_Objects') then ('Related') else if (local-name() = 'Associated_Objects') then ('Associated') else ('Other')" />
        <div class="container {$relatedOrAssociated}Objects">
            <div class="heading {$relatedOrAssociated}Objects">
                <xsl:value-of select="$relatedOrAssociatedCapitalized"/> Objects
            </div>
            <div class="contents {$relatedOrAssociated}Objects">
                <xsl:apply-templates select="cybox:Related_Object|cybox:Associated_Object">
                    <xsl:with-param name="idStack" select="$idStack" />
                </xsl:apply-templates>
            </div>
        </div>
    </xsl:template>

    <!--
      This is the consolidated Swiss Army knife template that prints object
      type data.
      
      This prints out objects that are:
       * Object
       * Event
       * Related Object
       * Associated Object
       
       It also prints out either original inline objects (with an id) or object references (with and idref).
    -->
    <xsl:template match="cybox:Object|cybox:Event|cybox:Related_Object|cybox:Associated_Object">
        <xsl:param name="idStack" select="()" />
        <xsl:param name="isObservableDirectChild" select="fn:true()" />
        <xsl:param name="includeHeading" select="fn:true()" />
        
        <xsl:variable name="localName" select="local-name()"/>
        <xsl:variable name="identifierName" select="if ($localName = 'Object') then 'object' else if ($localName = 'Event') then 'event' else if ($localName = 'Related_Object') then 'relatedObject' else if ($localName = 'Associated_Object') then 'associatedObject' else ''" />
        <xsl:variable name="friendlyName" select="fn:replace($localName, '_', ' ')" />
        <xsl:variable name="headingName" select="fn:upper-case($friendlyName)" />
        
        <xsl:variable name="idStack" select="$idStack, (fn:data(@id))"/>
        
        <xsl:variable name="debug" select="$debug"/>

        <xsl:if test="$debug = 'true'">
            <xsl:message>GENERIC OBJECT TEMPLATE current: id=<xsl:value-of select="@id"/> and idref=<xsl:value-of select="@idref"/> and object_reference=<xsl:value-of select="@object_reference" /> ### stack: <xsl:value-of select="fn:string-join($idStack, ',')" /></xsl:message>
        </xsl:if>

        <div class="container {$identifierName}Container {$identifierName}">
            <!--
              The following is important - it makes this object "linkable" with
              an id. This means the idref links can be resolved to show linked
              objects.  This is the object that will be highlighted when a link
              is clicked.
            -->
            <xsl:if test="@id and $includeHeading"><xsl:attribute name="id" select="@id"/></xsl:if>
            
            <!-- print out the actual object heading (name and xsi type) -->
            
                <div class="heading {$identifierName}Heading {$identifierName}">
                    <xsl:if test="@id and $includeHeading">
                       <xsl:call-template name="inlineObjectHeading">
                           <xsl:with-param name="currentObject" select="." />
                           <xsl:with-param name="relationshipOrAssociationType" select="cybox:Relationship|cybox:Association_Type"/>
                           <xsl:with-param name="id" select="@id"/>
                       </xsl:call-template>
                    </xsl:if>
                    <!--
                      If this "object" is an object reference (an "idref link")
                      print out the link that will jump to the original object.
                    -->
                    <xsl:if test="@idref">
                        
                        <xsl:variable name="targetId" select="string(@idref)"/>
                        <xsl:variable name="targetObject" select="//*[@id = $targetId]"/>
                        
                        <xsl:variable name="relationshipOrAssociationType" select="cybox:Relationship|cybox:Association_Type" />
                        
                        <xsl:call-template name="headerAndExpandableContent">
                            <xsl:with-param name="targetId" select="$targetId"/>
                            <xsl:with-param name="relationshipOrAssociationType" select="$relationshipOrAssociationType" />
                            <xsl:with-param name="idStack" select="$idStack" />
                        </xsl:call-template>
                        
                    </xsl:if>
                    
                </div>
            
            <div class="contents {$identifierName}Contents {$identifierName}">
                
                <!-- Print the description if one is available (often they are not) -->
                <xsl:if test="cybox:Description">
                    <div class="{$identifierName}Description description">
                        description: <xsl:value-of select="cybox:Description"/>
                    </div>
                </xsl:if>
                
                <!--
                  If this is an Event, we need to print out the list of Actions
                -->
                <xsl:if test="cybox:Actions/cybox:Action">
                    <div class="container">
                        <div class="heading actions">Actions</div>
                        <div class="contents actions">
                            <xsl:apply-templates select="cybox:Actions/cybox:Action">
                                <xsl:with-param name="idStack" select="$idStack" />
                            </xsl:apply-templates>
                        </div>
                    </div>
                </xsl:if>

                <!-- print out defined object type information if it's available -->
                <xsl:if test="cybox:Defined_Object/@xsi:type">
                    <div id="defined_object_type_label">defined object type: <xsl:value-of select="cybox:Defined_Object/@xsi:type"/></div>
                </xsl:if>

                <!--
                  print out the all-important cybox:Properties.  Lots of details in here!!
                -->
                <div>
                    <xsl:apply-templates select="cybox:Properties">
                        <xsl:with-param name="idStack" select="$idStack" />
                    </xsl:apply-templates>
                </div>
                
                <!--
                  Associated Objects need to have any Related Objects printed out
                -->
                <xsl:apply-templates select="cybox:Related_Objects">
                    <xsl:with-param name="idStack" select="$idStack" />
                </xsl:apply-templates>
            </div>
        </div>
        <xsl:if test="$debug = 'true'">
            <xsl:message>(end template) GENERIC OBJECT TEMPLATE current: id=<xsl:value-of select="@id"/> and idref=<xsl:value-of select="@idref"/> and object_reference=<xsl:value-of select="@object_reference" /></xsl:message>
        </xsl:if>
    </xsl:template>
    
    <!--
      Print the details of an action.
      
      TODO: Merge this into the master object template.
    -->
    <!-- <xsl:template name="processAction"> -->
    <xsl:template match="cybox:Action">
        <xsl:param name="idStack" select="()" />
        
        <xsl:variable name="idStack" select="$idStack, (@id)"/>
        
        <div class="container action">
            <div class="heading action">ACTION <xsl:value-of select="cybox:Type/text()" /> (xsi type: <xsl:value-of select="cybox:Type/@xsi:type" />)</div>
            <div class="contents action">
                <xsl:apply-templates select="cybox:Associated_Objects">
                    <xsl:with-param name="idStack" select="$idStack" />
                </xsl:apply-templates>
            </div>
        </div>
    </xsl:template>
    
    <!--
      Print out the details of cybox:Properties.
      
      For each property, print out the name, value, and constrains.
      
      Normally, the name is the element local name, the value is the text value
      of the context property element (all its descendent text nodes
      concatenated together), and the constrains is a list of all the
      attributes on the properties element (the element that is a direct
      child of cybox:Properties).
      
      This is customizable by writing custom templates for specific properties.
    -->
    <xsl:template match="cybox:Properties">
        <xsl:param name="idStack" select="()" />
        <fieldset>
            <legend>
                cybox properties
                (type: <xsl:value-of select="local-name-from-QName(fn:resolve-QName(fn:data(@xsi:type), .))"/>)
                <xsl:apply-templates select="@*[not(fn:QName(namespace-uri(), local-name()) = fn:QName('http://www.w3.org/2001/XMLSchema-instance', 'type'))]" mode="cyboxProperties" />
            </legend>
            <xsl:apply-templates select="*" mode="cyboxProperties">
                <xsl:with-param name="idStack" select="$idStack" />
            </xsl:apply-templates>
            
        </fieldset>
    </xsl:template>
    
    <!--
      Show email raw headers wrapped in a div with a class that is css styled
      to preserve wrapping in the original content.
    -->
    <xsl:template match="EmailMessageObj:Raw_Header/text()|EmailMessageObj:Raw_Body/text()" mode="cyboxProperties">
        <div class="verbatim">
            <xsl:value-of select="fn:data(.)" />
        </div>
    </xsl:template>
    
    <!--
      default template for outputting hierarchical cybox:Properties names/values/constraints
    -->
    <xsl:template match="element()" mode="cyboxProperties">
        <xsl:param name="idStack" select="()" />
        <div class="container cyboxPropertiesContainer cyboxProperties">
            <div class="heading cyboxPropertiesHeading cyboxProperties">
                <span class="cyboxPropertiesName"><xsl:value-of select="local-name()"/> </span>
                <span class="cyboxPropertiesConstraints"><xsl:apply-templates select="@*[not(node-name(.) = fn:QName('', 'object_reference'))][not(node-name(.) = fn:QName('http://www.w3.org/2001/XMLSchema-instance', 'type'))]" mode="#current"/></span>
                <span class="cyboxPropertiesNameValueSeparator"> &#x2192; </span>
                <span class="cyboxPropertiesValue">
                    <xsl:apply-templates select="text()" mode="#current"/>
                </span>
                <div class="cyboxPropertiesLink">
                    <xsl:apply-templates select="@*[node-name(.) = fn:QName('', 'object_reference')]" mode="#current">
                        <xsl:with-param name="idStack" select="$idStack"/>
                    </xsl:apply-templates>
                </div>
            </div>
            <div class="contents cyboxPropertiesContents cyboxProperties">
                <xsl:apply-templates select="*" mode="#current">
                    <xsl:with-param name="idStack" select="$idStack"/>
                </xsl:apply-templates>
            </div>
        </div>
    </xsl:template>
    
    <!--
      template to show text within cybox:Properties.  If the text is greater
      than a certain length, make this expandable, otherwise just show it as
      inline text.
      
      collapsed mode uses:
       * the css overflow property set to hiddent to only show the beginning
         of the text
       * "height: 1em" to show first line
       
       expanded mode uses:
       * clearing the display and height properties
       * "word-wrap: break-word" to force wrapping (particularly needed for
         binary base64 data)
    -->
    <xsl:template match="text()" mode="cyboxProperties">

        <xsl:variable name="default_collapse" select="$default_collapse"/>
        <xsl:variable name="collapse_class" select="if($default_collapse = 'none') then 'collapsed' else 'expanded'" />

        <xsl:choose>
            <xsl:when test="string-length() gt 200">
                <div class="longText expandableContainer expandableToggle expandableContents {$collapse_class} expandableSame" onclick="toggle(this)"><xsl:value-of select="fn:data(.)" /></div>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="fn:data(.)" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!--
      default template for printint out constraints associated with cybox:Properties entries
    -->
    <xsl:template match="attribute()" mode="cyboxProperties">
        <span class="cyboxPropertiesSingleConstraint">
          <xsl:if test="position() = 1"> [</xsl:if>
          <xsl:value-of select="local-name()"/>=<xsl:value-of select="fn:data(.)"/>
          <xsl:if test="position() != last()">, </xsl:if>
          <xsl:if test="position() = last()">]</xsl:if>
        </span>
    </xsl:template>

    <!--
       do not show the type on cybox:Properties entries
    -->
    <xsl:template match="@xsi:type" mode="cyboxProperties">
    </xsl:template>
    
    <!--
      print out object reference links
    -->
    <xsl:template match="@object_reference" mode="cyboxProperties">
        <xsl:param name="idStack" select="()" />
        <xsl:variable name="targetId" select="fn:data(.)"/>
        <xsl:variable name="targetObject" select="//*[@id = $targetId]"/>

        <xsl:variable name="debug" select="$debug"/>

        <xsl:if test="$debug = 'true'">
            <xsl:message>@object_reference TEMPLATE current: object_reference=<xsl:value-of select="fn:data(.)"/> ### stack: <xsl:value-of select="fn:string-join($idStack, ',')" /></xsl:message>
        </xsl:if>
        
        <xsl:variable name="relationshipOrAssociationType" select="()" />
        <xsl:call-template name="headerAndExpandableContent">
            <xsl:with-param name="targetId" select="$targetId"/>
            <xsl:with-param name="relationshipOrAssociationType" select="$relationshipOrAssociationType" />
            <xsl:with-param name="idStack" select="$idStack" />
        </xsl:call-template>

        <xsl:if test="$debug = 'true'">
            <xsl:message> (end template) @object_reference TEMPLATE current: object_reference=<xsl:value-of select="fn:data(.)"/> </xsl:message>
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>
