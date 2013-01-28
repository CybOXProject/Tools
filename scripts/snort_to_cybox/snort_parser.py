#Snort to CybOX Translator
#v0.1
#Snort Rule Parser

import pyparsing as pyp
import itertools

class snort_parser():
    def __init__(self):
        #Counter for keeping tracking of how many rules were skipped
        self.skipped_rules = 0
        #Define all of the Snort grammar
        self.word = pyp.Word(pyp.printables)
        self.alphanumword = pyp.Word(pyp.alphanums)
        self.var_word = pyp.Combine(pyp.Group(pyp.Literal('$') + self.alphanumword + pyp.ZeroOrMore(pyp.Literal('_') + self.alphanumword)))
        self.integer=pyp.Word(pyp.nums)
        self.ipfield=pyp.Word(pyp.nums,max=3)
        self.cidr_int = pyp.Word(pyp.nums, max=2)
        self.action = pyp.oneOf('pass log alert activate dynamic drop reject sdrop').setResultsName('action')
        self.protocol = pyp.oneOf('tcp udp icmp any').setResultsName('protocol')
        self.direction = pyp.oneOf('-> <>').setResultsName('direction')
        self.cidr_suffix = pyp.Combine(pyp.Literal('/') + self.cidr_int)
        self.ip_addr=pyp.Combine(pyp.Optional(pyp.Literal('!'))+self.ipfield+'.'+self.ipfield+'.'+self.ipfield+'.'+self.ipfield+pyp.Optional(self.cidr_suffix))
        self.ip_addr_list = pyp.Combine(pyp.Literal(',') + self.ip_addr)
        self.snort_ip_list = pyp.Combine(pyp.Suppress('[') + self.ip_addr + pyp.ZeroOrMore(self.ip_addr_list) + pyp.Suppress(']'))
        self.port = pyp.Combine(pyp.Group(pyp.Optional(pyp.Literal('!')) + self.integer))
        self.port_range = pyp.Combine(pyp.Group(pyp.Optional(pyp.Literal(':')) + self.port + pyp.Optional(pyp.Literal(':') + self.port | pyp.Literal(':'))))
        self.port_list_element = pyp.Combine(pyp.Literal(',') + self.port_range)
        self.snort_port_list = pyp.Combine(pyp.Suppress('[') + self.port_range + pyp.ZeroOrMore(self.port_list_element) + pyp.Suppress(']'))
        self.ip_or_word = self.ip_addr | self.snort_ip_list | self.var_word | pyp.Literal('any')
        self.port_or_word = self.port_range | self.snort_port_list | self.var_word | pyp.Literal('any')
        self.src_ip = self.ip_or_word.setResultsName('src_ip')
        self.dst_ip = self.ip_or_word.setResultsName('dst_ip')
        self.src_port = self.port_or_word.setResultsName('src_port')
        self.dst_port = self.port_or_word.setResultsName('dst_port')
        #These are the modifiers we currently support
        self.content_modifiers = pyp.oneOf('offset depth distance within nocase rawbytes')
        #The general options and some useful extras
        self.general_options = pyp.oneOf('msg reference gid sid rev classtype priority metadata fragoffset ttl id ipopts dsize seq ack window')
        self.modifier_statement = pyp.ZeroOrMore(pyp.Combine(self.content_modifiers + pyp.SkipTo(';',include=True)))
        self.content = pyp.Combine(pyp.Literal('content:') + pyp.SkipTo(';',include=True))
        self.content_statement = pyp.Group(self.content + self.modifier_statement).setResultsName('content_statement', listAllMatches=True)
        self.pcre_statement = pyp.Combine(pyp.Literal('pcre:') + pyp.SkipTo(';',include=True)).setResultsName('pcre_statement', listAllMatches=True)
        self.option_prefix = pyp.Combine(self.general_options + pyp.Literal(':'))
        self.useful_options = pyp.Combine(self.option_prefix + pyp.SkipTo(';',include=True)).setResultsName('options', listAllMatches=True)
        self.other_options = pyp.Combine(self.alphanumword + pyp.SkipTo(';',include=True))
        self.options_statement = self.content_statement | self.pcre_statement | self.useful_options | pyp.Suppress(self.other_options)
        self.rule_header=pyp.Suppress("(") + pyp.OneOrMore(self.options_statement) + pyp.Suppress(")")
        #Build the BNF expression for the actual parsing
        self.snort_bnf = self.action+self.protocol+self.src_ip+self.src_port+self.direction+self.dst_ip+self.dst_port+self.rule_header
    
    #Get the number of skipped rules
    def get_skipped_rules(self):
        return self.skipped_rules
    
    #Parse and return a single rule
    def parse_rule_string(self, rulestring):
        if self.usable_rule_check(rulestring):
            return self.snort_bnf.parseString(rulestring)
        else:
            return None
    
    #Check if we should process a snort rule
    def usable_rule_check(self, rulestring):
        if len(rulestring) < 2:
            return False
        disallowed_options =['http_','fast_pattern','uricontent', 'urilen', 'isdataat',\
                             'file_data', 'base64_','byte_', 'ftpbounce', 'asn1', 'cvs',\
                             'dce_', 'sip_', 'gtp_', 'ssl_', 'base64_', 'tos', 'fragbits',\
                             'flags']
        if rulestring[0] == '#' or rulestring[1] == '#':
            return False
        for disallowed_option in disallowed_options:
            if disallowed_option in rulestring:
                self.skipped_rules += 1
                return False
        return True
    
    #Parse and return a set of rules from a file
    def parse_rule_file(self, rulefile):
        parsed_rules = []
        
        for line in open(rulefile, 'r').readlines():
            if self.usable_rule_check(line):
                parsed_rules.append(self.snort_bnf.parseString(line).asDict())
        
        return parsed_rules

