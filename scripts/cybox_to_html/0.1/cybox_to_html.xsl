<?xml version="1.0" encoding="UTF-8"?>
<!--
CybOX XML to HTML transform v0.1
Compatible with CybOX v1.0 draft

Updated 9/11/2012
ikirillov@mitre.org
-->


<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:cybox="http://cybox.mitre.org/cybox_v1"
    xmlns:Common="http://cybox.mitre.org/Common_v1"
    xmlns:SystemObj="http://cybox.mitre.org/objects#SystemObject"
    xmlns:FileObj="http://cybox.mitre.org/objects#FileObject"
    xmlns:ProcessObj="http://cybox.mitre.org/objects#ProcessObject"
    xmlns:PipeObj="http://cybox.mitre.org/objects#PipeObject" 
    xmlns:PortObj="http://cybox.mitre.org/objects#PortObject" 
    xmlns:AddressObj="http://cybox.mitre.org/objects#AddressObject"
    xmlns:SocketObj="http://cybox.mitre.org/objects#SocketObject"
    xmlns:MutexObj="http://cybox.mitre.org/objects#MutexObject"
    xmlns:MemoryObj="http://cybox.mitre.org/objects#MemoryObject"
    xmlns:URIObj="http://cybox.mitre.org/objects#URIObject"
    xmlns:LibraryObj="http://cybox.mitre.org/objects#LibraryObject"
    xmlns:EmailMessageObj="http://cybox.mitre.org/objects#EmailMessageObject"
    xmlns:WinHandleObj="http://cybox.mitre.org/objects#WinHandleObject"
    xmlns:WinMutexObj="http://cybox.mitre.org/objects#WinMutexObject"
    xmlns:WinServiceObj="http://cybox.mitre.org/objects#WinServiceObject"
    xmlns:WinRegistryKeyObj="http://cybox.mitre.org/objects#WinRegistryKeyObject"
    xmlns:WinPipeObj="http://cybox.mitre.org/objects#WinPipeObject"
    xmlns:WinDriverObj="http://cybox.mitre.org/objects#WinDriverObject"
    xmlns:WinFileObj="http://cybox.mitre.org/objects#WinFileObject"
    xmlns:WinExecutableFileObj="http://cybox.mitre.org/objects#WinExecutableFileObject"
    xmlns:WinProcessObj="http://cybox.mitre.org/objects#WinProcessObject">
    
