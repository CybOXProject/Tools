<?xml version="1.0" encoding="UTF-8"?>
<!--
CybOX XML to HTML transform v1.1
Compatible with CybOX v2.0 draft

Updated 2013-06-01
mcoarr@mitre.org

Updated 9/11/2012
ikirillov@mitre.org
-->


<xsl:stylesheet 
    version="2.0"
    xmlns:cybox="http://cybox.mitre.org/cybox-2"
    xmlns:Common="http://cybox.mitre.org/common-2"
    xmlns:ArtifactObj="http://cybox.mitre.org/objects#ArtifactObject-2"
    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:fn="http://www.w3.org/2005/xpath-functions"

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
    xmlns:WinProcessObj="http://cybox.mitre.org/objects#WinProcessObject-2">
    
<xsl:output method="html" omit-xml-declaration="yes" indent="yes" media-type="text/html" version="4.0" />
   <xsl:key name="observableID" match="cybox:Observable" use="@id"/>
    
    <xsl:template match="/">
            <html>
               <head>
                <title>CybOX Output</title>
                <style type="text/css">
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
                    
                    table.grid * {
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: 11px;
                    font-style: inherit;
                    vertical-align: top;
                    text-align: left;
                    }
                    
                    table.grid thead, table.grid .collapsible {
                    background-color: #c7c3bb;
                    }
                    
                    table.grid th {
                    color: #565770;
                    padding: 4px 16px 4px 0;
                    padding-left: 10px;
                    font-weight: bold;
                    } 
                    
                    table.grid td {
                    color: #565770;
                    padding: 4px 6px;
                    }

                    table.grid tr.even {
                    background-color: #EDEDE8;
                    }

                    body {
                    font: 11px Arial, Helvetica, sans-serif;
                    font-size: 13px;
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
                    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                    font-size: 11px;
                    color: #039;
                    }
                    #hor-minimalist-a
                    {
                    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                    font-size: 12px;
                    background: #fff;
                    margin: 0px;
                    border-collapse: collapse;
                    text-align: left;
                    width: 90%;
                    }
                    #hor-minimalist-a th
                    {
                    font-size: 11px;
                    font-weight: normal;
                    color: #039;
                    padding: 10px 8px;
                    border-bottom: 2px solid #6678b1;
                    }
                    #hor-minimalist-a td
                    {
                    color: #669;
                    padding: 9px 8px 0px 8px;
                    }
                    #hor-minimalist-a tbody tr:hover td
                    {
                    color: #009;
                    }
                    .one-column-emphasis
                    {
                    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                    font-size: 12px;
                    margin: 0px;
                    text-align: left;
                    border-collapse: collapse;
                    width: 100%;
                    }
                    .one-column-emphasis td
                    {
                    padding: 5px 10px;
                    color: #200;
                    border-top: 1px solid #e8edff;
                    border-right: 1px solid #e8edff;
                    border-bottom: 1px solid #e8edff;
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
                    border-right: 10px solid transparent;
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
                    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
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
                    }
                    table
                    {
                      empty-cells: show;
                    }
                </style>
                
                <script type="text/javascript">
                    //Collapse functionality
                    function toggleDiv(divid, spanID)
                    {
                      if(document.getElementById(divid).style.display == 'none')
                      {
                        document.getElementById(divid).style.display = 'block';
                        if(spanID)
                        {
                          document.getElementById(spanID).innerText = "-";
                        }
                      } // end of if-then
                      else
                      {
                        document.getElementById(divid).style.display = 'none';
                        if(spanID)
                        {
                          document.getElementById(spanID).innerText = "+";
                        }
                      } // end of else
                    } // end of function toggleDiv()
                </script>
<script type="text/javascript">
var currentTarget = null;
var previousTarget = null;

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