<xsl:output method="html" omit-xml-declaration="yes" indent="no" media-type="text/html"/>
   <xsl:key name="observableID" match="cybox:Observable" use="@id"/>
    
    <xsl:template match="/">
            <html>
                <title>CybOX Output</title>
                <STYLE type="text/css">
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
                    font: 11px Arial, Helvetica, sans-serif;
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
                    #one-column-emphasis
                    {
                    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                    font-size: 12px;
                    margin: 0px;
                    text-align: left;
                    border-collapse: collapse;
                    }
                    #one-column-emphasis td
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
                    display: inline;
                    width: 30%;
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
                </STYLE>
                
                <SCRIPT type="text/javascript">
                    //Collapse functionality
                    function toggleDiv(divid, spanID){
                    if(document.getElementById(divid).style.display == 'none'){
                    document.getElementById(divid).style.display = 'block';
                    if(spanID){
                    document.getElementById(spanID).innerText = "-";
                    }
                    }else{
                    document.getElementById(divid).style.display = 'none';
                    if(spanID){
                    document.getElementById(spanID).innerText = "+";
                    }
                    }
                    }
                </SCRIPT>
                <head/>
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
                                    <TD><xsl:value-of select="current-date()"/></TD>
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
            <TABLE class="grid tablesorter" cellspacing="0" style="width: auto;">
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
                            Has Composition
                        </TH>
                    </TR>
                </THEAD>
                <TBODY>
                    <xsl:for-each select="cybox:Observable">
                        <xsl:sort select="cybox:Observable_Composition" order="descending"/>
                        <xsl:choose>
                            <xsl:when test="position() mod 2">
                                <TR class="odd">
                                    <xsl:call-template name="processObservable"/>
                                </TR>
                            </xsl:when>
                            <xsl:otherwise>
                                <TR class="even">
                                    <xsl:call-template name="processObservable"/>
                                </TR>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </TBODY>
            </TABLE>    
        </div>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="processObservable">
        <TD>
            <xsl:variable name="contentVar" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
            <xsl:variable name="imgVar" select="generate-id()"/>
            <div id="fileObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$contentVar}','{$imgVar}')">
                <span id="{$imgVar}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span><xsl:value-of select="@id"/>
            </div>
          <div id="{$contentVar}" style="overflow:hidden; display:none; padding:0px 7px;">
                <xsl:if test="cybox:Title">
                    <br/>
                    <div id="section">
                        <table id="one-column-emphasis">
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
              <xsl:if test="cybox:Observable_Composition">
                  <br/>
                  <div id="section">
                      <table id="one-column-emphasis">
                          <colgroup>
                              <col class="oce-first-obs" />
                          </colgroup>
                          <tbody>
                              <tr>
                                  <td>Observable Composition</td>
                                  <td>
                                      <xsl:for-each select="cybox:Observable_Composition">
                                          <xsl:call-template name="processObservableComposition"/>
                                      </xsl:for-each>
                                  </td>
                              </tr>
                          </tbody>
                      </table> 
                  </div>
              </xsl:if>
             <xsl:if test="cybox:Stateful_Measure">
                    <br/>
                    <div id="section">
                        <table id="one-column-emphasis">
                            <colgroup>
                                <col class="oce-first-obs" />
                            </colgroup>
                            <tbody>
                                <tr>
                                    <td>Stateful Measure</td>
                                    <td>
                                        <xsl:for-each select="cybox:Stateful_Measure">
                                            <xsl:call-template name="processStatefulMeasure">
                                                <xsl:with-param name="div_var" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
                                                <xsl:with-param name="span_var" select="generate-id()"/>
                                            </xsl:call-template>
                                        </xsl:for-each>
                                    </td>
                                </tr>
                            </tbody>
                        </table> 
                    </div>
                </xsl:if>
            </div>
        </TD>
        <TD>                    
            <xsl:choose>
                <xsl:when test="cybox:Observable_Composition">
                    Yes
                </xsl:when>
                <xsl:otherwise>
                    No
                </xsl:otherwise>
            </xsl:choose>
        </TD>
    </xsl:template>
    
    <xsl:template name="processObservableComposition">
        <table id="one-column-emphasis">
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
                    <td><span style="font-weight:bold; margin:5px; color:#BD9C8C;"><xsl:value-of select="@operator"/></span></td>
                    <td>
                        <xsl:for-each select="cybox:Observable">
                            <xsl:call-template name="processObscompObservable"/>
                        </xsl:for-each>
                    </td>
                </tr>
            </tbody>
        </table> 
    </xsl:template>
    
    <xsl:template name="processObscompObservable">
        <xsl:param name="span_var" select="generate-id()"/>
        <xsl:param name="div_var" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
        <xsl:if test="@id">
            <xsl:if test="cybox:Stateful_Measure">
                <xsl:for-each select="cybox:Stateful_Measure">
                    <xsl:call-template name="processStatefulMeasure">
                        <xsl:with-param name="div_var" select="$div_var"/>
                        <xsl:with-param name="span_var" select="$span_var"/>
                    </xsl:call-template>
                </xsl:for-each>
            </xsl:if>
            <xsl:if test="cybox:Observable_Composition">
                <xsl:for-each select="cybox:Observable_Composition">
                    <xsl:call-template name="processObservableComposition"/>
                </xsl:for-each>
            </xsl:if>
        </xsl:if>
        <xsl:if test="@idref">
            <xsl:for-each select="key('observableID',@idref)">
                <xsl:if test="cybox:Stateful_Measure">
                    <xsl:for-each select="cybox:Stateful_Measure">
                        <xsl:call-template name="processStatefulMeasure">
                            <xsl:with-param name="div_var" select="$div_var"/>
                            <xsl:with-param name="span_var" select="$span_var"/>
                        </xsl:call-template>
                    </xsl:for-each>
                </xsl:if>
            </xsl:for-each>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processStatefulMeasure">
        <xsl:param name="span_var"/>
        <xsl:param name="div_var"/>
        <xsl:if test="cybox:Object/cybox:Defined_Object">
          <xsl:for-each select="cybox:Object">
              <xsl:call-template name="processObject">
                  <xsl:with-param name="div_var" select="$div_var"/>
                  <xsl:with-param name="span_var" select="$span_var"/>
              </xsl:call-template>
          </xsl:for-each>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processCyboxValue">
        <xsl:choose>
            <xsl:when test="@condition or @start_range or @end_range or @pattern_type or @regex_syntax or @appears_random">
                <table id="hor-minimalist-a">
                    <thead>
                        <tr>
                            <xsl:if test="@condition">
                                <th scope="col">Condition</th>
                            </xsl:if>
                            <xsl:if test="@condition != 'IsInRange'">
                                <th scope="col">Value</th>
                            </xsl:if>
                            <xsl:if test="@start_range">
                                <th scope="col">Start Range</th>
                            </xsl:if>
                            <xsl:if test="@end_range">
                                <th scope="col">End Range</th>
                            </xsl:if>
                            <xsl:if test="@pattern_type">
                                <th scope="col">Pattern Type</th>
                            </xsl:if>
                            <xsl:if test="@regex_syntax">
                                <th scope="col">Regex Syntax</th>
                            </xsl:if>
                            <xsl:if test="@appears_random">
                                <th scope="col">Appears Random</th>
                            </xsl:if>
                        </tr>
                    </thead>
                    <TR>
                        <xsl:if test="@condition">
                            <TD><xsl:value-of select="@condition"/></TD>
                        </xsl:if>
                        <xsl:if test="@condition != 'IsInRange'">
                            <TD><xsl:value-of select="."/></TD>
                        </xsl:if>
                        <xsl:if test="@start_range">
                            <TD><xsl:value-of select="@start_range"/></TD>
                        </xsl:if>
                        <xsl:if test="@end_range">
                            <TD><xsl:value-of select="@end_range"/></TD>
                        </xsl:if>
                        <xsl:if test="@pattern_type">
                            <TD><xsl:value-of select="@pattern_type"/></TD>
                        </xsl:if>
                        <xsl:if test="@regex_syntax">
                            <TD><xsl:value-of select="@regex_syntax"/></TD>
                        </xsl:if>
                        <xsl:if test="@appears_random">
                            <TD><xsl:value-of select="@appears_random"/></TD>
                        </xsl:if>
                    </TR>   
                </table>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="processContributor">
        <xsl:if test="Common:Name">
            <tr>
                <td>Name</td>
                <td><xsl:value-of select="Common:Name"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Organization">
            <tr>
                <td>Organization</td>
                <td><xsl:value-of select="Common:Organization"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Role">
            <tr>
                <td>Role</td>
                <td><xsl:value-of select="Common:Role"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Email">
            <tr>
                <td>Email Address</td>
                <td><xsl:value-of select="Common:Email"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Date">
            <tr>
                <td>Date</td>
                <td><xsl:value-of select="Common:Date"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Phone">
            <tr>
                <td>Phone Number</td>
                <td><xsl:value-of select="Common:Phone"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Contribution_Location">
            <tr>
                <td>Contribution Location</td>
                <td><xsl:value-of select="Common:Contribution_Location"/></td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processToolInformation">
        <xsl:if test="Common:Name">
            <tr>
                <td>Name</td>
                <td><xsl:value-of select="Common:Name"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Version">
            <tr>
                <td>Version</td>
                <td><xsl:value-of select="Common:Version"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Vendor">
            <tr>
                <td>Vendor</td>
                <td><xsl:value-of select="Common:Vendor"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Service_Pack">
            <tr>
                <td>Service Pack</td>
                <td><xsl:value-of select="Common:Service_Pack"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Tool_Hashes">
            <tr>
                <td>Tool Hashes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Tool_Hashes/Common:Hash">
                                <xsl:call-template name="processHash"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Tool_Configuration">
            <tr>
                <td>Tool Configuration</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Tool_Configuration">
                                <xsl:call-template name="processToolConfiguration"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processToolConfiguration">
        <xsl:if test="Common:Configuration_Settings">
            <tr>
                <td>Configuration Settings</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Configuration_Settings/Common:Configuration_Setting">
                                <xsl:call-template name="processConfigurationSetting"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Dependencies">
            <tr>
                <td>Dependencies</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Dependencies/Common:Dependency">
                                <xsl:call-template name="processDependency"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Usage_Context_Assumptions">
            <tr>
                <td>Usage Context Assumptions</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Usage_Context_Assumptions/Common:Usage_Context_Assumption">
                                <xsl:call-template name="processStructuredTextGroup"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Internationalization_Settings">
            <tr>
                <td>Internationalization Settings</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Internationalization_Settings/Common:InternalStrings">
                                <xsl:call-template name="processInternalStrings"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Information">
            <tr>
                <td>Build Information</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Build_Information">
                                <xsl:call-template name="processBuildInformation"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processInternalStrings">
        <xsl:if test="Common:Key">
            <tr>
                <td>Key</td>
                <td><xsl:value-of select="Common:Key"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Content">
            <tr>
                <td>Content</td>
                <td><xsl:value-of select="Common:Content"/></td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processBuildInformation">
        <xsl:if test="Common:Build_ID">
            <tr>
                <td>Build ID</td>
                <td><xsl:value-of select="Common:Build_ID"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Project">
            <tr>
                <td>Build Project</td>
                <td><xsl:value-of select="Common:Build_Project"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Utility">
            <tr>
                <td>Build Utility</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Build_Utility">
                                <xsl:call-template name="processBuildUtility"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Version">
            <tr>
                <td>Build Version</td>
                <td><xsl:value-of select="Common:Build_Version"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Label">
            <tr>
                <td>Build Label</td>
                <td><xsl:value-of select="Common:Build_Label"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Compilation_Date">
            <tr>
                <td>Compilation Date</td>
                <td><xsl:value-of select="Common:Compilation_Date"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Compilers">
            <tr>
                <td>Compilers</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Compilers/Common:Compiler">
                                <xsl:call-template name="processCompiler"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Configuration">
            <tr>
                <td>Build Configuration</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Build_Configuration">
                                <xsl:call-template name="processBuildConfiguration"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Script">
            <tr>
                <td>Build Script</td>
                <td><xsl:value-of select="Common:Build_Script"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Libraries">
            <tr>
                <td>Libraries</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Libraries/Common:Library">
                                <xsl:call-template name="processLibrary"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Output_Log">
            <tr>
                <td>Build Output Log</td>
                <td><xsl:value-of select="Common:Build_Output_Log"/></td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processLibrary">
        <xsl:if test="@name">
            <tr>
                <td>Name</td>
                <td><xsl:value-of select="@name"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="@version">
            <tr>
                <td>Version</td>
                <td><xsl:value-of select="@version"/></td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processBuildConfiguration">
        <xsl:if test="Common:Configuration_Setting_Description">
            <tr>
                <td>Configuration Setting Description</td>
                <td><xsl:value-of select="Common:Configuration_Setting_Description"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Configuration_Settings">
            <tr>
                <td>Configuration Settings</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Configuration_Settings/Common:Configuration_Setting">
                                <xsl:call-template name="processConfigurationSetting"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processCompiler">
        <xsl:if test="Common:Compiler_Informal_Description">
            <tr>
                <td>Compiler Informal Description</td>
                <td><xsl:value-of select="Common:Compiler_Informal_Description"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Compiler_CPE_Specification">
            <tr>
                <td>Compiler CPE Specification</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Compiler_CPE_Specification">
                                <xsl:call-template name="processCPESpecification"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processBuildUtility">
        <xsl:if test="Common:Build_Utility_Name">
            <tr>
                <td>Build Utility Name</td>
                <td><xsl:value-of select="Common:Build_Utility_Name"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Build_Utility_CPE_Specification">
            <tr>
                <td>Build Utility</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Build_Utility_CPE_Specification">
                                <xsl:call-template name="processCPESpecification"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processCPESpecification">
        <xsl:if test="Common:CPE_Name">
            <tr>
                <td>CPE Name</td>
                <td><xsl:value-of select="Common:CPE_Name"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Title">
            <tr>
                <td>Title</td>
                <td><xsl:value-of select="Common:Title"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Meta_Item_Metadata">
            <tr>
                <td>Meta Item Metadata</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Meta_Item_Metadata">
                                <xsl:call-template name="processMetaItemMetadata"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processMetaItemMetadata">
        <xsl:if test="Common:Modification_Date">
            <tr>
                <td>Modification Data</td>
                <td><xsl:value-of select="Common:Modification_Date"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:NVD_ID">
            <tr>
                <td>NVD ID</td>
                <td><xsl:value-of select="Common:NVD_ID"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Status">
            <tr>
                <td>Status</td>
                <td><xsl:value-of select="Common:Status"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:XMLNS_Meta">
            <tr>
                <td>XMLNS Meta</td>
                <td><xsl:value-of select="Common:XMLNS_Meta"/></td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processConfigurationSetting">
        <xsl:if test="Common:Item_Name">
            <tr>
                <td>Item Name</td>
                <td><xsl:value-of select="Common:Item_Name"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Item_Value">
            <tr>
                <td>Item Value</td>
                <td><xsl:value-of select="Common:Item_Value"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Item_Type">
            <tr>
                <td>Item Type</td>
                <td><xsl:value-of select="Common:Item_Type"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Item_Description">
            <tr>
                <td>Item Description</td>
                <td><xsl:value-of select="Common:Item_Description"/></td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processDependency">
        <xsl:if test="Common:Dependency_Type">
            <tr>
                <td>Type</td>
                <td><xsl:value-of select="Common:Dependency_Type"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Dependency_Description">
            <tr>
                <td>Description</td>
                <td><xsl:value-of select="Common:Dependency_Description"/></td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processDefinedObject">
        <xsl:param name="span_var"/>
        <xsl:param name="div_var"/>
        <xsl:choose>
            <xsl:when test="@xsi:type='FileObj:FileObjectType'">
                <div id="fileObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> File Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processFileObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinFileObj:WindowsFileObjectType'">
                <div id="winFileObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows File Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processFileObject"/>
                    <xsl:call-template name="processWinFileObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinExecutableFileObj:WindowsExecutableFileObjectType'">
                <div id="winExecFileObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows Executable File Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processFileObject"/>
                    <xsl:call-template name="processWinFileObject"/>
                    <xsl:call-template name="processWinExecutableFileObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinRegistryKeyObj:WindowsRegistryKeyObjectType'">
                <div id="winRegKeyObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows Registry Key Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processWinRegistryKeyObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='ProcessObj:ProcessObjectType'">
                <div id="processObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Process Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processProcessObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinProcessObj:WindowsProcessObjectType'">
                <div id="winProcessObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows Process Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processProcessObject"/>
                    <xsl:call-template name="processWinProcessObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinServiceObj:WindowsServiceObjectType'">
                <div id="winServiceObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows Service Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processProcessObject"/>
                    <xsl:call-template name="processWinProcessObject"/>
                    <xsl:call-template name="processWinServiceObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinDriverObj:WindowsDriverObjectType'">
                <div id="winDriverObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows Driver Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processWinDriverObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='PipeObj:PipeObjectType'">
                <div id="pipeObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Pipe Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processPipeObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='PortObj:PortObjectType'">
                <div id="portObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Port Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processPortObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='AddressObj:AddressObjectType'">
                <div id="addressObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Address Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processAddressObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinPipeObj:WindowsPipeObjectType'">
                <div id="winPipeObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows Pipe Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processPipeObject"/>
                    <xsl:call-template name="processWinPipeObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='MutexObj:MutexObjectType'">
                <div id="mutexObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Mutex Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processMutexObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinMutexObj:WindowsMutexObjectType'">
                <div id="winMutexObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows Mutex Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processMutexObject"/>
                    <xsl:call-template name="processWinMutexObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='WinPipeObj:WindowsPipeObjectType'">
                <div id="winPipeObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Windows Pipe Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processPipeObject"/>
                    <xsl:call-template name="processWinPipeObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='SocketObj:SocketObjectType'">
                <div id="socketObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Socket Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processSocketObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='URIObj:URIObjectType'">
                <div id="uriObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> URI Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processURIObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='LibraryObj:LibraryObjectType'">
                <div id="libraryObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Library Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processLibraryObject"/>
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='EmailMessageObj:EmailMessageObjectType'">
                <div id="emailmsgObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Email Message Object Attributes
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <br/>
                    <xsl:call-template name="processEmailMessageObject"/>
                </div>
            </xsl:when>
            <xsl:otherwise>
                <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">Unsupported Object Type</span> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="processDefinedEffect">
        <xsl:param name="span_var" select="generate-id()"/>
        <xsl:param name="div_var" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
        <xsl:choose>
            <xsl:when test="@xsi:type='cybox:DataReadEffectType'">
                <div id="effect" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Data Read (effect)
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="cybox:Data">
                                <xsl:call-template name="processDataSegment"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='cybox:DataReceivedEffectType'">
                <div id="effect" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Data Received (effect)
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="cybox:Data">
                                <xsl:call-template name="processDataSegment"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='cybox:DataSentEffectType'">
                <div id="effect" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Data Sent (effect)
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="cybox:Data">
                                <xsl:call-template name="processDataSegment"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='cybox:DataWrittenEffectType'">
                <div id="effect" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Data Written (effect)
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="cybox:Data">
                                <xsl:call-template name="processDataSegment"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='cybox:PropertyReadEffectType'">
                <div id="effect" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Property Read (effect)
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:if test="cybox:Name">
                                <tr>
                                    <td>Name</td>
                                    <td><xsl:value-of select="cybox:Name"/></td>
                                </tr>
                            </xsl:if>
                            <xsl:if test="cybox:Value">
                                <tr>
                                    <td>Value</td>
                                    <td><xsl:value-of select="cybox:Value"/></td>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table> 
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='cybox:SendControlCodeEffectType'">
                <div id="effect" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Control Code Sent (effect)
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:if test="cybox:Control_Code">
                                <tr>
                                    <td>Control Code</td>
                                    <td><xsl:value-of select="cybox:Control_Code"/></td>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table> 
                </div>
            </xsl:when>
            <xsl:when test="@xsi:type='cybox:ValuesEnumeratedEffectType'">
                <div id="effect" style="cursor: pointer;" onclick="toggleDiv('{$div_var}','{$span_var}')">
                    <span id="{$span_var}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> Values Enumerated (effect)
                </div>
                <div id="{$div_var}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="cybox:Values/cybox:Value">
                                <tr>
                                    <td>Value</td>
                                    <td><xsl:value-of select="cybox:Value"/></td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </div>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="processDataSegment">
        <xsl:if test="Common:Data_Format">
            <tr>
                <td>Data Format</td>
                <td>
                    <xsl:for-each select="Common:Data_Format">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Data_Size">
            <tr>
                <td>Data Size</td>
                <td>
                    <xsl:for-each select="Common:Data_Size">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Data_Segment">
            <tr>
                <td>Data Segment</td>
                <td>
                    <xsl:for-each select="Common:Data_Segment">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Offset">
            <tr>
                <td>Offset</td>
                <td>Data Segment</td>
                <td>
                    <xsl:for-each select="Common:Offset">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Search_Distance">
            <tr>
                <td>Search Distance</td>
                <td>
                    <xsl:for-each select="Common:Search_Distance">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Search_Within">
            <tr>
                <td>Search Within</td>
                <td>
                    <xsl:for-each select="Common:Search_Within">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>

    <xsl:template name="processAssociatedObject">
        <xsl:param name="span_var" select="generate-id()"/>
        <xsl:param name="div_var" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
        <xsl:choose>
            <xsl:when test="@idref">
                <xsl:if test="@association_type">
                    <div id="associated_object_label"><xsl:value-of select="@association_type"/> Object</div>
                </xsl:if>
                <xsl:for-each select="key('objectID',@idref)">
                    <xsl:call-template name="processObject">
                        <xsl:with-param name="div_var" select="$div_var"/>
                        <xsl:with-param name="span_var" select="$span_var"/>
                    </xsl:call-template>
                </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
                <xsl:if test="@association_type">
                    <div id="associated_object_label"><xsl:value-of select="@association_type"/> Object</div>
                </xsl:if>
                <xsl:call-template name="processObject">
                    <xsl:with-param name="div_var" select="$div_var"/>
                    <xsl:with-param name="span_var" select="$span_var"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="processObj">
            <TD>
                <xsl:variable name="contentVar" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
                <xsl:variable name="imgVar" select="generate-id()"/>
                <div id="fileObjAtt" style="cursor: pointer;" onclick="toggleDiv('{$contentVar}','{$imgVar}')">
                    <span id="{$imgVar}" style="font-weight:bold; margin:5px; color:#BD9C8C;">+</span> <xsl:value-of select="@type"/>
                </div>
                <div id="{$contentVar}" style="overflow:hidden; display:none; padding:0px 7px;">
                    <xsl:for-each select="cybox:Defined_Object">
                        <xsl:call-template name="processDefinedObject">
                            <xsl:with-param name="div_var" select="concat(count(ancestor::node()), '00000000', count(preceding::node()))"/>
                            <xsl:with-param name="span_var" select="generate-id()"/>
                        </xsl:call-template>
                    </xsl:for-each>
                </div>
            </TD>
            <TD>                    
                <xsl:choose>
                    <xsl:when test="cybox:Defined_Object">
                        <xsl:value-of select="cybox:Defined_Object/@xsi:type"/>
                    </xsl:when>
                    <xsl:otherwise>
                        N/A
                    </xsl:otherwise>
                </xsl:choose>
            </TD>
        
    </xsl:template>
    
    <xsl:template name="processObject">
        <xsl:param name="span_var"/>
        <xsl:param name="div_var"/>
        <div id="object_label_div">
            <xsl:if test="@type"><div id="object_type_label">
                <xsl:value-of select="@type"/> Object </div>
            </xsl:if>
            
            <xsl:if test="cybox:Defined_Object/@xsi:type">
                <div id="defined_object_type_label"><xsl:value-of select="cybox:Defined_Object/@xsi:type"/></div>
            </xsl:if>
        </div>
        <div id="container">
            <xsl:if test="cybox:Defined_Object">
                <xsl:for-each select="cybox:Defined_Object">
                    <xsl:call-template name="processDefinedObject">
                        <xsl:with-param name="div_var" select="$div_var"/>
                        <xsl:with-param name="span_var" select="$span_var"/>
                    </xsl:call-template>
                </xsl:for-each>
            </xsl:if>
            <xsl:if test="cybox:Defined_Effect">
                <xsl:for-each select="cybox:Defined_Effect">
                    <xsl:call-template name="processDefinedEffect"/>
                </xsl:for-each>
            </xsl:if>
        </div>
    </xsl:template>

    <xsl:template name="processWinExecutableFileObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="WinExecutableFileObj:Peak_Code_Entropy">
                    <tr>
                        <td>Peak Code Entropy</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:call-template name="processPeakCodeEntropy"/>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinExecutableFileObj:PE_Attributes">
                    <tr>
                        <td>PE Attributes</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinExecutableFileObj:PE_Attributes">
                                        <xsl:call-template name="processPEAttributes"/>
                                    </xsl:for-each>
                                </tbody>
                            </table>                             
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processWinHandleObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="WinHandleObj:ID">
                    <tr>
                        <td>ID</td>
                        <td>
                            <xsl:for-each select="WinHandleObj:ID">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinHandleObj:Name">
                    <tr>
                        <td>Name</td>
                        <td>
                            <xsl:for-each select="WinHandleObj:Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinHandleObj:Type">
                    <tr>
                        <td>Type</td>
                        <td>
                            <xsl:for-each select="WinHandleObj:Type">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinHandleObj:Object_Address">
                    <tr>
                        <td>Object Address</td>
                        <td>
                            <xsl:for-each select="WinHandleObj:Object_Address">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinHandleObj:Access_Mask">
                    <tr>
                        <td>Access Mask</td>
                        <td>
                            <xsl:for-each select="WinHandleObj:Access_Mask">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinHandleObj:Pointer_Count">
                    <tr>
                        <td>Pointer Count</td>
                        <td>
                            <xsl:for-each select="WinHandleObj:Pointer_Count">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processPipeObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@named">
                    <tr>
                        <td>Named</td>
                        <td><xsl:value-of select="@named"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="PipeObj:Name">
                    <tr>
                        <td>Name</td>
                        <td>
                            <xsl:for-each select="PipeObj:Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processMutexObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@named">
                    <tr>
                        <td>Named</td>
                        <td><xsl:value-of select="@named"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="MutexObj:Name">
                    <tr>
                        <td>Name</td>
                        <td>
                            <xsl:for-each select="MutexObj:Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processWinMutexObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="WinMutexObj:Handle">
                    <tr>
                        <td>Handle</td>
                        <td>
                            <xsl:for-each select="WinMutexObj:Handle">
                                <xsl:call-template name="processWinHandleObject"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinMutexObj:Security_Attributes">
                    <tr>
                        <td>Security Attributes</td>
                        <td>
                            <xsl:for-each select="WinMutexObj:Security_Attributes">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processMemoryObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@is_injected">
                    <tr>
                        <td>Is Injected</td>
                        <td><xsl:value-of select="@is_injected"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="@is_mapped">
                    <tr>
                        <td>Is Mapped</td>
                        <td><xsl:value-of select="@is_mapped"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="@is_protected">
                    <tr>
                        <td>Is Protected</td>
                        <td><xsl:value-of select="@is_protected"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="MemoryObj:Hashes">
                    <tr>
                        <td>Hashes</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="MemoryObj:Hashes/Common:Hash">
                                        <xsl:call-template name="processHash"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="MemoryObj:Name">
                    <tr>
                        <td>Name</td>
                        <td>
                            <xsl:for-each select="MemoryObj:Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="MemoryObj:Region_Size">
                    <tr>
                        <td>Region Size</td>
                        <td>
                            <xsl:for-each select="MemoryObj:Region_Size">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="MemoryObj:Region_Start_Address">
                    <tr>
                        <td>Region Start Address</td>
                        <td>
                            <xsl:for-each select="MemoryObj:Region_Start_Address">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processPortObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="PortObj:Port_Value">
                    <tr>
                        <td>Port Number</td>
                        <td>
                            <xsl:for-each select="PortObj:Port_Value">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="PortObj:Layer4_Protocol">
                    <tr>
                        <td>Layer 4 Protocol</td>
                        <td>
                            <xsl:for-each select="PortObj:Layer4_Protocol">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processURIObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@type">
                    <tr>
                        <td>URI Type</td>
                        <td><xsl:value-of select="@type"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="URIObj:Value">
                    <tr>
                        <td>URI Value</td>
                        <td>
                            <xsl:for-each select="URIObj:Value">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processEmailMessageObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="EmailMessageObj:Attachments">
                    <tr>
                        <td>Attachments</td>
                        <td>                    
                            <table id="one-column-emphasis">
                            <colgroup>
                                <col class="oce-first-inner" />
                            </colgroup>
                            <tbody>
                                <xsl:for-each select="EmailMessageObj:Attachments/EmailMessageObj:File">
                                    <tr>
                                        <td>File</td>
                                        <td><xsl:call-template name="processFileObject"/></td>
                                    </tr>                    
                                </xsl:for-each>
                            </tbody>
                        </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="EmailMessageObj:Header">
                    <tr>
                        <td>Header</td>
                        <td>                    
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="EmailMessageObj:Header">
                                        <xsl:call-template name="processEmailHeader"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="EmailMessageObj:Optional_Header">
                    <tr>
                        <td>Optional Header</td>
                        <td>   
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="EmailMessageObj:Optional_Header">
                                        <xsl:call-template name="processEmailOptionalHeader"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="EmailMessageObj:Email_Server">
                    <tr>
                        <td>Email Server</td>
                        <td>
                            <xsl:for-each select="EmailMessageObj:Email_Server">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="EmailMessageObj:Raw_Body">
                    <tr>
                        <td>Raw Body</td>
                        <td>
                            <xsl:for-each select="EmailMessageObj:Raw_Body">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="EmailMessageObj:Raw_Header">
                    <tr>
                        <td>Raw Header</td>
                        <td>
                            <xsl:for-each select="EmailMessageObj:Raw_Header">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processEmailOptionalHeader">
        <xsl:if test="EmailMessageObj:Boundary">
            <tr>
                <td>Boundary</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Boundary">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:Content-Type">
            <tr>
                <td>Content-Type</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Content-Type">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:MIME-Version">
            <tr>
                <td>MIME-Version</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:MIME-Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:Precedence">
            <tr>
                <td>Precedence</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Precedence">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:X-Mailer">
            <tr>
                <td>X-Mailer</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:X-Mailer">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:X-Originating-IP">
            <tr>
                <td>X-Originating-IP</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:X-Originating-IP">
                        <xsl:call-template name="processAddressObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:X-Priority">
            <tr>
                <td>X-Priority</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:X-Priority">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    
    <xsl:template name="processEmailHeader">
        <xsl:if test="EmailMessageObj:To">
            <tr>
                <td>To</td>
                <td>            
                    <table id="one-column-emphasis">
                    <colgroup>
                        <col class="oce-first" />
                    </colgroup>
                    <tbody>
                        <xsl:for-each select="EmailMessageObj:To/EmailMessageObj:Recipient">
                            <tr>
                                <td>Recipient</td>
                                <td><xsl:call-template name="processAddressObject"/></td>
                            </tr>
                            <!-- Spacer for repeated entries -->
                            <tr bgcolor="#FFFFFF">
                                <td></td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:CC">
            <tr>
                <td>CC</td>
                <td>            
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="EmailMessageObj:CC/EmailMessageObj:Recipient">
                                <tr>
                                    <td>Recipient</td>
                                    <td><xsl:call-template name="processAddressObject"/></td>
                                </tr>
                                <!-- Spacer for repeated entries -->
                                <tr bgcolor="#FFFFFF">
                                    <td></td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:BCC">
            <tr>
                <td>BCC</td>
                <td>            
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="EmailMessageObj:BCC/EmailMessageObj:Recipient">
                                <tr>
                                    <td>Recipient</td>
                                    <td><xsl:call-template name="processAddressObject"/></td>
                                </tr>
                                <!-- Spacer for repeated entries -->
                                <tr bgcolor="#FFFFFF">
                                    <td></td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:From">
            <tr>
                <td>From</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:From">
                        <xsl:call-template name="processAddressObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:Subject">
            <tr>
                <td>Subject</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Subject">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:In_Reply_To">
            <tr>
                <td>In Reply To</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:In_Reply_To">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:Date">
            <tr>
                <td>Date</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Date">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:Message_ID">
            <tr>
                <td>Message ID</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Message_ID">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:Sender">
            <tr>
                <td>Sender</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Sender">
                        <xsl:call-template name="processAddressObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:Reply_To">
            <tr>
                <td>Reply To</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Reply_To">
                        <xsl:call-template name="processAddressObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="EmailMessageObj:Errors_To">
            <tr>
                <td>Errors To</td>
                <td>
                    <xsl:for-each select="EmailMessageObj:Errors_To">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processSocketObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@is_blocking">
                    <tr>
                        <td>Is Blocking</td>
                        <td><xsl:value-of select="@is_blocking"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="@is_listening">
                    <tr>
                        <td>Is Listening</td>
                        <td><xsl:value-of select="@is_listening"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="SocketObj:Address_Family">
                    <tr>
                        <td>Address Family</td>
                        <td>
                            <xsl:for-each select="SocketObj:Address_Family">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="SocketObj:Domain">
                    <tr>
                        <td>Communication Domain</td>
                        <td>
                            <xsl:for-each select="SocketObj:Domain">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="SocketObj:Local_Address">
                    <tr>
                        <td>Local Address</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="SocketObj:Local_Address">
                                        <xsl:call-template name="processSocketAddress"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="SocketObj:Remote_Address">
                    <tr>
                        <td>Remote Address</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <tr>
                                        <td>Address</td>
                                        <td>
                                            <xsl:for-each select="SocketObj:Remote_Address">
                                                <xsl:call-template name="processSocketAddress"/>
                                            </xsl:for-each>
                                        </td>
                                    </tr>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="SocketObj:Protocol">
                    <tr>
                        <td>IP Protocol</td>
                        <td>
                            <xsl:for-each select="SocketObj:Protocol">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="SocketObj:Options">
                    <tr>
                        <td>Socket Options</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <tr>
                                        <td>Options</td>
                                        <td>                                    
                                            <xsl:for-each select="SocketObj:Options">
                                                <xsl:call-template name="processSocketOptions"/>
                                            </xsl:for-each>
                                        </td>
                                    </tr>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="SocketObj:Type">
                    <tr>
                        <td>Socket Type</td>
                        <td>
                            <xsl:for-each select="SocketObj:Type">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processSocketOptions">
        <xsl:if test="SocketObj:IP_MULTICAST_IF">
            <tr>
                <td>IP_MULTICAST_IF</td>
                <td>
                    <xsl:for-each select="SocketObj:IP_MULTICAST_IF">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:IP_MULTICAST_IF2">
            <tr>
                <td>IP_MULTICAST_IF2</td>
                <td>
                    <xsl:for-each select="SocketObj:IP_MULTICAST_IF2">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:IP_MULTICAST_LOOP">
            <tr>
                <td>IP_MULTICAST_LOOP</td>
                <td>
                    <xsl:for-each select="SocketObj:IP_MULTICAST_LOOP">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:IP_TOS">
            <tr>
                <td>IP_TOS</td>
                <td>
                    <xsl:for-each select="SocketObj:IP_TOS">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_BROADCAST">
            <tr>
                <td>SO_BROADCAST</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_BROADCAST">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_CONDITIONAL_ACCEPT">
            <tr>
                <td>SO_CONDITIONAL_ACCEPT</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_CONDITIONAL_ACCEPT">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_KEEPALIVE">
            <tr>
                <td>SO_KEEPALIVE</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_KEEPALIVE">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_DONTROUTE">
            <tr>
                <td>SO_DONTROUTE</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_DONTROUTE">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_LINGER">
            <tr>
                <td>SO_LINGER</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_LINGER">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_DONTLINGER">
            <tr>
                <td>SO_DONTLINGER</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_DONTLINGER">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_OOBINLINE">
            <tr>
                <td>SO_OOBINLINE</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_OOBINLINE">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_RCVBUF">
            <tr>
                <td>SO_RCVBUF</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_RCVBUF">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_GROUP_PRIORITY">
            <tr>
                <td>SO_GROUP_PRIORITY</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_GROUP_PRIORITY">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_REUSE_ADDR">
            <tr>
                <td>SO_REUSE_ADDR</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_REUSE_ADDR">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_DEBUG">
            <tr>
                <td>SO_DEBUG</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_DEBUG">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_RCVTIMEO">
            <tr>
                <td>SO_RCVTIMEO</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_RCVTIMEO">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_SNDBUF">
            <tr>
                <td>SO_SNDBUF</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_SNDBUF">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_SNDTIMEO">
            <tr>
                <td>SO_SNDTIMEO</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_SNDTIMEO">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_UPDATE_ACCEPT_CONTEXT">
            <tr>
                <td>SO_UPDATE_ACCEPT_CONTEXT</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_UPDATE_ACCEPT_CONTEXT">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:SO_TIMEOUT">
            <tr>
                <td>SO_TIMEOUT</td>
                <td>
                    <xsl:for-each select="SocketObj:SO_TIMEOUT">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:TCP_NODELAY">
            <tr>
                <td>TCP_NODELAY</td>
                <td>
                    <xsl:for-each select="SocketObj:TCP_NODELAY">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processSocketAddress">
        <xsl:if test="SocketObj:IP_Address">
            <tr>
                <td>IP Address</td>
                <td>
                    <xsl:for-each select="SocketObj:IP_Address">
                        <xsl:call-template name="processAddressObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="SocketObj:Port">
            <tr>
                <td>Port</td>
                <td>
                    <xsl:for-each select="SocketObj:Port">
                        <xsl:call-template name="processPortObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processAddressObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@category">
                    <tr>
                        <td>Address Category</td>
                        <td><xsl:value-of select="@category"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="@is_source">
                    <tr>
                        <td>Is Source Address</td>
                        <td><xsl:value-of select="@is_source"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="@is_destination">
                    <tr>
                        <td>Is Destination Address</td>
                        <td><xsl:value-of select="@is_destination"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="AddressObj:Address_Value">
                    <tr>
                        <td>Address</td>
                        <td>
                            <xsl:for-each select="AddressObj:Address_Value">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="AddressObj:Ext_Category">
                    <tr>
                        <td>Extension Category</td>
                        <td>
                            <xsl:for-each select="AddressObj:Ext_Category">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="AddressObj:VLAN_Name">
                    <tr>
                        <td>VLAN Name</td>
                        <td>
                            <xsl:for-each select="AddressObj:VLAN_Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="AddressObj:VLAN_Num">
                    <tr>
                        <td>VLAN Number</td>
                        <td>
                            <xsl:for-each select="AddressObj:VLAN_Num">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processWinServiceObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@service_dll_signature_exists">
                    <tr>
                        <td>Service DLL Signature Exists</td>
                        <td><xsl:value-of select="@service_dll_signature_exists"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="@service_dll_signature_verified">
                    <tr>
                        <td>Service DLL Signature Verified</td>
                        <td><xsl:value-of select="@service_dll_signature_verified"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Description_List">
                    <tr>
                        <td>Descriptions</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinServiceObj:Description_List/WinServiceObj:Description">
                                        <tr>
                                            <td>Description</td>
                                            <td>
                                                <xsl:call-template name="processCyboxValue"/>
                                            </td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Display_Name">
                    <tr>
                        <td>Display Name</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Display_Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Service_Name">
                    <tr>
                        <td>Service Name</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Service_Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Service_DLL">
                    <tr>
                        <td>Service DLL</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Service_DLL">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Service_DLL_Certificate_Issuer">
                    <tr>
                        <td>Service DLL Certificate Issuer</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Service_DLL_Certificate_Issuer">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Service_DLL_Certificate_Subject">
                    <tr>
                        <td>Service DLL Certificate Subject</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Service_DLL_Certificate_Subject">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Service_DLL_Hashes">
                    <tr>
                        <td>Service DLL Hashes</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinServiceObj:Service_DLL_Hashes/Common:Hash">
                                        <xsl:call-template name="processHash"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Service_DLL_Signature_Description">
                    <tr>
                        <td>Service DLL Signature Description</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Service_DLL_Signature_Description">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Startup_Command_Line">
                    <tr>
                        <td>Startup Command Line</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Startup_Command_Line">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Startup_Type">
                    <tr>
                        <td>Startup Type</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Startup_Type">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Service_Status">
                    <tr>
                        <td>Service Status</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Service_Status">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Service_Type">
                    <tr>
                        <td>Service Type</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Service_Type">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinServiceObj:Started_As">
                    <tr>
                        <td>Started As</td>
                        <td>
                            <xsl:for-each select="WinServiceObj:Started_As">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processWinPipeObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="WinPipeObj:Default_Time_Out">
                    <tr>
                        <td>Default Time Out</td>
                        <td>
                            <xsl:for-each select="WinPipeObj:Default_Time_Out">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinPipeObj:Handle">
                    <tr>
                        <td>Handle</td>
                        <td>
                            <xsl:for-each select="WinPipeObj:Handle">
                                <xsl:call-template name="processWinHandleObject"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinPipeObj:In_Buffer_Size">
                    <tr>
                        <td>Input Buffer Size</td>
                        <td>
                            <xsl:for-each select="WinPipeObj:In_Buffer_Size">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinPipeObj:Max_Instances">
                    <tr>
                        <td>Maximum # of Instances</td>
                        <td>
                            <xsl:for-each select="WinPipeObj:Max_Instances">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinPipeObj:Open_Mode">
                    <tr>
                        <td>Open Mode</td>
                        <td>
                            <xsl:for-each select="WinPipeObj:Open_Mode">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinPipeObj:Out_Buffer_Size">
                    <tr>
                        <td>Output Buffer Size</td>
                        <td>
                            <xsl:for-each select="WinPipeObj:Out_Buffer_Size">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinPipeObj:Pipe_Mode">
                    <tr>
                        <td>Pipe Mode</td>
                        <td>
                            <xsl:for-each select="WinPipeObj:Pipe_Mode">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinPipeObj:Security_Attributes">
                    <tr>
                        <td>Security Attributes</td>
                        <td>
                            <xsl:for-each select="WinPipeObj:Security_Attributes">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processLibraryObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="LibraryObj:Name">
                    <tr>
                        <td>Name</td>
                        <td>
                            <xsl:for-each select="LibraryObj:Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="LibraryObj:Base_Address">
                    <tr>
                        <td>Base_Address</td>
                        <td>
                            <xsl:for-each select="LibraryObj:Base_Address">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="LibraryObj:Path">
                    <tr>
                        <td>Path</td>
                        <td>
                            <xsl:for-each select="LibraryObj:Path">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="LibraryObj:Size">
                    <tr>
                        <td>Size (bytes)</td>
                        <td>
                            <xsl:for-each select="LibraryObj:Size">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="LibraryObj:Type">
                    <tr>
                        <td>Type</td>
                        <td>
                            <xsl:for-each select="LibraryObj:Type">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="LibraryObj:Version">
                    <tr>
                        <td>Version</td>
                        <td>
                            <xsl:for-each select="LibraryObj:Version">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processFileObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="FileObj:File_Name">
                    <tr>
                        <td>File Name</td>
                        <td>
                            <xsl:for-each select="FileObj:File_Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:File_Path">
                    <tr>
                        <td>File Path</td>
                        <td>
                            <xsl:for-each select="FileObj:File_Path">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Device_Path">
                    <tr>
                        <td>Device Path</td>
                        <td>
                            <xsl:for-each select="FileObj:Device_Path">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Full_Path">
                    <tr>
                        <td>Full Path</td>
                        <td>
                            <xsl:for-each select="FileObj:Full_Path">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:File_Extension">
                    <tr>
                        <td>File Extension</td>
                        <td>
                            <xsl:for-each select="FileObj:File_Extension">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Size_In_Bytes">
                    <tr>
                        <td>Size (bytes)</td>
                        <td>
                            <xsl:for-each select="FileObj:Size_In_Bytes">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Modified_Time">
                    <tr>
                        <td>Modified Time (m_time)</td>
                        <td>
                            <xsl:for-each select="FileObj:Modified_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Accessed_Time">
                    <tr>
                        <td>Accessed Time (a_time)</td>
                        <td>
                            <xsl:for-each select="FileObj:Accessed_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Created_Time">
                    <tr>
                        <td>Created Time (c_time)</td>
                        <td>
                            <xsl:for-each select="FileObj:Created_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:User_Owner">
                    <tr>
                        <td>User Owner</td>
                        <td>
                            <xsl:for-each select="FileObj:User_Owner">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Peak_Entropy">
                    <tr>
                        <td>User Owner</td>
                        <td>
                            <xsl:for-each select="FileObj:Peak_Entropy">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Hashes">
                    <tr>
                        <td>Hashes</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="FileObj:Hashes/Common:Hash">
                                        <xsl:call-template name="processHash"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Digital_Signatures">
                    <tr>
                        <td>Digital Signatures</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="FileObj:Digital_Signatures/FileObj:Digital_Signature">
                                        <xsl:call-template name="processDigitalSignature"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Sym_Links">
                    <tr>
                        <td>Symbolic Links</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="FileObj:Sym_Links/FileObj:Sym_Link">
                                        <tr>
                                            <td>Symbolic Link</td>
                                            <td><xsl:value-of select="."/></td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Packer_List">
                    <tr>
                        <td>Packed With</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="FileObj:Packer_List/FileObj:Packer">
                                        <xsl:call-template name="processPacker"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Extracted_Features">
                    <tr>
                        <td>Extracted Features</td>
                        <td>
                            <xsl:for-each select="FileObj:Extracted_Features">
                                <xsl:call-template name="processExtractedFeatures"/>
                            </xsl:for-each> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="FileObj:Byte_Runs">
                    <tr>
                        <td>Byte Runs</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="FileObj:Byte_Runs/Common:Byte_Run">
                                        <xsl:call-template name="processByteRun"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processExtractedFeatures">
        <xsl:if test="Common:Strings">
            <table id="one-column-emphasis">
                <colgroup>
                    <col class="oce-first-inner" />
                </colgroup>
                <tbody>
                    <xsl:for-each select="Common:Strings/Common:String">
                        <xsl:call-template name="processExtractedString"/>
                    </xsl:for-each>
                </tbody>
            </table> 
        </xsl:if>
        <xsl:if test="Common:Imports">
            <table id="one-column-emphasis">
                <colgroup>
                    <col class="oce-first-inner-inner" />
                </colgroup>
                <tbody>
                    <xsl:for-each select="Common:Imports/Common:Import">
                        <tr>
                            <td>Extracted Import</td>
                            <td><xsl:value-of select="."/></td>
                        </tr>
                        <!-- Spacer for repeated entries -->
                        <tr bgcolor="#FFFFFF">
                            <td></td>
                        </tr>
                    </xsl:for-each>
                </tbody>
            </table> 
        </xsl:if>
        <xsl:if test="Common:Functions">
            <table id="one-column-emphasis">
                <colgroup>
                    <col class="oce-first-inner-inner" />
                </colgroup>
                <tbody>
                    <xsl:for-each select="Common:Functions/Common:Function">
                        <tr>
                            <td>Extracted Function</td>
                            <td><xsl:value-of select="."/></td>
                        </tr>
                        <!-- Spacer for repeated entries -->
                        <tr bgcolor="#FFFFFF">
                            <td></td>
                        </tr>
                    </xsl:for-each>
                </tbody>
            </table> 
        </xsl:if>

    </xsl:template>
    
    <xsl:template name="processWinDriverObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="WinDriverObj:Driver_Name">
                    <tr>
                        <td>Driver Name</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:Driver_Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:Device_Object_List">
                    <tr>
                        <td>Devices List</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinDriverObj:Device_Object_List/WinDriverObj:Device_Object">
                                        <xsl:call-template name="processDriverDevice"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:Driver_Object_Address">
                    <tr>
                        <td>Driver Object Address</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:Driver_Object_Address">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:Driver_Start_IO">
                    <tr>
                        <td>Driver StartIO Entrypoint</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:Driver_Start_IO">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:Driver_Unload">
                    <tr>
                        <td>Driver Unload Entrypoint</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:Driver_Unload">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:Image_Base">
                    <tr>
                        <td>Preferred Image Base Address</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:Image_Base">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:Image_Size">
                    <tr>
                        <td>Image Size (bytes)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:Image_Size">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_CLEANUP">
                    <tr>
                        <td>IRP_MJ_CLEANUP (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_CLEANUP">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_CLOSE">
                    <tr>
                        <td>IRP_MJ_CLOSE (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_CLOSE">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_CREATE">
                    <tr>
                        <td>IRP_MJ_CREATE (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_CREATE">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_CREATE_MAILSLOT">
                    <tr>
                        <td>IRP_MJ_CREATE_MAILSLOT (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_CREATE_MAILSLOT">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_CREATE_NAMED_PIPE">
                    <tr>
                        <td>IRP_MJ_CREATE_NAMED_PIPE (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_CREATE_NAMED_PIPE">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_DEVICE_CHANGE">
                    <tr>
                        <td>IRP_MJ_DEVICE_CHANGE (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_DEVICE_CHANGE">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_DEVICE_CONTROL">
                    <tr>
                        <td>IRP_MJ_DEVICE_CONTROL (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_DEVICE_CONTROL">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_DIRECTORY_CONTROL">
                    <tr>
                        <td>IRP_MJ_DIRECTORY_CONTROL (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_DIRECTORY_CONTROL">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_FILE_SYSTEM_CONTROL">
                    <tr>
                        <td>IRP_MJ_FILE_SYSTEM_CONTROL (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_FILE_SYSTEM_CONTROL">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_FLUSH_BUFFERS">
                    <tr>
                        <td>IRP_MJ_FLUSH_BUFFERS (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_FLUSH_BUFFERS">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_INTERNAL_DEVICE_CONTROL">
                    <tr>
                        <td>IRP_MJ_INTERNAL_DEVICE_CONTROL (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_INTERNAL_DEVICE_CONTROL">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_LOCK_CONTROL">
                    <tr>
                        <td>IRP_MJ_LOCK_CONTROL (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_LOCK_CONTROL">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_PNP">
                    <tr>
                        <td>IRP_MJ_PNP (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_PNP">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_POWER">
                    <tr>
                        <td>IRP_MJ_POWER (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_POWER">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_READ">
                    <tr>
                        <td>IRP_MJ_READ (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_READ">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_QUERY_EA">
                    <tr>
                        <td>IRP_MJ_QUERY_EA (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_QUERY_EA">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_QUERY_INFORMATION">
                    <tr>
                        <td>IRP_MJ_QUERY_INFORMATION (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_QUERY_INFORMATION">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_QUERY_SECURITY">
                    <tr>
                        <td>IRP_MJ_QUERY_SECURITY (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_QUERY_SECURITY">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_QUERY_QUOTA">
                    <tr>
                        <td>IRP_MJ_QUERY_QUOTA (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_QUERY_QUOTA">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_QUERY_VOLUME_INFORMATION">
                    <tr>
                        <td>IRP_MJ_QUERY_VOLUME_INFORMATION (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_QUERY_VOLUME_INFORMATION">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_SET_EA">
                    <tr>
                        <td>IRP_MJ_SET_EA (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_SET_EA">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_SET_INFORMATION">
                    <tr>
                        <td>IRP_MJ_SET_INFORMATION (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_SET_INFORMATION">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_SET_SECURITY">
                    <tr>
                        <td>IRP_MJ_SET_SECURITY (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_SET_SECURITY">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_SET_QUOTA">
                    <tr>
                        <td>IRP_MJ_SET_QUOTA (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_SET_QUOTA">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_SET_VOLUME_INFORMATION">
                    <tr>
                        <td>IRP_MJ_SET_VOLUME_INFORMATION (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_SET_VOLUME_INFORMATION">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_SHUTDOWN">
                    <tr>
                        <td>IRP_MJ_SHUTDOWN (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_SHUTDOWN">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_SYSTEM_CONTROL">
                    <tr>
                        <td>IRP_MJ_SYSTEM_CONTROL (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_SYSTEM_CONTROL">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinDriverObj:IRP_MJ_WRITE">
                    <tr>
                        <td>IRP_MJ_WRITE (count)</td>
                        <td>
                            <xsl:for-each select="WinDriverObj:IRP_MJ_WRITE">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processDriverDevice">
        <xsl:if test="WinDriverObj:Device_Name">
            <tr>
                <td>Device Name</td>
                <td>
                    <xsl:for-each select="WinDriverObj:Device_Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinDriverObj:Device_Object">
            <tr>
                <td>Device Object</td>
                <td>
                    <xsl:for-each select="WinDriverObj:Device_Object">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinDriverObj:Attached_Device_Name">
            <tr>
                <td>Attached Device Name</td>
                <td>
                    <xsl:for-each select="WinDriverObj:Attached_Device_Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinDriverObj:Attached_Device_Object">
            <tr>
                <td>Attached Device Object</td>
                <td>
                    <xsl:for-each select="WinDriverObj:Attached_Device_Object">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinDriverObj:Attached_To_Device_Name">
            <tr>
                <td>Attached To Device Name</td>
                <td>
                    <xsl:for-each select="WinDriverObj:Attached_To_Device_Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinDriverObj:Attached_To_Device_Object">
            <tr>
                <td>Attached To Device Object</td>
                <td>
                    <xsl:for-each select="WinDriverObj:Attached_To_Device_Object">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinDriverObj:Attached_To_Driver_Object">
            <tr>
                <td>Attached To Driver Object</td>
                <td>
                    <xsl:for-each select="WinDriverObj:Attached_To_Driver_Object">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinDriverObj:Attached_To_Driver_Name">
            <tr>
                <td>Attached To Driver Name</td>
                <td>
                    <xsl:for-each select="WinDriverObj:Attached_To_Driver_Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processWinProcessObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@aslr_enabled">
                    <tr>
                        <td>ASLR Enabled</td>
                        <td><xsl:value-of select="@aslr_enabled"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="@dep_enabled">
                    <tr>
                        <td>DEP Enabled</td>
                        <td><xsl:value-of select="@dep_enabled"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinProcessObj:Handle_List">
                    <tr>
                        <td>Open Handles</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinProcessObj:Handle_List/WinHandleObj:Handle">
                                        <tr>
                                            <td>Handle</td>
                                            <td><xsl:call-template name="processWinHandleObject"/></td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinProcessObj:Priority">
                    <tr>
                        <td>Priority</td>
                        <td>
                            <xsl:for-each select="WinProcessObj:Priority">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinProcessObj:Section_List">
                    <tr>
                        <td>Memory Sections</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinProcessObj:Section_List/WinProcessObj:Memory_Section">
                                        <tr>
                                            <td>Memory Section</td>
                                            <td><xsl:call-template name="processMemoryObject"/></td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinProcessObj:Security_ID">
                    <tr>
                        <td>Security ID (SID)</td>
                        <td>
                            <xsl:for-each select="WinProcessObj:Security_ID">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinProcessObj:Startup_Info">
                    <tr>
                        <td>Startup Info</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinProcessObj:Startup_Info">
                                        <xsl:call-template name="processStartupInfo"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinProcessObj:Security_Type">
                    <tr>
                        <td>Security ID (SID) Type</td>
                        <td>
                            <xsl:for-each select="WinProcessObj:Security_Type">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinProcessObj:Window_Title">
                    <tr>
                        <td>Window Title</td>
                        <td>
                            <xsl:for-each select="WinProcessObj:Window_Title">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processProcessObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="@is_hidden">
                    <tr>
                        <td>Is Hidden</td>
                        <td><xsl:value-of select="@is_hidden"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:PID">
                    <tr>
                        <td>Process ID (PID)</td>
                        <td>
                            <xsl:for-each select="ProcessObj:PID">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Name">
                    <tr>
                        <td>Name</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Name">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Path">
                    <tr>
                        <td>Path</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Path">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Current_Working_Directory">
                    <tr>
                        <td>Current Working Directory</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Current_Working_Directory">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Creation_Time">
                    <tr>
                        <td>Creation Date/Time</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Creation_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Parent_PID">
                    <tr>
                        <td>Parent PID</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Parent_PID">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Child_PID_List">
                    <tr>
                        <td>Children (PIDs)</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="ProcessObj:Child_PID_List/ProcessObj:Child_PID">
                                        <tr>
                                            <td>Child PID</td>
                                            <td><xsl:value-of select="."/></td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Argument_List">
                    <tr>
                        <td>Argument List</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="ProcessObj:Argument_List/ProcessObj:Argument">
                                        <tr>
                                            <td>Argument</td>
                                            <td><xsl:value-of select="."/></td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Environment_Variable_List">
                    <tr>
                        <td>Environment Variables</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="ProcessObj:Environment_Variable_List/Common:Environment_Variable">
                                        <xsl:call-template name="processEnvironmentVariable"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Image_Info">
                    <tr>
                        <td>Image Information</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="ProcessObj:Image_Info">
                                        <xsl:call-template name="processImageInfo"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Kernel_Time">
                    <tr>
                        <td>Kernel Time</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Kernel_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Port_List">
                    <tr>
                        <td>Open Ports</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="ProcessObj:Port_List/ProcessObj:Port">
                                        <tr>
                                            <td>Port</td>
                                            <td><xsl:call-template name="processPortObject"/></td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Network_Connection_List">
                    <tr>
                        <td>Open Network Connections</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="ProcessObj:Network_Connection_List/ProcessObj:Network_Connection">
                                        <xsl:call-template name="processNetworkConnection"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Start_Time">
                    <tr>
                        <td>Start Time</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Start_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Status">
                    <tr>
                        <td>Status</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Status">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:String_List">
                    <tr>
                        <td>Strings</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="ProcessObj:String_List/Common:String">
                                        <xsl:call-template name="processExtractedString"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:Username">
                    <tr>
                        <td>Username</td>
                        <td>
                            <xsl:for-each select="ProcessObj:Username">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="ProcessObj:User_Time">
                    <tr>
                        <td>User Time</td>
                        <td>
                            <xsl:for-each select="ProcessObj:User_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processWinFileObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="WinFileObj:Filename_Accessed_Time">
                    <tr>
                        <td>Filename Accessed Time</td>
                        <td>
                            <xsl:for-each select="WinFileObj:Filename_Accessed_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinFileObj:Filename_Created_Time">
                    <tr>
                        <td>Filename Created Time</td>
                        <td>
                            <xsl:for-each select="WinFileObj:Filename_Created_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinFileObj:Filename_Modified_Time">
                    <tr>
                        <td>Filename Modified Time</td>
                        <td>
                            <xsl:for-each select="WinFileObj:Filename_Modified_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinFileObj:Drive">
                    <tr>
                        <td>Drive Letter</td>
                        <td>
                            <xsl:for-each select="WinFileObj:Drive">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinFileObj:Security_ID">
                    <tr>
                        <td>Security ID (SID)</td>
                        <td>
                            <xsl:for-each select="WinFileObj:Security_ID">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinFileObj:Security_Type">
                    <tr>
                        <td>Security Type</td>
                        <td>
                            <xsl:for-each select="WinFileObj:Security_Type">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinFileObj:Stream_List">
                    <tr>
                        <td>Stream List</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinFileObj:Stream_List/WinFileObj:Stream">
                                        <xsl:call-template name="processStream"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processWinRegistryKeyObject">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="WinRegistryKeyObj:Hive">
                    <tr>
                        <td>Hive</td>
                        <td>
                            <xsl:for-each select="WinRegistryKeyObj:Hive">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Key">
                    <tr>
                        <td>Key</td>
                        <td>
                            <xsl:for-each select="WinRegistryKeyObj:Key">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Number_Values">
                    <tr>
                        <td>Number of Values</td>
                        <td>
                            <xsl:for-each select="WinRegistryKeyObj:Number_Values">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Modified_Time">
                    <tr>
                        <td>Modified Time</td>
                        <td>
                            <xsl:for-each select="WinRegistryKeyObj:Modified_Time">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Creator_Username">
                    <tr>
                        <td>Creator Username</td>
                        <td>
                            <xsl:for-each select="WinRegistryKeyObj:Creator_Username">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Number_Subkeys">
                    <tr>
                        <td>Number of Subkeys</td>
                        <td>
                            <xsl:for-each select="WinRegistryKeyObj:Number_Subkeys">
                                <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Values">
                    <tr>
                        <td>Values</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinRegistryKeyObj:Values/WinRegistryKeyObj:Value">
                                        <xsl:call-template name="processWinRegistryValue"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Handle_List">
                    <tr>
                        <td>Handle List</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinRegistryKeyObj:Handle_List/WinHandleObj:Handle">
                                        <tr>
                                            <td>Handle</td>
                                            <td><xsl:call-template name="processWinHandleObject"/></td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Subkeys">
                    <tr>
                        <td>Subkeys</td>
                        <td>
                            <xsl:for-each select="WinRegistryKeyObj:Subkeys/WinRegistryKeyObj:Subkey">
                              <xsl:call-template name="processCyboxValue"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="WinRegistryKeyObj:Byte_Runs">
                    <tr>
                        <td>Byte Runs</td>
                        <td>
                            <table id="one-column-emphasis">
                                <colgroup>
                                    <col class="oce-first-inner" />
                                </colgroup>
                                <tbody>
                                    <xsl:for-each select="WinRegistryKeyObj:Byte_Runs/Common:Byte_Run">
                                        <xsl:call-template name="processByteRun"/>
                                    </xsl:for-each>
                                </tbody>
                            </table> 
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
    
    <xsl:template name="processStream">
        <xsl:if test="WinFileObj:Name">
            <tr>
                <td>Name</td>
                <td>
                    <xsl:for-each select="WinFileObj:Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinFileObj:Size_In_Bytes">
            <tr>
                <td>Size (bytes)</td>
                <td>
                    <xsl:for-each select="WinFileObj:Size_In_Bytes">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Hash">
            <tr>
                <td>Hashes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Hash">
                                <xsl:call-template name="processHash"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processHash">
        <tr>
            <xsl:choose>
                <xsl:when test="Common:Other_Type">
                    <td>
                        <xsl:for-each select="Common:Other_Type">
                            <xsl:call-template name="processCyboxValue"/>
                        </xsl:for-each>
                    </td>
                </xsl:when>
                <xsl:otherwise>
                    <td><xsl:value-of select="Common:Type"/></td>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="Common:Fuzzy_Hash_Value">
                    <td>
                        <xsl:for-each select="Common:Fuzzy_Hash_Value">
                            <xsl:call-template name="processCyboxValue"/>
                        </xsl:for-each>
                    </td>
                </xsl:when>
                <xsl:otherwise>
                    <td>
                        <xsl:for-each select="Common:Simple_Hash_Value">
                            <xsl:call-template name="processCyboxValue"/>
                        </xsl:for-each>
                    </td>
                </xsl:otherwise>
            </xsl:choose>
        </tr>
    </xsl:template>
    
    <xsl:template name="processEnvironmentVariable">
        <xsl:if test="Common:Name">
            <tr>
                <td>Name</td>
                <td>
                    <xsl:for-each select="Common:Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Value">
            <tr>
                <td>Value</td>
                <td>
                    <xsl:for-each select="Common:Value">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processExtractedString">
        <xsl:if test="@encoding">
            <tr>
                <td>Encoding</td>
                <td><xsl:value-of select="@encoding"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:String_Value">
            <tr>
                <td>String Value</td>
                <td>
                    <xsl:for-each select="Common:String_Value">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Hashes">
            <tr>
                <td>Hashes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Hashes/Common:Hash">
                                <xsl:call-template name="processHash"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Address">
            <tr>
                <td>Address</td>
                <td>
                    <xsl:for-each select="Common:Address">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Length">
            <tr>
                <td>Length (characters)</td>
                <td>
                    <xsl:for-each select="Common:Length">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Language">
            <tr>
                <td>Language</td>
                <td>
                    <xsl:for-each select="Common:Language">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:English_Translation">
            <tr>
                <td>English Translation</td>
                <td>
                    <xsl:for-each select="Common:English_Translation">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processNetworkConnection">
        <xsl:if test="ProcessObj:Creation_Time">
            <tr>
                <td>Creation Time</td>
                <td>
                    <xsl:for-each select="ProcessObj:Creation_Time">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="ProcessObj:Destination_IP_Address">
            <tr>
                <td>Destination IP Address</td>
                <td>
                    <xsl:for-each select="ProcessObj:Destination_IP_Address">
                        <xsl:call-template name="processAddressObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="ProcessObj:Destination_Port">
            <tr>
                <td>Destination Port</td>
                <td>
                    <xsl:for-each select="ProcessObj:Destination_Port">
                        <xsl:call-template name="processPortObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="ProcessObj:Source_IP_Address">
            <tr>
                <td>Source IP Address</td>
                <td>
                    <xsl:for-each select="ProcessObj:Source_IP_Address">
                        <xsl:call-template name="processAddressObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="ProcessObj:Source_Port">
            <tr>
                <td>Source Port</td>
                <td>
                    <xsl:for-each select="ProcessObj:Source_Port">
                        <xsl:call-template name="processPortObject"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="ProcessObj:TCP_State">
            <tr>
                <td>TCP State</td>
                <td>
                    <xsl:for-each select="ProcessObj:TCP_State">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processStartupInfo">
        <xsl:if test="WinProcessObj:lpDesktop">
            <tr>
                <td>lpDesktop</td>
                <td>
                    <xsl:for-each select="WinProcessObj:lpDesktop">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:lpTitle">
            <tr>
                <td>lpTitle</td>
                <td>
                    <xsl:for-each select="WinProcessObj:lpTitle">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:dwX">
            <tr>
                <td>dwX</td>
                <td>
                    <xsl:for-each select="WinProcessObj:dwX">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:dwY">
            <tr>
                <td>dwY</td>
                <td>
                    <xsl:for-each select="WinProcessObj:dwY">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:dwXSize">
            <tr>
                <td>dwXSize</td>
                <td>
                    <xsl:for-each select="WinProcessObj:dwXSize">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:dwYSize">
            <tr>
                <td>dwYSize</td>
                <td>
                    <xsl:for-each select="WinProcessObj:dwYSize">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:dwXCountChars">
            <tr>
                <td>dwXCountChars</td>
                <td>
                    <xsl:for-each select="WinProcessObj:dwXCountChars">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:dwYCountChars">
            <tr>
                <td>dwYCountChars</td>
                <td>
                    <xsl:for-each select="WinProcessObj:dwYCountChars">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:dwFillAttribute">
            <tr>
                <td>dwFillAttribute</td>
                <td>
                    <xsl:for-each select="WinProcessObj:dwFillAttribute">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:dwFlags">
            <tr>
                <td>dwFlags</td>
                <td>
                    <xsl:for-each select="WinProcessObj:dwFlags">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:wShowWindow">
            <tr>
                <td>wShowWindow</td>
                <td>
                    <xsl:for-each select="WinProcessObj:wShowWindow">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:hStdInput">
            <tr>
                <td>hStdInput</td>
                <td>
                    <xsl:for-each select="WinProcessObj:hStdInput">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:hStdOutput">
            <tr>
                <td>hStdOutput</td>
                <td>
                    <xsl:for-each select="WinProcessObj:hStdOutput">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinProcessObj:hStdError">
            <tr>
                <td>hStdError</td>
                <td>
                    <xsl:for-each select="WinProcessObj:hStdError">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processImageInfo">
        <xsl:if test="ProcessObj:Command_Line">
            <tr>
                <td>Command Line</td>
                <td>
                    <xsl:for-each select="ProcessObj:Command_Line">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="ProcessObj:Current_Directory">
            <tr>
                <td>Current Directory</td>
                <td>
                    <xsl:for-each select="ProcessObj:Current_Directory">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="ProcessObj:Path">
            <tr>
                <td>Path</td>
                <td>
                    <xsl:for-each select="ProcessObj:Path">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processDigitalSignature">
        <xsl:if test="@signature_exists">
            <tr>
                <td>Signature Exists</td>
                <td><xsl:value-of select="@signature_exists"></xsl:value-of></td>
            </tr>
        </xsl:if>
        <xsl:if test="@signature_verified">
            <tr>
                <td>Signature Verified</td>
                <td><xsl:value-of select="@signature_verified"></xsl:value-of></td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Certificate_Issuer">
            <tr>
                <td>Certificate Issuer</td>
                <td>
                    <xsl:for-each select="Common:Certificate_Issuer">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Certificate_Subject">
            <tr>
                <td>Certificate Subject</td>
                <td>
                    <xsl:for-each select="Common:Certificate_Subject">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Certificate_Description">
            <tr>
                <td>Certificate Description</td>
                <td>
                    <xsl:for-each select="Common:Certificate_Description">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processPeakCodeEntropy">
        <xsl:if test="WinExecutableFileObj:Peak_Code_Entropy/WinExecutableFileObj:Value">
            <tr>
                <td>Value</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Peak_Code_Entropy/WinExecutableFileObj:Value">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Peak_Code_Entropy/WinExecutableFileObj:Min">
            <tr>
                <td>Minimum</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Peak_Code_Entropy/WinExecutableFileObj:Min">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Peak_Code_Entropy/WinExecutableFileObj:Max">
            <tr>
                <td>Maximum</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Peak_Code_Entropy/WinExecutableFileObj:Max">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processByteRun">
        <xsl:if test="Common:Offset">
            <tr>
                <td>Offset</td>
                <td>
                    <xsl:for-each select="Common:Offset">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:File_System_Offset">
            <tr>
                <td>File System Offset</td>
                <td>
                    <xsl:for-each select="Common:File_System_Offset">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Image_Offset">
            <tr>
                <td>Image Offset</td>
                <td>
                    <xsl:for-each select="Common:Image_Offset">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Length">
            <tr>
                <td>Length</td>
                <td>
                    <xsl:for-each select="Common:Length">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Byte_Run_Data">
            <tr>
                <td>Byte Run Data</td>
                <td>
                    <xsl:for-each select="Common:Byte_Run_Data">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="Common:Hashes">
            <tr>
                <td>Hashes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="Common:Hashes/Common:Hash">
                                <xsl:call-template name="processHash"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processPacker">
        <xsl:if test="FileObj:Name">
            <tr>
                <td>Packer Name</td>
                <td>
                    <xsl:for-each select="FileObj:Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="FileObj:Version">
            <tr>
                <td>Packer Version</td>
                <td>
                    <xsl:for-each select="FileObj:Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="FileObj:Type">
            <tr>
                <td>Packer Type</td>
                <td>
                    <xsl:for-each select="FileObj:Type">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="FileObj:PEiD">
            <tr>
                <td>PEiD</td>
                <td>
                    <xsl:for-each select="FileObj:PEiD">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processWinRegistryValue">
        <xsl:if test="WinRegistryKeyObj:Name">
            <tr>
                <td>Name</td>
                <td>
                    <xsl:for-each select="WinRegistryKeyObj:Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinRegistryKeyObj:Data">
            <tr>
                <td>Data</td>
                <td>
                    <xsl:for-each select="WinRegistryKeyObj:Data">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinRegistryKeyObj:Datatype">
            <tr>
                <td>Datatype</td>
                <td>
                    <xsl:for-each select="WinRegistryKeyObj:Datatype">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinRegistryKeyObj:Byte_Runs">
            <tr>
                <td>Byte Runs</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinRegistryKeyObj:Byte_Runes/Common:Byte_Run">
                                <xsl:call-template name="processByteRun"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processEPJumpCode">
        <xsl:if test="WinExecutableFileObj:Depth">
            <tr>
                <td>Depth</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Depth">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Opcodes">
            <tr>
                <td>Opcodes</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Opcodes">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processPEAttributes">
        <xsl:if test="WinExecutableFileObj:Base_Address">
            <tr>
                <td>Base Address</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Base_Address">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Extraneous_Bytes">
            <tr>
                <td>Extraneous Bytes</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Extraneous_Bytes">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Digital_Signature">
            <tr>
                <td>Digital Signature</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Digital_Signature">
                                <xsl:call-template name="processDigitalSignature"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:EP_Jump_Codes">
            <tr>
                <td>EP Jump Codes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:EP_Jump_Codes">
                                <xsl:call-template name="processEPJumpCode"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:PE_Timestamp">
            <tr>
                <td>PE Timestamp</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:PE_Timestamp">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Subsystem">
            <tr>
                <td>Subsystem</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Subsystem">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Type">
            <tr>
                <td>Type</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Type">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Imports">
            <tr>
                <td>Imports</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Imports/WinExecutableFileObj:Import">
                                <xsl:call-template name="processPEImport"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Exports">
            <tr>
                <td>Exports</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Exports">
                                <xsl:call-template name="processPEExports"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Headers">
            <tr>
                <td>PE Headers</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Headers">
                                <xsl:call-template name="processPEHeaders"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processPEHeaders">
        <xsl:if test="WinExecutableFileObj:Signature">
            <tr>
                <td>Signature</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Signature">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:DOS_Header">
            <tr>
                <td>DOS Header</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:DOS_Header">
                                <xsl:call-template name="processDOSHeader"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:File_Header">
            <tr>
                <td>File Header</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:File_Header">
                                <xsl:call-template name="processPEFileHeader"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Optional_Header">
            <tr>
                <td>Optional Header</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Optional_Header">
                                <xsl:call-template name="processPEOptionalHeader"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Entropy">
            <tr>
                <td>Entropy</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Entropy">
                                <xsl:call-template name="processEntropy"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Hashes">
            <tr>
                <td>Hashes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Hashes/Common:Hash">
                                <xsl:call-template name="processHash"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processEntropy">
        <xsl:if test="WinExecutableFileObj:Value">
            <tr>
                <td>Value</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Value">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Min">
            <tr>
                <td>Minimum</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Min">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Max">
            <tr>
                <td>Maximum</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Max">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processDOSHeader">
        <xsl:if test="WinExecutableFileObj:e_magic">
            <tr>
                <td>e_magic</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_magic">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_cblp">
            <tr>
                <td>e_cblp</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_cblp">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_cp">
            <tr>
                <td>e_cp</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_cp">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_crlc">
            <tr>
                <td>e_crlc</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_crlc">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_cparhdr">
            <tr>
                <td>e_cparhdr</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_cparhdr">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_minalloc">
            <tr>
                <td>e_minalloc</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_minalloc">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_maxalloc">
            <tr>
                <td>e_maxalloc</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_maxalloc">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_ss">
            <tr>
                <td>e_ss</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_ss">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_sp">
            <tr>
                <td>e_sp</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_sp">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_csum">
            <tr>
                <td>e_csum</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_csum">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_ip">
            <tr>
                <td>e_ip</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_ip">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_cs">
            <tr>
                <td>e_cs</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_cs">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_lfarlc">
            <tr>
                <td>e_lfarlc</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_lfarlc">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_ovro">
            <tr>
                <td>e_ovro</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_ovro">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:reserved1">
            <xsl:for-each select="WinExecutableFileObj:reserved1">
                <tr>
                    <td>reserved1</td>
                    <td><xsl:value-of select="."/></td>
                </tr>
            </xsl:for-each>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_oemid">
            <tr>
                <td>e_oemid</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_oemid">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_oeminfo">
            <tr>
                <td>e_oeminfo</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_oeminfo">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:reserved2">
            <tr>
                <td>reserved2</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:reserved2">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:e_lfanew">
            <tr>
                <td>e_lfanew</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:e_lfanew">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Hashes">
            <tr>
                <td>Hashes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Hashes/Common:Hash">
                                <xsl:call-template name="processHash"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processPEFileHeader">
        <xsl:if test="WinExecutableFileObj:Machine">
            <tr>
                <td>Machine</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Machine">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Number_Of_Sections">
            <tr>
                <td>Number of Sections</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Number_Of_Sections">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Time_Date_Stamp">
            <tr>
                <td>Time/Date Stamp</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Time_Date_Stamp">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Pointer_To_Symbol_Table">
            <tr>
                <td>Pointer to Symbol Table</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Pointer_To_Symbol_Table">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Number_Of_Symbols">
            <tr>
                <td>Number of Symbols</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Number_Of_Symbols">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Optional_Header">
            <tr>
                <td>Size of Optional Header</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Optional_Header">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Characteristics">
            <tr>
                <td>Characteristics</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Characteristics">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Hashes">
            <tr>
                <td>Hashes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Hashes/Common:Hash">
                                <xsl:call-template name="processHash"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processPEOptionalHeader">
        <xsl:if test="WinExecutableFileObj:Magic">
            <tr>
                <td>Magic</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Magic">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Major_Linker_Version">
            <tr>
                <td>Major Linker Version</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Major_Linker_Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Minor_Linker_Version">
            <tr>
                <td>Minor Linker Version</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Minor_Linker_Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Code">
            <tr>
                <td>Size of Code</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Code">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Initialized_Data">
            <tr>
                <td>Size of Initialized Data</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Initialized_Data">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Uninitialized_Data">
            <tr>
                <td>Size of Uninitialized Data</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Uninitialized_Data">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Address_Of_Entry_Point">
            <tr>
                <td>Address of Entry Point</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Address_Of_Entry_Point">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Base_Of_Code">
            <tr>
                <td>Base of Code</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Base_Of_Code">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Base_Of_Data">
            <tr>
                <td>Base of Data</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Base_Of_Data">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Image_Base">
            <tr>
                <td>Image Base</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Image_Base">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Section_Alignment">
            <tr>
                <td>Section Alignment</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Section_Alignment">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:File_Alignment">
            <tr>
                <td>File Alignment</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:File_Alignment">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Major_OS_Version">
            <tr>
                <td>Major OS Version</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Major_OS_Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Minor_OS_Version">
            <tr>
                <td>Minor OS Version</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Minor_OS_Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Major_Image_Version">
            <tr>
                <td>Major Image Version</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Major_Image_Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Minor_Image_Version">
            <tr>
                <td>Minor Image Version</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Minor_Image_Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Major_Subsystem_Version">
            <tr>
                <td>Major Subsystem Version</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Major_Subsystem_Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Minor_Subsystem_Version">
            <tr>
                <td>Minor Subsystem Version</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Minor_Subsystem_Version">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Win32_Version_Value">
            <tr>
                <td>Win32 Version Value</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Win32_Version_Value">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Image">
            <tr>
                <td>Size of Image</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Image">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Headers">
            <tr>
                <td>Size of Headers</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Headers">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Checksum">
            <tr>
                <td>Checksum</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Checksum">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Subsystem">
            <tr>
                <td>Subsystem</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Subsystem">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:DLL_Characteristics">
            <tr>
                <td>DLL Characteristics</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:DLL_Characteristics">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Stack_Reserve">
            <tr>
                <td>Size of Stack Reserve</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Stack_Reserve">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Stack_Commit">
            <tr>
                <td>Size of Stack Commit</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Stack_Commit">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Heap_Reserve">
            <tr>
                <td>Size of Heap Reserve</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Heap_Reserve">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size_Of_Heap_Commit">
            <tr>
                <td>Size of Heap Commit</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size_Of_Heap_Commit">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Loader_Flags">
            <tr>
                <td>Loader Flags</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Loader_Flags">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Number_Of_Rva_And_Sizes">
            <tr>
                <td>Number of RVA and Sizes</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Number_Of_Rva_And_Sizes">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Data_Directory">
            <tr>
                <td>Data Directory</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Data_Directory">
                                <xsl:call-template name="processDataDirectory"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Hashes">
            <tr>
                <td>Hashes</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Hashes/Common:Hash">
                                <xsl:call-template name="processHash"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processDataDirectory">
        <xsl:if test="WinExecutableFileObj:Export_Table">
            <tr>
                <td>Export Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Export_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Import_Table">
            <tr>
                <td>Import Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Import_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Resource_Table">
            <tr>
                <td>Resource Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Resource_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Exception_Table">
            <tr>
                <td>Exception Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Exception_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Certificate_Table">
            <tr>
                <td>Certificate Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Certificate_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Base_Relocation_Table">
            <tr>
                <td>Base Relocation Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Base_Relocation_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Debug">
            <tr>
                <td>Debug</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Debug">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Architecture">
            <tr>
                <td>Architecture</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Architecture">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Global_Ptr">
            <tr>
                <td>Global Pointer</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Global_Ptr">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:TLS_Table">
            <tr>
                <td>TLS Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:TLS_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Load_Config_Table">
            <tr>
                <td>Load Config Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Load_Config_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Bound_Import">
            <tr>
                <td>Bound Import Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Bound_Import">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Import_Address_Table">
            <tr>
                <td>Import Address Table</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Import_Address_Table">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Delay_Import_Descriptor">
            <tr>
                <td>Delay Import Descriptor</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Delay_Import_Descriptor">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:CLR_Runtime_Header">
            <tr>
                <td>CLR Runtime Header</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:CLR_Runtime_Header">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Reserved">
            <tr>
                <td>Reserved</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Reserved">
                                <xsl:call-template name="processPEDataDirectoryStruct"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr> 
            <tr bgcolor="#FFFFFF">
                <td></td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processPEDataDirectoryStruct">
        <xsl:if test="WinExecutableFileObj:Virtual_Address">
            <tr>
                <td>Virtual Address</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Virtual_Address">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Size">
            <tr>
                <td>Size (bytes)</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Size">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processPEImport">
        <xsl:if test="WinExecutableFileObj:File_Name">
            <tr>
                <td>File Name</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:File_Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Virtual_Address">
            <tr>
                <td>Virtual Address</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Virtual_Address">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="@delay_load">
            <tr>
                <td>Delay Load</td>
                <td><xsl:value-of select="@delay_load"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="@initially_visible">
            <tr>
                <td>Initially Visible</td>
                <td><xsl:value-of select="@initially_visible"/></td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Imported_Functions">
            <tr>
                <td>Imported Functions</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Imported_Functions/WinExecutableFileObj:Imported_Function">
                                <xsl:call-template name="processPEImportedFunction"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processPEExports">
        <xsl:if test="WinExecutableFileObj:Exports_Time_Stamp">
            <tr>
                <td>Exports Time Stamp</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Exports_Time_Stamp">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Number_Of_Addresses">
            <tr>
                <td>Number of Addresses</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Number_Of_Addresses">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Number_Of_Names">
            <tr>
                <td>Number of Names</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Number_Of_Names">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Exported_Functions">
            <tr>
                <td>Exported Functions</td>
                <td>
                    <table id="one-column-emphasis">
                        <colgroup>
                            <col class="oce-first-inner-inner-inner" />
                        </colgroup>
                        <tbody>
                            <xsl:for-each select="WinExecutableFileObj:Exported_Functions/WinExecutableFileObj:Exported_Function">
                                <xsl:call-template name="processPEExportedFunction"/>
                            </xsl:for-each>
                        </tbody>
                    </table> 
                </td>
            </tr>  
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="processPEExportedFunction">
        <xsl:if test="WinExecutableFileObj:Function_Name">
            <tr>
                <td>Function Name</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Function_Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Entry_Point">
            <tr>
                <td>Entry Point</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Entry_Point">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Ordinal">
            <tr>
                <td>Ordinal</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Ordinal">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processPEImportedFunction">
        <xsl:if test="WinExecutableFileObj:Function_Name">
            <tr>
                <td>Function Name</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Function_Name">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Hint">
            <tr>
                <td>Hint</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Hint">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Hint">
            <tr>
                <td>Ordinal</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Hint">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Bound">
            <tr>
                <td>Bound</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Bound">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <xsl:if test="WinExecutableFileObj:Virtual_Address">
            <tr>
                <td>Virtual Address</td>
                <td>
                    <xsl:for-each select="WinExecutableFileObj:Virtual_Address">
                        <xsl:call-template name="processCyboxValue"/>
                    </xsl:for-each>
                </td>
            </tr>
        </xsl:if>
        <!-- Spacer for repeated entries -->
        <tr bgcolor="#FFFFFF">
            <td></td>
        </tr>
    </xsl:template>
    
    <xsl:template name="processStructuredTextGroup">
        <table id="one-column-emphasis">
            <colgroup>
                <col class="oce-first" />
            </colgroup>
            <tbody>
                <xsl:if test="Common:Text_Title">
                    <tr>
                        <td>Title</td>
                        <td><xsl:value-of select="Common:Text_Title"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="Common:Text">
                    <tr>
                        <td>Text</td>
                        <td><xsl:value-of select="Common:Text"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="Common:Code_Example_Language">
                    <tr>
                        <td>Code Example Language</td>
                        <td><xsl:value-of select="Common:Code_Example_Language"/></td>
                    </tr>
                </xsl:if>
                <xsl:if test="Common:Code">
                    <tr>
                        <td>Code</td>
                        <td><xsl:value-of select="Common:Code"/></td>
                    </tr>
                </xsl:if>
            </tbody>
        </table> 
    </xsl:template>
</xsl:stylesheet>