function findAndExpandTarget(targetElement)
{
    var currentAncestor = targetElement.parentNode;
    var isFound = false;
    while (currentAncestor != null &amp;&amp; !isFound)
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

</script>
               </head>
                <body>
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
                          <xsl:call-template name="processObservables"/>
                   </div>
                </body>
            </html>
    </xsl:template>
    
    <xsl:template name="processObservables">
      <xsl:for-each select="cybox:Observables">        
          <div id="observablesspandiv" style="font-weight:bold; margin:5px; color:#BD9C8C;">
            <TABLE class="grid tablesorter" cellspacing="0">
                <COLGROUP>
                    <COL width="90%"/>
                    <COL width="10%"/>
                </COLGROUP>
                <THEAD>
                    <TR>
                        <TH class="header">
                            ID
                        </TH>
                        <TH class="header">
                            Type
                        </TH>
                    </TR>
                </THEAD>
                <TBODY>
                    <xsl:for-each select="cybox:Observable">
                        <!-- <xsl:sort select="cybox:Observable_Composition" order="descending"/> -->
                        <xsl:variable name="evenOrOdd" select="if(position() mod 2 = 0) then 'even' else 'odd'" />
                        <xsl:call-template name="processObservable"><xsl:with-param name="evenOrOdd" select="$evenOrOdd"/></xsl:call-template>
                    </xsl:for-each>
                </TBODY>
            </TABLE>    
        </div>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="processObservable">
        <xsl:param name="evenOrOdd" />
        <xsl:variable name="contentVar" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
        <xsl:variable name="imgVar" select="generate-id()"/>
        <TR><xsl:attribute name="class"><xsl:value-of select="$evenOrOdd" /></xsl:attribute>
        <TD>
            <div id="fileObjAtt" class="collapsibleLabel" style="cursor: pointer;" onclick="toggleDiv('{$contentVar}','{$imgVar}')">
                <span id="{$imgVar}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span><xsl:value-of select="@id"/>
            </div>
        </TD>
        <TD>                    
            <xsl:choose>
                <xsl:when test="cybox:Observable_Composition">
                    Composition
                </xsl:when>
                <xsl:when test="cybox:Event">
                    Event
                </xsl:when>
                <xsl:when test="cybox:Object/cybox:Properties/@xsi:type">
                    <xsl:value-of select="fn:local-name-from-QName(fn:resolve-QName(cybox:Object/cybox:Properties/@xsi:type, cybox:Object/cybox:Properties))" />
                    <!-- <xsl:value-of select="fn:replace('Matthew E. Coarr', 'Matthew', 'Matt')" /> -->
                </xsl:when>
                <xsl:when test="cybox:Object/cybox:Properties/@xsi:type and not(cybox:Object/cybox:Properties/@xsi:type)">
                    Object (no properties set)
                </xsl:when>
                <xsl:otherwise>
                    Other
                </xsl:otherwise>
            </xsl:choose>
        </TD>
        </TR>
        <TR><xsl:attribute name="class"><xsl:value-of select="$evenOrOdd" /></xsl:attribute>
        <TD colspan="2">
          <div id="{$contentVar}"  class="collapsibleContent" style="overflow:hidden; display:none; padding:0px 7px;">
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
                                      <!-- <xsl:for-each select="cybox:Observable"> -->
                                          <xsl:call-template name="processPlainObservable"/>
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
                                          <xsl:call-template name="processObservableCompositionSimple"/>
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
    </xsl:template>
    
    <xsl:template name="processObservableCompositionSimple">
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
                                        <xsl:call-template name="processObservableInObservableCompositionSimple"/>
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
    
    <xsl:template name="clickableIdref">
        <xsl:param name="type"/>
        <xsl:param name="idref"/>
        (<xsl:value-of select="$type"/> reference:
        <xsl:element name="span">
            <xsl:attribute name="class">highlightTargetLink</xsl:attribute>
            <xsl:attribute name="onclick"><xsl:value-of select='concat("highlightTarget(&apos;", $idref, "&apos;)")'/></xsl:attribute>
            <xsl:value-of select="$idref"/>
        </xsl:element>
        )
    </xsl:template>

    <xsl:template name="processObservableInObservableCompositionSimple">
        <xsl:if test="@idref">
            <div class="foreignObservablePointer">
                <!-- <span><xsl:value-of select="@idref"/></span> -->
                <xsl:call-template name="clickableIdref">
                    <xsl:with-param name="type" select="'object'"/>
                    <xsl:with-param name="idref" select="@idref"/>
                </xsl:call-template>
            </div>
        </xsl:if>
        
        <xsl:for-each select="cybox:Observable_Composition">
            <xsl:call-template name="processObservableCompositionSimple" />
        </xsl:for-each>
        
   </xsl:template>
    
    
    
    <xsl:template name="processPlainObservable">
        <xsl:param name="span_var" select="generate-id()"/>
        <xsl:param name="div_var" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
        <xsl:if test="@id">
            <xsl:for-each select="cybox:Object">
                <xsl:call-template name="processObject">
                    <xsl:with-param name="div_var" select="$div_var"/>
                    <xsl:with-param name="span_var" select="$span_var"/>
                </xsl:call-template>
            </xsl:for-each>
            <xsl:for-each select="cybox:Event">
                <xsl:call-template name="processEvent">
                    <xsl:with-param name="div_var" select="$div_var"/>
                    <xsl:with-param name="span_var" select="$span_var"/>
                </xsl:call-template>
            </xsl:for-each>
        </xsl:if>
        
    </xsl:template>


    
    <xsl:template name="processAssociatedObjectSimple">
        <div class="container associatedObject associatedObjectContainer">
            <xsl:if test="@id">
                <xsl:attribute name="id" select="@id"/>
            </xsl:if>
            <div class="heading associatedObject">
                ASSOCIATED OBJECT <xsl:value-of select="@id" />
                <xsl:if test="cybox:Type/@xsi:type"> (xsi type: <xsl:value-of select="cybox:Type/@xsi:type" />)</xsl:if>
            </div>
            <div class="contents associatedObject">
                <div class="associatedObjectType">
                    <xsl:value-of select="cybox:Association_Type/text()"/><xsl:apply-templates select="cybox:Association_Type/@xsi:type"/>
                </div>
                
                <div class="associatedObjectDescription description">
                    <xsl:apply-templates select="cybox:Description"/>
                </div>
                
                <xsl:for-each select="cybox:Properties">
                    <xsl:call-template name="processProperties" />
                </xsl:for-each>
                
                <xsl:apply-templates select="cybox:Related_Objects" />
                
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="@xsi:type"> (<xsl:value-of select="."/>)</xsl:template>
    
    <xsl:template match="cybox:Related_Objects">
        <div class="container relatedObjects">
            <div class="heading relatedObjects">
                Related Objects
            </div>
            <div class="contents relatedObjects">
                <xsl:apply-templates select="cybox:Related_Object"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="cybox:Related_Object">
        <div class="container relatedObject">
            <div class="heading relatedObject">
                Related Object
            </div>
            <div class="contents relatedObject">
                <div>
                    <xsl:call-template name="clickableIdref">
                        <xsl:with-param name="type" select="'related object'"/>
                        <xsl:with-param name="idref" select="@idref"/>
                    </xsl:call-template>
                </div>
                <div>
                    via relationship: <xsl:value-of select="cybox:Relationship/text()"/>
                </div>
                <!-- <xsl:value-of select="@idref"/> via relationship: <xsl:value-of select="cybox:Relationship/text()"/> -->
            </div>
        </div>
    </xsl:template>
    
    
    <xsl:template name="processObject">
        <xsl:param name="span_var"/>
        <xsl:param name="div_var"/>
        <div class="objectContainer observableChildItemContainer">
            <xsl:attribute name="id" select="@id"/>
        <div id="object_label_div">
            <xsl:if test="@type"><div id="object_type_label">
                <xsl:value-of select="@type"/> Object </div>
            </xsl:if>
            
            <xsl:if test="cybox:Defined_Object/@xsi:type">
                <div id="defined_object_type_label"><xsl:value-of select="cybox:Defined_Object/@xsi:type"/></div>
            </xsl:if>
            
            <xsl:for-each select="cybox:Properties">
                <xsl:call-template name="processProperties"/>
            </xsl:for-each>
            
            <xsl:apply-templates select="cybox:Related_Objects"/>
        </div>
        
        </div>
    </xsl:template>
    
    <xsl:template name="processEvent">
        <xsl:param name="span_var"/>
        <xsl:param name="div_var"/>
        <div class="eventContainer observableChildItemContainer">
            <xsl:attribute name="id" select="@id"/>
            <div id="object_label_div">
                <xsl:if test="cybox:Type"><div class="eventTypeHeading" id="event_type_label">
                    <xsl:value-of select="cybox:Type/text()"/> Event (<xsl:value-of select="cybox:Type/@xsi:type"/>)</div>
                </xsl:if>
                
                <xsl:if test="cybox:Description">
                    <div class="eventDescription">
                        description: <xsl:value-of select="cybox:Description"/>
                    </div>
                </xsl:if>
                
                <xsl:if test="cybox:Actions/cybox:Action">
                    <div class="container">
                        <div class="heading actions">Actions</div>
                        <div class="contents actions">
                            <xsl:for-each select="cybox:Actions/cybox:Action">
                                <xsl:call-template name="processAction" />
                            </xsl:for-each>
                        </div>
                    </div>
                </xsl:if>
                
                <xsl:if test="cybox:Defined_Object/@xsi:type">
                    <div id="defined_object_type_label"><xsl:value-of select="cybox:Defined_Object/@xsi:type"/></div>
                </xsl:if>
                
                <xsl:for-each select="cybox:Properties">
                    <xsl:call-template name="processProperties"/>
                </xsl:for-each>
            </div>
            
        </div>
    </xsl:template>
    
    <xsl:template name="processAction">
        <div class="container action">
            <div class="heading action">ACTION <xsl:value-of select="cybox:Type/text()" /> (xsi type: <xsl:value-of select="cybox:Type/@xsi:type" />)</div>
            <div class="contents action">
                <xsl:for-each select="cybox:Associated_Objects/cybox:Associated_Object">
                    <xsl:call-template name="processAssociatedObjectSimple" />
                </xsl:for-each>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template name="processProperties">
        <xsl:apply-templates select="." />
    </xsl:template>

    <xsl:template match="cybox:Properties">
        <fieldset>
            <legend>cybox properties (type: <xsl:value-of select="@xsi:type"/>)</legend>
            <table>
                <thead><th>Name</th><th>Value</th><th>Constraints</th></thead>
                <xsl:for-each select="*">
                    <tr>
                        <td><xsl:value-of select="local-name()" /></td>
                        <td><xsl:apply-templates select="." /></td>
                        <td>
                            <xsl:for-each select="@*">
                                <div class="constraintItem"><xsl:value-of select="local-name()"/>: <xsl:value-of select="string(.)"/></div>
                            </xsl:for-each>
                            <!-- <xsl:if test="@condition"> (condition: <xsl:value-of select="@condition"/>)</xsl:if> -->
                        </td>
                    </tr>
                </xsl:for-each>
            </table>
            
        </fieldset>
    </xsl:template>
    
    <xsl:template match="ArtifactObj:Raw_Artifact">
        raw data omitted ["<xsl:value-of select='substring(text(), 1, 10)'/> ... <xsl:value-of select='substring(text(), string-length(text())-10, 10)'/>"; length: <xsl:value-of select="string-length()"/>]
    </xsl:template>
    
    <xsl:template match="ArtifactObj:Packaging">
        <!--packaging:--> <xsl:apply-templates />
    </xsl:template>
    
    <xsl:template match="ArtifactObj:Encoding">
        encoding algorithm is <xsl:value-of select="@algorithm"/>
    </xsl:template>
    
    <xsl:template match="AddressObj:Address_Value">
        <xsl:apply-templates />
        <xsl:if test="@pattern_type or @apply_condition">
            (pattern type: <xsl:value-of select="@pattern_type"/>; apply condition: <xsl:value-of select="@apply_condition"/>)
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="EmailMessageObj:Header">
        <ul>
            <xsl:apply-templates/>
        </ul>
    </xsl:template>
    
    <xsl:template match="EmailMessageObj:Header/*">
        <li><xsl:value-of select="local-name()" />: <xsl:apply-templates/></li>
    </xsl:template>
    
    <xsl:template match="EmailMessageObj:Recipient">
        <xsl:apply-templates/> (category: <xsl:value-of select="@category"/>)
    </xsl:template>
    
    <xsl:template match="EmailMessageObj:File|EmailMessageObj:Link">
        <div class="emailDiv">
          <xsl:apply-templates/>
          [<xsl:value-of select="local-name()"/>]
          (object reference:
            <xsl:element name="span">
                <xsl:attribute name="class">highlightTargetLink</xsl:attribute>
                <xsl:attribute name="onclick"><xsl:value-of select='concat("highlightTarget(&apos;", @object_reference, "&apos;)")'/></xsl:attribute>
                <xsl:value-of select="@object_reference"/>
            </xsl:element>
            )
        </div>
    </xsl:template>
    
    <xsl:template match="EmailMessageObj:Raw_Header">
        <div class="verbatim">
            <xsl:value-of select="text()" />
        </div>
    </xsl:template>
    
</xsl:stylesheet>
